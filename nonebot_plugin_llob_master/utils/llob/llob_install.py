import os
import sys
import json
import ctypes
from pathlib import Path
from typing import NewType, List, Optional
from zipfile import ZipFile

import httpx
from nonebot import get_plugin_config
from nonebot.log import logger
from nonebot.adapters.onebot.v11.config import Config

from .http_proxy import get_github_proxy
from ..ntqq import NTQQUpdater, NTQQProcess
from ...config import Driver, PluginConfig
from ...db import SelfIndexPath, DefaultLLOBConfig


LLQQNT_Path = NewType("LLQQNT_Path", Path)
LLOB_DataPath = NewType("LLOB_DataPath", Path)


class LLOBInstaller:
    @staticmethod
    def is_llqqnt_installed():
        """检查是否可能已安装LiteLoaderQQNT"""
        if "LITELOADERQQNT_PROFILE" in os.environ:
            raise ValueError(
                "当前环境变量中存在'LITELOADERQQNT_PROFILE', "
                "你可能已经手动安装过'LiteLoaderQQNT'!"
            )

    @staticmethod
    def is_admin():
        """检查是否为管理员权限"""
        logger.debug("正在检查是否拥有管理员权限...")
        try:
            result = bool(ctypes.windll.shell32.IsUserAnAdmin())
        except Exception:
            result = False
        # 检查结果
        if not result:
            raise ValueError("当前没有管理员权限!")

    @staticmethod
    def is_sys_win64() -> bool:
        """检查操作系统是否为64位"""
        return sys.maxsize > 2 ** 32

    @staticmethod
    async def get_data(client: httpx.AsyncClient, url: str) -> bytes:
        """下载一些数据"""
        res = await client.get(
            url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
            },
            follow_redirects=True
        )
        res.raise_for_status()
        return res.content

    @staticmethod
    def install_llqqnt(zip_data: bytes, ntqq_path: Path) -> LLQQNT_Path:
        """解压LLQQNT并覆写相关文件"""
        up_path = os.getenv("USERPROFILE")
        assert up_path is not None, "无法获取环境变量'USERPROFILE'!"
        up_path = Path(up_path)

        # 写入安装包
        zip_path = up_path/"LiteLoaderQQNT-main.zip"
        with zip_path.open("wb") as f:
            f.write(zip_data)
        # 解压
        logger.debug("正在解压LLQQNT...")
        with ZipFile(file=str(zip_path), mode="r") as f:
            llqqnt_path = up_path/"LiteLoaderQQNT-main"
            f.extractall(path=str(llqqnt_path))
        # 删除压缩包
        logger.debug("解压完成, 删除LLQQNT压缩包...")
        if zip_path.exists():
            os.remove(zip_path)

        # 覆写'index.js'文件
        logger.debug("正在覆写NTQQ文件...")
        index_path = ntqq_path.parent/"resources"/"app"/"app_launcher"/"index.js"
        if not index_path.exists():
            raise FileNotFoundError("'index.js'文件实际不存在!")
        if not index_path.is_file():
            raise ValueError("此路径指向一个非文件!")

        with SelfIndexPath.open("r") as f:
            index_data = f.read()
        with index_path.open("w") as f:
            f.write(index_data)

        # 传递一个路径用于安装LLOB
        return LLQQNT_Path(llqqnt_path)

    @staticmethod
    def install_llob(zip_data: bytes, llqqnt_path: LLQQNT_Path) -> LLOB_DataPath:
        """安装LLOB"""
        if not llqqnt_path.exists():
            raise FileNotFoundError("LLQQNT路径不存在!")

        plugin_path = llqqnt_path/"plugins"
        if not plugin_path.exists():  # 若无plugins目录则创建
            os.mkdir(plugin_path)
        # 写入安装包
        zip_path = plugin_path/"LLOneBot-main.zip"
        with zip_path.open("wb") as f:
            f.write(zip_data)
        # 解压
        logger.debug("正在解压LLOB...")
        with ZipFile(file=str(zip_path), mode="r") as f:
            llob_path = plugin_path/"LLOneBot"
            f.extractall(path=str(llob_path))
        # 删除压缩包
        logger.debug("解压完成, 删除LLOB压缩包...")
        if zip_path.exists():
            os.remove(zip_path)
        # 创建必要目录
        data_path = llqqnt_path/"data"  # 参考'install_llob'项目, 不创建可能会报错
        if not data_path.exists():
            logger.debug("创建LLOB必要目录...")
            os.mkdir(data_path)
        # 检查是否初次安装LLOB
        if not (llob_data_path := data_path/"LLOneBot").exists():
            logger.warning("检测到可能为初次安装LLOB (提示: 安装完成后, 你可能需自行配置LLOB以连接Bot)")
        else:
            logger.info("检测到非初次安装LLOB (提示: 你之前的LLOB配置将被保留)")
        return LLOB_DataPath(llob_data_path)


def auto_llob_setting(llob_data_path: LLOB_DataPath) -> None:
    """自动帮用户配置LLOB, 轮椅坐穿"""
    try:
        assert PluginConfig.lm_llob_first_auto_setting_qqid is not None, "未找到该插件配置!"

        if not llob_data_path.exists():
            logger.debug("创建LLOB必要数据目录...")
            os.mkdir(llob_data_path)

        # 读取默认配置
        logger.debug("正在读取预设配置...")
        with DefaultLLOBConfig.open("r", encoding="utf-8") as f:
            data = json.load(f)

        # 读取nb配置
        host, port = Driver.config.host, Driver.config.port
        ws_url = f"ws://{host}:{port}/onebot/v11/ws"
        ws_hosts: List = data["ob11"]["wsHosts"]
        ws_hosts.append(ws_url)

        if (  # 读取ob11配置
                access_token := get_plugin_config(Config).onebot_access_token
        ) is not None:
            data["token"] = access_token

        # 写入预设配置
        logger.debug("正在自动写入LLOB预设配置...")
        file_path = llob_data_path/f"config_{PluginConfig.lm_llob_first_auto_setting_qqid}.json"
        with file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    except Exception as e:
        logger.error(f"LLOB预设配置写入失败: {e.__class__.__name__}{e.args}")
    else:
        logger.success(
            f"LLOB预设配置已写入, 使用账号({PluginConfig.lm_llob_first_auto_setting_qqid})登录即可连接Bot!"
        )


async def llob_auto_install() -> Optional[LLOB_DataPath]:
    """LLOB自动安装"""
    logger.info("正在自动安装新版本的LLOB...")
    try:
        # 前置检查
        LLOBInstaller.is_llqqnt_installed()  # 检查是否有手动安装LLQQNT痕迹
        LLOBInstaller.is_admin()  # 检查是否为管理员

        ntqq_path = NTQQUpdater.get_path()
        ntqq_bit = "x64" if NTQQUpdater.is_win64(ntqq_path) else "x86"
        # 检测NTQQ是否处于运行状态
        proc_result = NTQQProcess.is_running(ntqq_path)
        if proc_result.action:  # NTQQ处于运行状态则终止
            raise RuntimeError(
                f"检测到NTQQ正在运行, 无法自动安装LLOB"
                f"(进程: {', '.join([f'PID-{pid}' for pid in proc_result.processes])})"
            )
        # 获取GitHub代理
        proxy_url = await get_github_proxy()
        logger.info(
            "无需使用代理即可连接GitHub" if (
                    proxy_url == "https://github.com"
            ) else f"使用代理: {proxy_url}"
        )
        # 下载相关文件
        async with httpx.AsyncClient() as client:
            # 下载修补文件
            logger.debug("正在下载NTQQ修补文件...")
            try:
                ntqq_fvp = await LLOBInstaller.get_data(
                    client,
                    url=f"{proxy_url}/LiteLoaderQQNT/QQNTFileVerifyPatch/"
                        f"releases/latest/download/dbghelp_{ntqq_bit}.dll"
                )
            except Exception as e:
                raise ValueError(f"下载补丁文件失败: {e}")
            else:
                # 覆盖原始文件
                file_path = ntqq_path.parent/"dbghelp.dll"
                if file_path.exists():
                    os.remove(file_path)  # 读写不了你我还删不了你🐴
                with file_path.open("wb") as f:
                    f.write(ntqq_fvp)
                logger.success("NTQQ修补完成!")

            # 下载LLQQNT
            logger.debug("正在下载LLQQNT项目...")
            try:
                llqqnt_zip = await LLOBInstaller.get_data(
                    client,
                    url=f"{proxy_url}/LiteLoaderQQNT/LiteLoaderQQNT/"
                        "releases/latest/download/LiteLoaderQQNT.zip"
                )
            except Exception as e:
                raise ValueError(f"下载LLQQNT项目失败: {e}")
            else:
                # 解压文件并覆写'index.js'文件
                llqqnt_path = LLOBInstaller.install_llqqnt(
                    zip_data=llqqnt_zip, ntqq_path=ntqq_path
                )
                logger.success("LLQQNT安装完成")

            # 下载LLOB
            logger.debug("正在下载LLOB项目...")
            try:
                llob_zip = await LLOBInstaller.get_data(
                    client,
                    url=f"{proxy_url}/LLOneBot/LLOneBot/"
                        f"releases/latest/download/LLOneBot.zip"
                )
            except Exception as e:
                raise ValueError(f"下载LLQQNT项目失败: {e}")
            else:
                # 解压并创建必要目录
                llob_data_path = LLOBInstaller.install_llob(
                    zip_data=llob_zip, llqqnt_path=llqqnt_path
                )

    except Exception as e:
        logger.error(f"安装LLOB失败: {e.__class__.__name__}{e.args}")
    else:
        logger.success(f"自动安装LLOB成功, 享受快乐时光吧!")
        return llob_data_path


__all__ = ["llob_auto_install", "auto_llob_setting"]

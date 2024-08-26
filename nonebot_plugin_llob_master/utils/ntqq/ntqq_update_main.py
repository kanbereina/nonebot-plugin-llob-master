import json
from pathlib import Path
from typing import Dict

from nonebot.log import logger

from .ntqq import NTQQ
from .ntqq_path import NTQQPath
from ...config import PluginConfig
from ...models import NTQQVersion


class NTQQUpdater:
    @staticmethod
    def get_path() -> Path:
        """获取路径"""
        # 开始获取NTQQ路径
        logger.debug("正在尝试从插件配置获取NTQQ路径...")

        try:  # 先尝试插件获取
            return NTQQPath.get_path_by_config()
        except RuntimeError as e:
            logger.warning(e)

            logger.debug("正在尝试从注册表获取NTQQ路径...")
            try:  # 再尝试注册表获取
                return NTQQPath.get_path_by_reg()
            except RuntimeError as e:
                logger.warning(e)
                raise RuntimeError("NTQQ路径获取失败!")

    @staticmethod
    def get_version(ntqq_path: Path) -> NTQQVersion:
        """获取版本"""
        logger.debug("正在检查NTQQ版本...")

        try:
            file_path = ntqq_path.parent/"resources"/"app"/"package.json"
            # 检查文件
            if not file_path.exists():
                raise FileNotFoundError("文件实际不存在!")
            if not file_path.is_file():
                raise ValueError("此路径指向一个非文件!")

            # 读取数据并构建模型
            with file_path.open("r", encoding="utf-8") as file:
                data: Dict = json.loads(file.read())

            version: str = data["version"]
            main_version, build_version = version.split("-")

            return NTQQVersion(main=main_version, build=build_version)
        except Exception as e:
            logger.warning(e)
            raise RuntimeError("NTQQ版本获取失败!")

    @staticmethod
    def is_win64(ntqq_path: Path) -> bool:
        """检查NTQQ位数"""
        logger.debug("正在检查NTQQ位数...")

        try:
            file_path = ntqq_path.parent/"resources"/"app"/"package.json"
            # 检查文件
            if not file_path.exists():
                raise FileNotFoundError("文件实际不存在!")
            if not file_path.is_file():
                raise ValueError("此路径指向一个非文件!")

            with file_path.open("r", encoding="utf-8") as file:
                data: Dict = json.loads(file.read())
            return data["eleArch"] == "x64"
        except Exception as e:
            raise RuntimeError(f"NTQQ位数获取失败: {e.__class__.__name__}{e.args}")


async def ntqq_update_checker() -> Path:
    """NTQQ更新检查"""
    # 本地检查
    ntqq_path = NTQQUpdater.get_path()
    ntqq_version = NTQQUpdater.get_version(ntqq_path)
    ntqq_bit = 64 if (
        result := NTQQUpdater.is_win64(ntqq_path)
    ) else 32
    logger.info(f"当前NTQQ版本: {ntqq_version.main}-{ntqq_version.build} ({ntqq_bit} 位)")

    # 检查是否允许检查NTQQ版本更新
    if PluginConfig.lm_ntqq_update_check:
        logger.debug("正在进行NTQQ更新检查...")
        # 联网检查
        try:
            url = await NTQQ.get_latest_download_url(is_win64=result)
            latest_version = NTQQ.get_latest_version(url)
            # 检查是否有更新
            if NTQQ.check_update(ntqq_version, latest_version):
                logger.info(
                    f"检测到NTQQ有新版本: "
                    f"{ntqq_version.main}-{ntqq_version.build} "
                    f"=> {latest_version.main}-{latest_version.build}"
                )
                logger.warning(f"若要更新, 请手动前往QQ官网下载更新: '{url}'")
            else:
                logger.success("当前NTQQ已为最新版本!")
        except Exception as e:
            logger.error(f"检查NTQQ版本更新失败: {e.__class__.__name__}{e.args}")
    else:
        logger.warning("已关闭'NTQQ更新检查', 跳过该流程")

    return ntqq_path


__all__ = ["ntqq_update_checker", "NTQQUpdater"]

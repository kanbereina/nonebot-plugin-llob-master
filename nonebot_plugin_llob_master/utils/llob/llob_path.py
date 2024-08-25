import os
import json
from pathlib import Path
from typing import NewType, Dict

from nonebot.log import logger


LLQQNT_Path = NewType("LLQQNTPath", Path)
LLOB_Path = NewType("LLOBPath", Path)
LLOB_Version = NewType("LLOBVersion", str)
LLQQNT_Version = NewType("LLQQNT_Version", str)


class LLOBPath:
    @staticmethod
    def get_llqqnt_path() -> LLQQNT_Path:
        """获取LiteLoaderQQNT路径"""
        logger.debug("尝试获取LLQQNT路径...")

        up_path = os.getenv("USERPROFILE")
        assert up_path is not None, "无法获取环境变量'USERPROFILE'!"
        up_path = Path(up_path)
        llqqnt_path = up_path/"LiteLoaderQQNT-main"

        if llqqnt_path.exists():
            return LLQQNT_Path(llqqnt_path)

        raise RuntimeError("获取LLQQNT路径失败, 当前可能未安装LLQQNT!")

    @staticmethod
    def get_llqqnt_version(path: LLQQNT_Path) -> LLQQNT_Version:
        """获取LLQQNT版本"""
        logger.debug("尝试获取LLQQNT版本...")

        try:
            package_path = path/"package.json"
            # 检查文件
            if not package_path.exists():
                raise FileNotFoundError("文件实际不存在!")
            if not package_path.is_file():
                raise ValueError("配置路径指向一个非文件!")

            # 读取数据
            with package_path.open("r", encoding="utf-8") as file:
                data: Dict = json.loads(file.read())
            version: str = data["version"]

            return LLQQNT_Version(version)
        except Exception as e:
            raise RuntimeError(e)

    @staticmethod
    def get_llob_path(path: LLQQNT_Path) -> LLOB_Path:
        """获取LLOB路径"""
        logger.debug("尝试获取LLQQNT路径...")

        llob_path = path/"plugins"/"LLOneBot"

        if llob_path.exists():
            return LLOB_Path(llob_path)

        raise RuntimeError("获取LLOB路径失败, 当前可能未安装LLOB!")

    @staticmethod
    def get_llob_version(path: LLOB_Path) -> LLOB_Version:
        """获取LLOB版本"""
        logger.debug("尝试获取LLOB版本...")

        try:
            manifest_path = path/"manifest.json"
            # 检查文件
            if not manifest_path.exists():
                raise FileNotFoundError("文件实际不存在!")
            if not manifest_path.is_file():
                raise ValueError("配置路径指向一个非文件!")

            # 读取数据
            with manifest_path.open("r", encoding="utf-8") as file:
                data: Dict = json.loads(file.read())
            version: str = data["version"]

            return LLOB_Version(version)
        except Exception as e:
            raise RuntimeError(e)


__all__ = ["LLOBPath", "LLOB_Version"]

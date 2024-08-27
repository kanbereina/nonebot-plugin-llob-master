import asyncio
from pathlib import Path
from typing import Optional

from nonebot.log import logger

from ...config import PluginConfig
from .ntqq_process import NTQQProcess


NTQQ_Process: Optional[NTQQProcess] = None
NTQQ_Path: Optional[Path] = None
IsInstalling: Optional[bool] = False


def is_llob_installing() -> bool:
    """检查是否正在指令安装LLOB"""
    global IsInstalling
    return IsInstalling


def set_llob_install_status(value: bool):
    """设置安装状态"""
    global IsInstalling
    assert IsInstalling is not value, f"当前状态已为'{value}'!"
    IsInstalling = value


def get_ntqq_proc() -> Optional[NTQQProcess]:
    """获取NTQQ进程"""
    global NTQQ_Process
    return NTQQ_Process


def ntqq_start_checker(ntqq_path: Path):
    """初始启动NTQQ"""
    global NTQQ_Process, NTQQ_Path
    NTQQ_Path = ntqq_path

    if PluginConfig.lm_enable_auto_restart:
        logger.info("当前已允许'自动管理NTQQ进程、断连重启', 即将进行任务...")

        ntqq_process = NTQQProcess(ntqq_path)
        if ntqq_process.run():
            NTQQ_Process = ntqq_process
        else:
            logger.error("启动NTQQ进程失败, 请检查日志输出!")

    else:
        logger.warning("当前已禁用'自动管理NTQQ进程、断连重启', 请自行对接Bot!")


async def ntqq_restart():
    """重启NTQQ"""
    global NTQQ_Process, NTQQ_Path
    assert NTQQ_Path is not None, "NTQQ路径为空!"

    # 检查是否在指令安装状态, 若为该状态则直接启动NTQQ
    if not is_llob_installing():
        # 正常断线重连
        assert NTQQ_Process is not None, "进程信息为空!"
        # 关闭进程
        NTQQ_Process.close()
        NTQQ_Process = None

        restart_time = PluginConfig.lm_restart_time
        logger.info(f"将在Bot断连 {restart_time} 秒后尝试重启NTQQ...")
        await asyncio.sleep(restart_time)

    # 启动进程
    ntqq_process = NTQQProcess(NTQQ_Path)
    if ntqq_process.run():
        NTQQ_Process = ntqq_process
    else:
        logger.error("启动NTQQ进程失败, 请检查日志输出!")


__all__ = [
    "ntqq_start_checker", "get_ntqq_proc", "ntqq_restart",
    "set_llob_install_status", "is_llob_installing"
]

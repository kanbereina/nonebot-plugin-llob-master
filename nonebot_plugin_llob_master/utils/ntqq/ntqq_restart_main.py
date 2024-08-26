import asyncio
from pathlib import Path
from typing import Optional

from nonebot.log import logger

from ...config import PluginConfig
from .ntqq_process import NTQQProcess


NTQQ_Process: Optional[NTQQProcess] = None
NTQQ_Path: Optional[Path] = None


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
    assert NTQQ_Process is not None, "进程信息为空!"
    assert NTQQ_Path is not None, "NTQQ路径为空!"

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


__all__ = ["ntqq_start_checker", "get_ntqq_proc", "ntqq_restart"]

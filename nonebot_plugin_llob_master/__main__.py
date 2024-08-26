import asyncio
from datetime import datetime, timedelta

from nonebot.log import logger
from nonebot_plugin_apscheduler import scheduler

from .config import Driver
from .utils import (
    ntqq_update_checker, llob_update_checker, ntqq_start_checker,
    get_ntqq_proc, ntqq_restart
)


@Driver.on_startup
async def start():
    logger.warning("请不要在任何影响力较大的简中互联网平台, 发布和讨论任何与LLOB、本插件存在相关性的信息!")
    # 检查NTQQ版本更新
    ntqq_path = await ntqq_update_checker()
    # 检查LLOB版本更新
    await llob_update_checker()
    # 检查是否可启动NTQQ进程
    ntqq_start_checker(ntqq_path=ntqq_path)


@Driver.on_bot_connect
async def handle_window():
    ntqq_proc = get_ntqq_proc()
    # Bot连接时最小化NTQQ窗口
    if ntqq_proc is not None:
        await ntqq_proc.get_ntqq_hwnd()

        hide_time = 5
        logger.info(f"将在 {hide_time} 秒后最小化NTQQ窗口...")
        await asyncio.sleep(hide_time)  # 防止连接过快窗口未加载完的假最小化

        logger.debug("尝试最小化窗口...")
        await ntqq_proc.hide_window()


@Driver.on_bot_disconnect
async def restart_ntqq():
    ntqq_proc = get_ntqq_proc()
    # Bot断连后数秒后进行重连
    if ntqq_proc is not None:
        scheduler.add_job(  # 防一直处于on_bot_disconnect状态, 并防止shutdown的时候无法立即停止
            ntqq_restart, "date",
            next_run_time=datetime.now() + timedelta(seconds=1)
        )


@Driver.on_shutdown
async def close_ntqq():
    ntqq_proc = get_ntqq_proc()
    # 关闭NTQQ进程
    if ntqq_proc is not None:
        ntqq_proc.close()

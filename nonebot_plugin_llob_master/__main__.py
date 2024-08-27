import asyncio
from time import time
from datetime import datetime, timedelta

from nonebot import on_command
from nonebot.log import logger
from nonebot.params import ArgPlainText
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot_plugin_apscheduler import scheduler

from .config import Driver, PluginConfig
from .utils import (
    ntqq_update_checker, llob_update_checker, ntqq_start_checker,
    get_ntqq_proc, ntqq_restart,
    is_llob_installing, set_llob_install_status
)
# 指令更新
from .utils.llob.llob import LLOB
from .utils.llob.llob_path import LLOBPath
from .utils.llob.llob_install import llob_auto_install


update_llob = on_command(
    "检查更新",
    permission=SUPERUSER, block=True,
    aliases={"检查LLOB更新", "更新LLOB"}
)


@update_llob.handle()
async def check_llob_update(event: MessageEvent):
    await update_llob.send("正在检查更新中，请稍后...")
    logger.info(f"用户(ID: {event.get_user_id()})触发了LLOB版本更新检查, 正在执行任务...")

    try:  # 获取当前LLOB版本信息
        llqqnt_path = LLOBPath.get_llqqnt_path()
        llob_path = LLOBPath.get_llob_path(path=llqqnt_path)
        llob_version = LLOBPath.get_llob_version(path=llob_path)
        logger.info(f"当前LLOB版本: {llob_version}")
    except Exception as e:
        await update_llob.finish(
            f"检查当前LLOB版本失败： {e.__class__.__name__}(\n"
            f"{', '.join(e.args)}\n"
            ")"
        )
        raise e  # 防IDE若智检查

    logger.debug("正在检查LLOB版本更新...")
    try:
        latest_version = await LLOB.get_latest_version(
            api_url="https://api.github.com/repos/LLOneBot/LLOneBot/releases/latest"
        )
    except Exception:
        logger.warning("无法访问GitHub, 尝试使用备用URL")
        try:
            latest_version = await LLOB.get_latest_version(
                api_url="https://api.hydroroll.team/api/version?repo=LLOneBot/LLOneBot&type=github-releases-latest"
            )
        except Exception as e:
            await update_llob.finish(
                f"检查最新LLOB版本失败： {e.__class__.__name__}(\n"
                f"{', '.join(e.args)}\n"
                ")"
            )
            raise e  # 防IDE若智检查

    # 检查是否有更新
    if not LLOB.check_update(llob_version, latest_version):
        await update_llob.finish(f"当前版本(v{llob_version})已为最新！")

    logger.info(f"检测到LLOB有新版本: v{llob_version} => v{latest_version}")
    await update_llob.send(
        "检测到LLOB版本更新：\n"
        f"v{llob_version} => v{latest_version}\n"
        "\n"
        "是否安装此次更新（是/否）:"
    )


@update_llob.got(key="choice")
async def check_choice(event: MessageEvent, choice: str = ArgPlainText()):
    uid = event.get_user_id()

    if choice != "是":
        logger.info(f"用户(ID: {uid})取消安装此次LLOB更新")
        await update_llob.finish("未进行确认，已取消此次操作。")

    logger.info(f"用户(ID: {uid})确认安装此次LLOB更新")

    result = "（已启用“断连重启”，安装完成后将自动重启！）" if (
        PluginConfig.lm_enable_auto_restart
    ) else "（未启用“断连重启”，安装完成后请手动重启！）"
    await update_llob.send(
        "即将安装更新，安装过程中Bot将会下线！\n"
        f"{result}"
    )


@update_llob.handle()
async def install_latest_llob():
    async def wait_for_bot_connect(max_time: int = 20):
        """等待Bot重连"""
        start_time = time()
        while True:
            # 检查是否处于安装状态
            if not is_llob_installing():
                break

            # 检查是否超时
            end_time = time()
            if (end_time - start_time) > max_time:
                raise TimeoutError("等待NTQQ重连失败, 安装LLOB可能未成功!")
            await asyncio.sleep(1)

    # 设置当前指令安装LLOB状态
    set_llob_install_status(value=True)

    # 开始关闭NTQQ进程
    ntqq_process = get_ntqq_proc()
    ntqq_process.close()
    await asyncio.sleep(3)  # 防止假关闭进程

    # 开始安装LLOB
    result = await llob_auto_install() is not None

    if PluginConfig.lm_enable_auto_restart:  # 允许断连重启
        # 重启NTQQ进程
        await ntqq_restart()

        # 等待重连
        await wait_for_bot_connect()
        msg = "更新已完成，Bot已重启。" if result else "更新失败，但Bot正常重启。"
        await update_llob.finish(msg)

    else:
        if result:
            logger.success("安装新版本LLOB成功, 请手动重启NTQQ!")
        else:
            logger.error("安装新版本LLOB失败, 请检查日志输出!")


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
    if is_llob_installing():  # 安装完成
        set_llob_install_status(value=False)  # 还原状态

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

        # 检查是否正在指令更新LLOB, 若为该状态则忽略此次断连重启
        if not is_llob_installing():
            scheduler.add_job(  # 防一直处于on_bot_disconnect状态, 并防止shutdown的时候无法立即停止
                ntqq_restart, "date",
                next_run_time=datetime.now() + timedelta(seconds=1)
            )
        else:
            logger.info("正在指令更新LLOB, 忽略此次断连重启")


@Driver.on_shutdown
async def close_ntqq():
    ntqq_proc = get_ntqq_proc()
    # 关闭NTQQ进程
    if ntqq_proc is not None:
        ntqq_proc.close()

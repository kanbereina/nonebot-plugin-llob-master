import os

from nonebot import require
from nonebot.log import logger
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="LLOneBot-Master",
    description="在Windows上管理你的LLOB，可进行版本更新、断连自动重启。",
    usage="启动时自动检查相关更新、使用指令进行更新、断连自动重启",
    type="application",
    homepage="https://github.com/kanbereina/nonebot-plugin-llob-master",
    config=Config,
    supported_adapters={"~onebot.v11"},
    extra={
        "version": "v1.1.0",
    },
)

require("nonebot_plugin_apscheduler")


# 仅当系统为Windows时插件生效
if os.name == "nt":
    from .__main__ import *  # noqa
else:
    logger.warning("本插件仅能在Windows系统上使用, 已自动禁用插件!")

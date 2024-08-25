from nonebot import require
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
        "version": "v1.0.0",
    },
)

require("nonebot_plugin_apscheduler")

from .__main__ import *  # noqa

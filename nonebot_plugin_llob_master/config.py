from typing import Optional

import nonebot


class Config(nonebot.Config):
    lm_ntqq_path: Optional[str] = None  # NTQQ的.exe文件的路径
    lm_enable_lookup_reg: bool = False  # 允许从注册表查询NTQQ路径
    lm_ntqq_update_check: bool = True  # 允许插件加载时, 检查NTQQ版本更新(只进行提醒)

    lm_llob_update_check: bool = True  # 允许插件加载时, 检查LLOB更新(只进行提醒)
    lm_llob_first_auto_install: bool = True  # 允许插件没有检测到LLOB时(大概率没安装), 自动安装LLOB
    lm_llob_auto_install: bool = False  # 允许插件检测到LLOB有新版本时, 自动安装LLOB
    lm_llob_first_auto_setting_qqid: Optional[int] = None  # (可选)此处填QQ号, 当插件初次安装LLOB时, 自动为你填写一份初始LLOB配置

    lm_enable_auto_restart: bool = False   # 允许插件管理你的NTQQ进程, 并且Bot断连时自动重启NTQQ
    lm_restart_time: Optional[int] = 10  # 在Bot断连的{lm_restart_time}秒后重启NTQQ


Driver = nonebot.get_driver()
# 实例化插件配置
PluginConfig = nonebot.get_plugin_config(Config)


__all__ = ["Config", "PluginConfig", "Driver"]

from nonebot.log import logger

from .llob import LLOB
from .llob_path import LLOBPath
from .llob_install import llob_auto_install, auto_llob_setting
from ...config import PluginConfig


async def llob_update_checker():
    """LLOB更新检查"""
    try:  # 获取当前LLOB版本信息
        llqqnt_path = LLOBPath.get_llqqnt_path()
        llob_path = LLOBPath.get_llob_path(path=llqqnt_path)
        llob_version = LLOBPath.get_llob_version(path=llob_path)
        logger.info(f"当前LLOB版本: {llob_version}")

    except Exception as e:  # 未检测到LLOB版本时(大概率没安装), 则根据设置进行自动安装
        logger.error(f"检查LLOB版本失败: {e.__class__.__name__}{e.args}")
        logger.warning("当前可能未安装LLOB, 尝试自动安装...")

        if PluginConfig.lm_llob_first_auto_install:
            logger.info("当前已启用'初次使用LLOB自动安装', 即将进行任务...")
            llob_data_path = await llob_auto_install()

            if llob_data_path is not None:

                if PluginConfig.lm_llob_first_auto_setting_qqid is not None:
                    logger.info("当前已启用'初次使用LLOB自动配置', 即将进行任务...")
                    auto_llob_setting(llob_data_path=llob_data_path)

                else:
                    logger.warning("当前已禁止'初次使用LLOB自动配置', 跳过配置流程!")

        else:
            logger.warning("当前已禁止'初次使用LLOB自动安装', 跳过安装流程!")

    else:  # 检测到当前LLOB版本时, 则会进行版本更新检查和自动安装
        try:
            # 检查是否允许检查LLOB版本更新
            if PluginConfig.lm_llob_update_check:
                # 联网检查
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
                    except Exception:
                        raise RuntimeError("所有请求均失败, 无法获取LLOB最新版本信息!")

                # 检查是否有更新
                if LLOB.check_update(llob_version, latest_version):
                    logger.info(f"检测到LLOB有新版本: v{llob_version} => v{latest_version}")

                    # 检查是否允许自动安装LLOB
                    if PluginConfig.lm_llob_auto_install:
                        logger.info("当前已启用'LLOB自动安装', 即将进行任务...")
                        await llob_auto_install()
                    else:
                        logger.warning("当前已禁止'LLOB自动安装', 跳过安装流程!")

                else:
                    logger.success("当前LLOB已为最新版本!")

            else:
                logger.warning("已关闭'LLOB更新检查', 跳过检查流程")

        except Exception as e:
            logger.error(f"检查LLOB更新失败: {e.__class__.__name__}{e.args}")


__all__ = ["llob_update_checker"]

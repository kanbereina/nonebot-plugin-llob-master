from typing import Literal

import httpx
from nonebot.log import logger

from .llob_path import LLOB_Version


class LLOB:
    @staticmethod
    async def get_latest_version(
            api_url: Literal[
                "https://api.github.com/repos/LLOneBot/LLOneBot/releases/latest",
                "https://api.hydroroll.team/api/version?repo=LLOneBot/LLOneBot&type=github-releases-latest"
            ]
    ) -> LLOB_Version:
        """获取LLOB最新版本号"""
        logger.debug("正在获取LLOB最新版本号...")
        async with httpx.AsyncClient() as client:
            try:
                res = await client.get(
                    url=api_url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                                      "Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
                    }
                )
                res.raise_for_status()

                version = res.json()["tag_name"]
                if "v" in version:  # 版本号带'v'则删除
                    version = version.replace("v", "")
                return LLOB_Version(version)
            except Exception as e:
                logger.warning(f"请求失败: {e.__class__.__name__}{e.args}")
                raise e

    @staticmethod
    def check_update(
            now_version: LLOB_Version,
            latest_version: LLOB_Version
    ) -> bool:
        """检测LLOB是否有更新"""
        return now_version != latest_version


__all__ = ["LLOB"]

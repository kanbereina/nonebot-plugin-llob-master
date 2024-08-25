from typing import NewType

import httpx
from nonebot.log import logger


TestFile = "/LiteLoaderQQNT/QQNTFileVerifyPatch/releases/download/DllHijack_1.0.8/dbghelp_x64.dll"
GithubProxyList = [
        "https://mirror.ghproxy.com/https://github.com",
        "https://x.haod.me/https://github.com",
        "https://gh.jiasu.in/https://github.com",
        "https://github.com",
]
ProxyURL = NewType("ProxyURL", str)


async def get_github_proxy() -> ProxyURL:
    """获取可用的Github代理"""
    logger.debug("正在获取GitHub代理...")
    async with httpx.AsyncClient() as client:
        for proxy_url in GithubProxyList:
            test_url = proxy_url + TestFile
            try:
                res = await client.get(
                    url=test_url,
                    headers={"User-Agent": "Mozilla/5.0"},
                    follow_redirects=True, timeout=6
                )
                res.raise_for_status()
            except Exception as e:
                logger.debug(f"访问'{test_url}'发生错误: {e.__class__.__name__}{e.args}")
                continue
            else:
                return ProxyURL(proxy_url)
    raise ValueError("获取GitHub代理失败!")


__all__ = ["get_github_proxy"]

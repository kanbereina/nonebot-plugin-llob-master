import re
from typing import NewType

import httpx

from ...models import NTQQVersion


QQ_WIN_URL = "https://im.qq.com/pcqq/index.shtml"
LatestURL = NewType("LatestURL", str)


class NTQQ:
    @staticmethod
    async def get_latest_download_url(is_win64: bool) -> LatestURL:
        """获取最新版NTQQ下载链接"""
        try:
            client = httpx.AsyncClient()

            html = await client.get(url=QQ_WIN_URL)
            html.raise_for_status()

            result = re.findall(r'var rainbowConfigUrl = "(.*)\?t=.*"', html.text)
            assert len(result), "未找到模板变量!"

            res = await client.get(url=result[0])
            res.raise_for_status()
            await client.aclose()

            pattern = r"https://dldir1\.qq\.com/qqfile/qq/QQNT/Windows/QQ_[0-9]+\.[0-9]+\.[0-9]+_[0-9]{6}"
            pattern += r"_x64_[0-9]{2}\.exe" if is_win64 else r"_x86_64_[0-9]{2}\.exe"
            match = re.findall(pattern, res.text)
            assert len(match), "未找到指定版本!"
            return LatestURL(match[0])
        except Exception as e:
            raise RuntimeError(e)

    @staticmethod
    def get_latest_version(url: LatestURL) -> NTQQVersion:
        """获取NTQQ最新版本号"""
        try:
            match = re.findall(
                r"https://dldir1\.qq\.com/qqfile/qq/QQNT/Windows/"
                r"QQ_([0-9]+\.[0-9]+\.[0-9]+_[0-9]{6})_x64_[0-9]{2}\.exe",
                url
            )
            assert len(match), "提取版本失败!"
            main_version, build_version = match[0].split("_")
            return NTQQVersion(main=main_version, build=build_version)
        except Exception as e:
            raise RuntimeError(e)

    @staticmethod
    def check_update(
            now: NTQQVersion,
            latest: NTQQVersion
    ) -> bool:
        """检测NTQQ是否有更新"""
        return (now.main + now.build) != (latest.main + latest.build)


__all__ = ["NTQQ"]

import os
if os.name == "nt":  # 必须为Windos系统
    import winreg
from pathlib import Path

from ...config import PluginConfig


class NTQQPath:
    @staticmethod
    def get_path_by_config() -> Path:
        """从插件配置中获取NTQQ路径"""
        try:
            ntqq_path = Path(PluginConfig.lm_ntqq_path)
            # 检查文件
            if not ntqq_path.exists():
                raise FileNotFoundError("文件实际不存在!")
            if not ntqq_path.is_file():
                raise ValueError("配置路径指向一个非文件!")

            return ntqq_path
        except Exception as e:
            raise RuntimeError(f"从插件配置获取路径失败: {e.__class__.__name__}{e.args}")

    @staticmethod
    def get_path_by_reg() -> Path:
        """从注册表中获取NTQQ路径"""
        try:
            if not PluginConfig.lm_enable_lookup_reg:
                raise ValueError("插件配置已禁止查询注册表!")
            # 从注册表查询位置
            try:
                key = winreg.OpenKey(  # 先采用主项
                    winreg.HKEY_LOCAL_MACHINE,
                    r"Software\Microsoft\Windows\CurrentVersion\Uninstall\QQ"
                )
            except FileNotFoundError:
                key = winreg.OpenKey(  # 未找到该项, 尝试采用备用项
                    winreg.HKEY_LOCAL_MACHINE,
                    r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\QQ"
                )

            # 解析路径
            uninstall_string, _ = winreg.QueryValueEx(key, "UninstallString")
            ntqq_path = Path(
                uninstall_string.replace("Uninstall.exe", "QQ.exe")
            )
            # 检查文件
            if not ntqq_path.exists():
                raise FileNotFoundError("文件实际不存在!")
            if not ntqq_path.is_file():
                raise ValueError("配置路径指向一个非文件!")

            return ntqq_path
        except Exception as e:
            raise RuntimeError(f"从注册表获取路径失败: {e.__class__.__name__}{e.args}")


__all__ = ["NTQQPath"]

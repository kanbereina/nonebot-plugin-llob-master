import ctypes
import os

if os.name == "nt":  # 必须为Windos系统
    from ctypes.wintypes import (
        HWND, BOOL, LPCWSTR, SHORT, INT
    )

# 加载 user32.dll
user32 = ctypes.WinDLL('user32')

# 定义 Windows API 函数 IsWindow
user32.IsWindow.argtypes = [HWND]
user32.IsWindow.restype = BOOL

# 定义 Windows API 函数 IsWindowVisible
user32.IsWindowVisible.argtypes = [HWND]
user32.IsWindowVisible.restype = BOOL

# 定义 Windows API 函数 IsWindowEnabled
user32.IsWindowEnabled.argtypes = [HWND]
user32.IsWindowEnabled.restype = BOOL

# 定义 Windows API 函数 GetClassNameW
user32.GetClassNameW.argtypes = [HWND, LPCWSTR, INT]
user32.GetClassNameW.restype = INT

# 定义 Windows API 函数 ShowWindow
user32.ShowWindow.argtypes = [HWND, SHORT]
user32.ShowWindow.restype = BOOL

# 定义 Windows API 函数 IsIconic
user32.IsIconic.argtypes = [HWND]
user32.IsIconic.restype = BOOL


class win32con:  # noqa
    # 常量
    SW_HIDE = 0
    SW_SHOW = 5
    SW_MINIMIZE = 6
    SW_MAXIMIZE = 3
    SW_RESTORE = 9


class win32gui:  # noqa
    @staticmethod
    def IsWindow(hwnd: HWND) -> bool:  # noqa
        """检查窗口句柄是否有效"""
        return bool(user32.IsWindow(hwnd))

    @staticmethod
    def IsWindowVisible(hwnd: HWND) -> bool:  # noqa
        """检查窗口是否可见"""
        return bool(user32.IsWindowVisible(hwnd))

    @staticmethod
    def IsWindowEnabled(hwnd: HWND) -> bool:  # noqa
        """检查窗口是否可交互"""
        return bool(user32.IsWindowEnabled(hwnd))

    @staticmethod
    def GetClassName(hwnd: HWND) -> str:  # noqa
        """获取窗口的类名"""
        buffer_size = 256
        buffer = ctypes.create_unicode_buffer(buffer_size)
        length = user32.GetClassNameW(hwnd, buffer, buffer_size)
        return buffer.value[:length]

    @staticmethod
    def ShowWindow(hwnd: HWND, command: int) -> bool:  # noqa
        """显示或隐藏窗口"""
        return bool(user32.ShowWindow(hwnd, command))

    @staticmethod
    def IsIconic(hwnd: HWND) -> bool:  # noqa
        """检查窗口是否最小化"""
        return bool(user32.IsIconic(hwnd))


__all__ = ["win32gui", "win32con"]

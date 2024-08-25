import ctypes
import os
if os.name == "nt":  # 必须为Windos系统
    from ctypes import wintypes


def get_hwnd_list_by_pid(pid: int):
    """获取该进程下所有窗口句柄"""
    # 定义回调函数类型
    WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)

    # 加载 user32 DLL
    user32 = ctypes.WinDLL('user32')

    # 设置 EnumWindows 函数参数类型和返回值类型
    user32.EnumWindows.argtypes = [WNDENUMPROC, wintypes.LPARAM]
    user32.EnumWindows.restype = wintypes.BOOL

    # 设置 GetWindowThreadProcessId 函数参数类型和返回值类型
    user32.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
    user32.GetWindowThreadProcessId.restype = wintypes.DWORD

    # 存储窗口句柄的列表
    windows_list = []

    # 回调函数
    def enum_windows_callback(hwnd, l_param):
        target_pid = l_param
        process_id = wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(process_id))
        if process_id.value == target_pid:
            windows_list.append(hwnd)
        return True  # 返回 True 继续枚举

    # 创建回调函数对象
    callback = WNDENUMPROC(enum_windows_callback)

    # 调用 EnumWindows 函数
    if not user32.EnumWindows(callback, pid):
        raise RuntimeError("EnumWindows failed")

    return windows_list


__all__ = ["get_hwnd_list_by_pid"]

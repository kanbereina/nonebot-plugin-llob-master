import os
import asyncio
import subprocess
from pathlib import Path
from typing import Optional, List
from time import time

import psutil
from nonebot.log import logger

if os.name == "nt":  # 必须为Windos系统
    from ctypes.wintypes import HWND
    from ..win32api import win32process, win32gui, win32con
from ...models import ProcessResult


class NTQQProcess:
    def __init__(self, ntqq_path: Path):
        self.path = ntqq_path
        self.process: Optional[psutil.Process] = None
        self.hwnd_list: Optional[List[HWND]] = None

    def run(self) -> bool:
        """启动NTQQ"""
        logger.debug("正在启动NTQQ...")

        try:
            # 先检查是否已经运行过NTQQ
            proc_result = NTQQProcess.is_running(self.path, is_installing=False)
            if proc_result.action:
                raise ValueError(
                    f"检测到NTQQ正在运行, 无法继续启动NTQQ"
                    f"(进程: {', '.join([f'PID-{pid}' for pid in proc_result.processes])})"
                )

            pid = subprocess.Popen(
                self.path,
                cwd=self.path.parent, shell=False,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            ).pid
            self.process = psutil.Process(pid)

            logger.success(f"启动NTQQ成功, 当前进程: {pid}")
            return True

        except Exception as e:
            logger.error(f"启动NTQQ失败: {e.__class__.__name__}{e.args}")
            return False

    @staticmethod
    def _find_window_by_class(pid: int, class_name: str) -> Optional[List[int]]:
        """以窗口类名寻找指定窗口句柄"""
        windows = win32process.GetHWNDListByPID(pid)
        hwnd_list = []
        for hwnd in windows:
            if win32gui.IsWindow(hwnd):  # 是窗口
                if win32gui.IsWindowVisible(hwnd):  # 窗口可见
                    if win32gui.IsWindowEnabled(hwnd):  # 窗口可交互
                        if win32gui.GetClassName(hwnd) == class_name:  # 窗口类名特定
                            hwnd_list.append(hwnd)
        return hwnd_list if len(hwnd_list) else None

    async def get_ntqq_hwnd(self, max_time: int = 7) -> List[int]:
        """获取NTQQ窗口指定句柄直到超时"""
        start_time = time()
        try:
            while True:
                result = NTQQProcess._find_window_by_class(
                    pid=self.process.pid, class_name="Chrome_WidgetWin_1"
                )
                if result is not None:
                    self.hwnd_list = result
                    logger.debug(
                        f"成功获取NTQQ窗口句柄(ID: {', '.join([str(i) for i in result])})")
                    return result

                # 检查是否超时
                end_time = time()
                if (end_time - start_time) > max_time:
                    raise TimeoutError("已达到最大重试时间!")

                await asyncio.sleep(0)
        except Exception as e:
            logger.error(f"获取NTQQ窗口句柄失败: {e.__class__.__name__}{e.args}")

    async def hide_window(self, max_time: int = 14):
        """请求窗口最小化直到超时"""
        try:
            start_time = time()

            while True:
                assert self.hwnd_list is not None, "当前没有获取到窗口句柄!"

                try:
                    for hwnd in self.hwnd_list:
                        while True:
                            if win32gui.IsWindowEnabled(hwnd):  # 窗口激活
                                win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)  # 最小化
                                win32gui.ShowWindow(hwnd, win32con.SW_HIDE)  # 最小化并隐藏任务栏
                            else:
                                logger.warning(f"窗口(ID: {hwnd})未激活, 可能是一个无效的窗口句柄!")
                                raise ValueError

                            if win32gui.IsIconic(hwnd):  # 窗口完成最小化
                                logger.success(f"成功最小化窗口(ID: {hwnd})")
                                break

                            # 检查是否超时
                            end_time = time()
                            if (end_time - start_time) > max_time:
                                raise TimeoutError("已达到最大重试时间!")

                            await asyncio.sleep(0.5)
                    else:
                        break
                except ValueError:
                    # 重置窗口句柄
                    await self.get_ntqq_hwnd()

        except Exception as e:
            logger.error(f"隐藏NTQQ窗口失败: {e.__class__.__name__}{e.args}")

    def close(self):
        """关闭NTQQ进程"""
        try:
            assert self.process is not None, "当前没有可关闭的NTQQ进程!"
            self.process.kill()
            logger.success(f"关闭NTQQ进程(PID: {self.process.pid})成功")
        except Exception as e:
            logger.error(f"关闭NTQQ进程失败: {e.__class__.__name__}{e.args}")

    @staticmethod
    def is_running(ntqq_path: Path, is_installing: bool = True) -> ProcessResult:
        """检查当前工作路径的程序是否运行"""
        proc_list = list()
        for proc in psutil.process_iter():
            try:
                # 检查进程名称()
                if (proc.name() == "QQ.exe") and (proc.parent().name() != "QQ.exe"):
                    # 检查工作路径
                    if Path(proc.cwd()) == ntqq_path.parent:
                        proc_list.append(proc.pid)
                    else:
                        logger.warning(
                            f"检测到未知NTQQ进程(PID: {proc.pid})正在运行 "
                            "(提示: 若现在启动你配置路径的NTQQ, "
                            f"可能导致{'安装' if is_installing else '当前NTQQ启动'}不正常!)"
                        )
            except Exception as e:
                logger.warning(
                    f"检查进程'{proc.name()}(PID: {proc.pid})'时"
                    f"发生错误: {e.__class__.__name__}{e.args}"
                )
                continue

        return ProcessResult(
            action=bool(
                len(proc_list)
            ),
            processes=proc_list
        )


__all__ = ["NTQQProcess"]

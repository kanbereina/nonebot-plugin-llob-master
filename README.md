<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# LLOneBot-Master

_✨ 在Windows上无🧠管理你的LLOB！ ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/kanbereina/nonebot-plugin-llob-master.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-llob-master">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-llob-master.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="python">

</div>

> [!WARNING]
> 仅 **Windows系统** 可使用本插件！！！

> [!NOTE]
> 推荐在 **Windows10或更高版本** 或 **Windows Sever 2019或更高版本** 使用此插件。

## 🎀支持功能

- [x] 检查NTQQ更新
- [x] 检查LLOB更新
- [x] 自动安装LLOB
- [x] 自动配置LLOB
- [x] 断连重启NTQQ

## 📖 介绍

本插件可帮助小白 **用Windows系统一键安装LLOneBot** 并 **对接NoneBot** ，
<br>
每次启动NoneBot时还可以 **自动检查LLOB版本更新并自动安装** 。

不仅如此，上述流程结束后，
<br>
本插件还可以 **自动管理NTQQ进程 (启动NTQQ、重启NTQQ)** ，

当你的NTQQ**登录过期**时，本插件会**自动重启NTQQ**以连接你的Bot！
<br>

> [!WARNING]
> **断连重启** 只适用于**NTQQ登录过期**的情况（此情况仍旧**可以重启后正常登录**）
> 
> 对于其他情况（包括但不限于**账号冻结、版本过低**），**无法提供有效的解决方案** !

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-llob-master

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-llob-master
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-llob-master
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-llob-master
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-llob-master
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot-plugin-llob-master"]

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| LM_NTQQ_Path | 否 | None | NTQQ的.exe文件的路径 |
| LM_Enable_LookUp_Reg | 否 | False | 允许从注册表查询NTQQ路径 |
| LM_NTQQ_Update_Check | 否 | True | 允许插件加载时, 检查NTQQ版本更新 (只进行提醒) |
> [!NOTE]
> 当插件检测不到配置中“NTQQ路径”时，<br>
> 会根据配置中是否“允许查询注册表”，再次从注册表查询NTQQ路径
> 
> （适用于默认选项安装NTQQ的情况）

## 🎉 使用
### 指令表
| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| 指令1 | 主人 | 否 | 私聊 | 指令说明 |
| 指令2 | 群员 | 是 | 群聊 | 指令说明 |
### 效果图
如果有效果图的话

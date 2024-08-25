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

> [!CAUTION]\
> **请不要在任何影响力较大的简中互联网平台（包括但不限于哔哩哔哩），发布和讨论*任何*与LLOB、本插件存在相关性的信息！**

> [!WARNING]
> 仅 **Windows系统** 可使用本插件！！！

> [!IMPORTANT]
> 推荐在 **Windows10或更高版本** 或 **Windows Sever 2019或更高版本** 使用此插件。

## 🎀功能

- [x] 检查NTQQ更新
- [x] 检查LLOB更新
- [x] 自动安装LLOB
- [x] 自动配置LLOB
- [x] 断连重启NTQQ
- [ ] 指令更新LLOB

> [!NOTE]
> 因**指令更新**和钩子函数有些冲突需要解决，预计**下个版本会支持该功能**

## 📖 介绍

本插件可帮助小白 **用Windows系统一键安装LLOB** 并 **对接NoneBot** ，
<br>
每次启动NoneBot时，还可 **自动检查LLOB版本更新并自动安装** ,
<br>
 以及 **自动管理NTQQ进程 (启动、断连重启)** 。

> [!WARNING]
> **断连重启** 只适用于**登录过期**的情况（此情况仍旧**可以正常登录**）
> 
> 对于其他情况，**无法提供有效的解决方案** !

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

### NTQQ相关

| 配置项 | 必填 | 类型 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| LM_NTQQ_Path | 否 | str | **None** | NTQQ的.exe文件的路径 |
| LM_Enable_LookUp_Reg | 否 | bool | **False** | 允许从注册表查询NTQQ路径 |
| LM_NTQQ_Update_Check | 否 | bool | **True** | 允许插件加载时, 检查NTQQ版本更新 (只进行提醒) |

> [!NOTE]
> 当插件检测不到配置中“NTQQ路径”时，<br>
> 会根据配置中是否“允许查询注册表”，再次从注册表查询NTQQ路径。
> 
> （适用于默认安装NTQQ的情况）

### LLOB相关

| 配置项 | 必填 | 类型 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| LM_LLOB_Update_Check | 否 | bool | **True** | 允许插件加载时, 检查LLOB更新(只进行提醒) |
| LM_LLOB_First_Auto_Install | 否 | bool | **True** |  允许插件没有检测到LLOB时(大概率没安装), 自动安装LLOB |
| LM_LLOB_Auto_Install | 否 | bool | **False** | 允许插件检测到LLOB有新版本时, 自动安装LLOB |
| LM_LLOB_First_Auto_Setting_QQID | 否 | int | **None** | (可选)此处填QQ号, 当插件初次安装LLOB时, 自动为你填写一份初始LLOB配置，NTQQ启动并登录该QQ号时，可直接连接Bot |

> [!NOTE]
> 启用“检查LLOB更新”才能激活后面的功能(自动安装、配置)
>
> 若你初次安装使用LLOB，可在“LM_LLOB_First_Auto_Setting_QQID”填上自己的账号,<br>
> 在安装完成后，启动程序并登录该账号，预设配置会直接生效，连接上Bot。

### 断连重启相关

| 配置项 | 必填 | 类型 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| LM_Enable_Auto_Restart | 否 | bool | **False** | 允许插件管理你的NTQQ进程, 并且Bot断连时自动重启NTQQ |
| LM_Restart_Time | 否 | int | **10** |  在Bot断连的 {LM_Restart_Time} 秒后重启NTQQ |

> [!NOTE]
> 允许“自动重启”会让插件自动管理NTQQ进程，<br>
> NTQQ、LLOB更新检查完之后，若允许“自动重启”，会自动启动NTQQ，
> 若Bot断连，则会自动重启NTQQ。

> [!WARNING]
> **断连重启** 只适用于**登录过期**的情况（此情况仍旧**可以正常登录**）
> 
> 对于其他情况，**无法提供有效的解决方案** !

## 🎇鸣谢

- [install_llob](https://github.com/super1207/install_llob)
- [LLOneBot](https://github.com/LLOneBot/LLOneBot)
- [LiteLoaderQQNT](https://github.com/LiteLoaderQQNT/LiteLoaderQQNT)
- [QQNTFileVerifyPatch](https://github.com/LiteLoaderQQNT/QQNTFileVerifyPatch)

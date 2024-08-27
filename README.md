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
> **请不要在任何影响力较大的简中互联网平台（包括但不限于哔哩哔哩、抖音），发布和讨论*任何*与LLOB、本插件存在相关性的信息！**

> [!WARNING]
> 仅 **Windows系统** 可使用本插件！！！

> [!IMPORTANT]
> 推荐在 **Windows10或更高版本** 或 **Windows Sever 2019或更高版本** 使用此插件。

> [!NOTE]
> 觉得好用的话，就**给个⭐Star**吧！

## 🎀功能

- [x] 检查NTQQ更新
- [x] 检查LLOB更新
- [x] 自动安装LLOB
- [x] 自动配置LLOB
- [x] 断连重启NTQQ
- [x] 指令更新LLOB

## 📖 介绍

本插件可帮助小白 **用Windows系统一键安装LLOB** 并 **对接NoneBot** ，
<br>
每次启动NoneBot时，还可 **自动检查LLOB版本更新并自动安装** ,
<br>
 以及 **自动管理NTQQ进程 (启动、断连重启)** 。

<br>

---

<br>

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

<br>

---

<br>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

### NTQQ相关

| 配置项 | 必填 | 类型 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| LM_NTQQ_Path | 否 | str | **None** | NTQQ的.exe文件的路径 |
| LM_Enable_LookUp_Reg | 否 | bool | **False** | 允许从注册表查询NTQQ路径 |
| LM_NTQQ_Update_Check | 否 | bool | **True** | 允许插件加载时, 检查NTQQ版本更新 (只进行提醒) |

### LLOB相关

| 配置项 | 必填 | 类型 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| LM_LLOB_Update_Check | 否 | bool | **True** | 允许插件加载时, 检查LLOB更新(只进行提醒) |
| LM_LLOB_First_Auto_Install | 否 | bool | **True** |  允许插件没有检测到LLOB时(大概率没安装), 自动安装LLOB |
| LM_LLOB_Auto_Install | 否 | bool | **False** | 允许插件检测到LLOB有新版本时, 自动安装LLOB |
| LM_LLOB_First_Auto_Setting_QQID | 否 | int | **None** | (可选)此处填QQ号, 当插件初次安装LLOB时, 自动为你填写一份初始LLOB配置，NTQQ启动并登录该QQ号时，可直接连接Bot |

### 断连重启相关

| 配置项 | 必填 | 类型 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| LM_Enable_Auto_Restart | 否 | bool | **False** | 允许插件管理你的NTQQ进程, 并且Bot断连时自动重启NTQQ |
| LM_Restart_Time | 否 | int | **10** |  在Bot断连的 {LM_Restart_Time} 秒后重启NTQQ |

<br>

---

<br>

## 🎉指令更新
| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| **检查更新** | **超级用户**（机器人管理员） | 否 | 私聊/群聊 | 指令别名：**更新LLOB**、**检查LLOB更新** |

> [!WARNING]
> 使用**指令更新**需要**已经安装了LLOB**才能正常使用!

> [!IMPORTANT]
> 启用**自动管理NTQQ进程**以及**配置NTQQ登录设置**，**指令更新LLOB**效果会更好！

<br>

---

<br>

## 🌷如何上手LLOneBot-Master？

> [!IMPORTANT]
> 此处已假设你**已经安装NoneBot2、FastAPI驱动器、OneBotV11适配器**，<br>
> 如果上述未安装，请先参考[NoneBot2官方文档](https://nonebot.dev/docs/2.3.2/tutorial/application)进行安装!<br>
> 此处一并假设你**已经安装成功本插件**！

<br>
<br>

### Part.1 设置nonebot
在 nonebot2 项目的<kbd>.env</kbd>文件中设置<kbd>监听IP</kbd>和<kbd>端口</kbd>，例如：
  
    HOST=0.0.0.0 # 配置 NoneBot 监听的 IP / 主机名
    PORT=8080  # 配置 NoneBot 监听的端口

<br>
<br>

### Part.2 设置LLOneBot-Master配置
  
请在 nonebot2 项目的<kbd>.env</kbd>文件中进行配置：
<br>
**（“⚠”代表必选，“👍”代表推荐选择）**

<br>

⚠**①配置你的NTQQ路径**
<br>
**方法一** (使用指定路径下的NTQQ)：

    LM_NTQQ_Path="C:\Users\Administrator\Desktop\QQNT\QQ.exe"  # 此处替换成你的路径

**方法二：** (使用系统默认安装的NTQQ)：

    LM_Enable_LookUp_Reg=True  # 直接查询注册表获取NTQQ路径 (可不填，默认False)

> [!NOTE]
> 当插件检测不到配置中“NTQQ路径”时，<br>
> 会根据配置中是否“允许查询注册表”，再次从注册表查询NTQQ路径。
> 
> （查询注册表适用于用默认安装的NTQQ的情况）

---

**(可选) ②启动时检查NTQQ更新：**

    LM_NTQQ_Update_Check=True  # 设置为'False'则关闭 (默认True)

---

👍**③启动时检查LLOB更新：**

    LM_LLOB_Update_Check=True  # 设置为'False'则关闭 (默认True)

> [!NOTE]
> 启用“检查LLOB更新”才能激活后面的功能(自动安装、配置)
>
> 若你初次安装使用LLOB，可在“LM_LLOB_First_Auto_Setting_QQID”填上自己的账号,<br>
> 在安装完成后，启动程序并登录该账号，预设配置会直接生效，连接上Bot。

**(可选) ④检测到LLOB更新时，自动安装新版本：**

    LM_LLOB_Auto_Install=True  # 设置为'False'则关闭 (可不填，默认False)

👍**⑤(可选) 没有检测到LLOB时，自动安装LLOB：**

    LM_LLOB_First_Auto_Install=True  # 设置为'False'则关闭 (可不填，默认True)

👍**⑥(可选) 没有检测到LLOB时，自动安装LLOB后，自动生成LLOB配置（登录该账号即可直接连接Bot）：**

    LM_LLOB_First_Auto_Setting_QQID=<要登录的账号>  # 填整数，直接替换“<要登录的账号>”的字符 (可不填，默认None)

---

👍**⑦自动管理NTQQ进程，并在Bot断连时重启进程：**

    LM_Enable_Auto_Restart=True  # 设置为'False'则关闭 (可不填，默认False)

> [!NOTE]
> NTQQ、LLOB更新检查完之后，若允许“自动管理NTQQ进程”，会自动启动NTQQ，
> 若Bot断连，则会自动重启NTQQ。

> [!WARNING]
> **断连重启** 只适用于**登录过期**的情况（此情况仍旧**可以正常登录**）
> 
> 对于其他情况（包括不限于**账号封禁**），**无法提供有效的解决方案** !

**(可选) ⑧断连时经过多少秒重启NTQQ：**

    LM_Restart_Time=10  # (可不填，默认10秒)

<br>
<br>

### Part.3 启动，实战！

> [!IMPORTANT]
> 🤓☝️️此处假设我是一个小白

①**很久以前，有一个小白，他在 nonebot2 项目的<kbd>.env</kbd>文件配置如下：**

    # NoneBot的配置
    
    DRIVER=~fastapi
    HOST=0.0.0.0  # 配置 NoneBot 监听的 IP / 主机名
    PORT=8080  # 配置 NoneBot 监听的端口
    COMMAND_START=["/", ""]  # 配置命令起始字符
    COMMAND_SEP=[" "]  # 配置命令分割字符
    SUPERUSERS=["114514"]  # 小白的账号

    
    # LLOneBot-Master的配置
    
    LM_NTQQ_Path = "C:\Users\Administrator\Desktop\QQNT\QQ.exe"
    LM_LLOB_Auto_Install = True
    LM_LLOB_First_Auto_Install=True
    LM_LLOB_First_Auto_Setting_QQID = 114514  # 小白的账号
    LM_Enable_Auto_Restart=True

②**配置完毕，小白启动了NoneBot！**

![LLOneBot-Master运行-图片示例](https://github.com/kanbereina/nonebot-plugin-llob-master/blob/master/doc/img/start_llob_master.png)

> [!NOTE]
> 看！小白只是启动了NoneBot，其他事**压根不用做**！<br>
> 剩下的事只是**动动手指，登录配置的账号**，就能**连接Bot**啦！

③**小白打开了NTQQ的设置，启用了这些选项！**

![NTQQ配置-图片示例](https://github.com/kanbereina/nonebot-plugin-llob-master/blob/master/doc/img/ntqq_setting.png)

> [!IMPORTANT]
> 咦？小白**为什么要设置这些呢？** <br>
> ！！！<br>
> 原来，这样就可以让插件**更好管理NTQQ**，实现**自动登录、断连重启**啦！<br>

④**小白不信邪，非要测试下断连重启！**

![断连重启-图片示例](https://github.com/kanbereina/nonebot-plugin-llob-master/blob/master/doc/img/ntqq_disconnect.png)

<br>

⑤**小白的故事结束了，你觉得LLOneBot-Master的表现如何呢？**

<br>

**看到这里，也别忘记👇👇👇**
> [!CAUTION]\
> **请不要在任何影响力较大的简中互联网平台（包括但不限于哔哩哔哩、抖音），发布和讨论*任何*与LLOB、本插件存在相关性的信息！**

<br>

---

<br>

## 🎇鸣谢

- [install_llob](https://github.com/super1207/install_llob)
- [LLOneBot](https://github.com/LLOneBot/LLOneBot)
- [LiteLoaderQQNT](https://github.com/LiteLoaderQQNT/LiteLoaderQQNT)
- [QQNTFileVerifyPatch](https://github.com/LiteLoaderQQNT/QQNTFileVerifyPatch)

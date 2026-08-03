# PeekPassword

> Windows平台密码输入监控工具 —— 实时记录文本框输入 + 自动截图

[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-blue?logo=windows)](https://www.microsoft.com/windows)
[![PyInstaller](https://img.shields.io/badge/PyInstaller-6.0+-black)](https://pyinstaller.org/)

---

## 📖 项目简介

**PeekPassword** 是一款运行于 Windows 平台的安全监控小工具，专为**调试场景**和**安全测试**设计。它能够实时检测系统前台窗口中的密码输入框，记录用户输入的文本内容，并在特定场景下自动截取屏幕画面。

> ⚠️ **重要声明**：本工具仅供安全测试、调试分析和授权审计使用。请勿将其用于非法目的，使用者须遵守当地法律法规并承担全部责任。

项目针对**火绒安全软件**的密码输入框进行了特殊优化，在检测到火绒相关窗口时，会同时记录文本输入和屏幕截图，方便安全研究人员进行问题排查和功能验证。

---

## ✨ 功能特性

| 功能模块            | 描述                                                                   |
| ------------------- | ---------------------------------------------------------------------- |
| 🔍 **实时输入检测** | 通过 Windows API 持续监控前台窗口，精准识别密码输入框的变化            |
| 📝 **文本记录**     | 自动捕获编辑控件（Edit Control）中的文本内容，记录父窗口标题和类名信息 |
| 📸 **自动截图**     | 针对特定窗口（如火绒密码框）自动截取全屏画面，保存为 BMP 文件          |
| 🎯 **目标窗口识别** | 支持通过窗口类名关键字过滤目标编辑框，提高检测精度                     |
| ⚙️ **灵活配置**     | 通过 JSON5 配置文件调整检测长度、频率、目标类名等参数                  |
| 🖥️ **后台静默运行** | 采用守护线程设计，资源占用极低，适合长时间运行                         |
| 📋 **彩色日志输出** | 控制台和文件双通道日志，支持彩色输出，便于实时查看                     |
| 📦 **单文件打包**   | 支持 PyInstaller 打包为独立 EXE 文件，无需 Python 环境即可运行         |

---

## 🛠️ 技术栈

| 类别            | 技术                       |
| --------------- | -------------------------- |
| **核心语言**    | Python 3.8+                |
| **Windows API** | ctypes + user32/gdi32      |
| **日志系统**    | colorlog（彩色控制台输出） |
| **配置管理**    | JSON5（支持注释）          |
| **打包工具**    | PyInstaller                |
| **进程管理**    | threading + Win32 Mutex    |

---

## 🚀 快速开始

### 前置条件

- Windows 7/10/11 操作系统
- Python 3.8+（如需源码运行）
- 管理员权限（部分窗口需要）

### 安装步骤

```bash
# 1. 克隆项目
git clone https://github.com/yangsongh/PeekPassword.git
cd PeekPassword

# 2. 创建并激活虚拟环境 (推荐)
python -m venv .venv
.venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt
```

### 基本使用

```bash
python src/main.py
```

### 运行效果

启动后，工具将在后台持续监控，控制台输出示例：

```
[2026-08-03 16:00:00] INFO 开始检测输入框(目标长度<=30, 检测频率33次/秒, 目标类名关键字Edit)...
[2026-08-03 16:00:05] DEBUG [['Edit', 123456, '火绒安全-密码保护', 'ATL:00']]
[2026-08-03 16:00:05] INFO 文本输入框(父标题[火绒安全-密码保护] 父类名[ATL:00] 类名[Edit] 句柄[123456])
******
[2026-08-03 16:00:05] INFO 截图已保存到: screenshots/20260803_160005.bmp
```

---

## 📁 项目结构

```
PeekPassword/
├── src/                       # 📂 源代码目录
│   ├── main.py                # 🚀 入口文件：核心逻辑与窗口检测
│   └── utils/                 # 🛠️ 工具模块
│       ├── utils_lib.py       # 通用工具（日志/配置/系统辅助）
│       └── capture_screen.py  # 📸 屏幕截图模块（基于Windows GDI）
├── build/                     # 📦 打包输出目录
│   ├── config.jsonc           # ⚙️ 配置文件（支持注释）
│   └── PeekPassword.exe       # 🖥️ 可执行程序
├── .vscode/                   # 🔧 VS Code 工作区配置
│   ├── launch.json            # 调试启动配置
│   └── settings.json          # 编辑器设置
├── BUILD.BAT                  # 打包脚本
├── PeekPassword.spec          # PyInstaller 规格文件
├── requirements.txt           # 📦 Python 依赖
└── LICENSE                    # 📄 MIT 许可证
```

---

## ⚙️ 配置说明

配置文件位于 `build/config.jsonc`（打包模式）或项目根目录（开发模式），采用 JSON5 格式（支持注释）：

```jsonc
{
  // 目标密码长度阈值（仅记录长度 <= 此值的文本）
  "target_len": 30,

  // 检测间隔（秒）—— 0 表示无限频率
  "detect_sleep": 0.03,

  // 目标编辑框类名关键字（用于过滤窗口）
  "class_keyword": "Edit",
}
```

### 配置参数详解

| 参数            | 类型   | 默认值   | 描述                                                       |
| --------------- | ------ | -------- | ---------------------------------------------------------- |
| `target_len`    | int    | 30       | 仅记录长度不超过此值的文本，避免捕获大段内容               |
| `detect_sleep`  | float  | 0.03     | 检测循环间隔（秒），值越小检测频率越高，CPU 占用也越高     |
| `class_keyword` | string | `"Edit"` | 编辑框类名包含此关键字时才会被捕获（如 `"Edit"`、`"ATL"`） |

---

## 🔧 核心 API

### `detect_editbox_input(target_len, detect_sleep, class_keyword)`

持续检测密码输入框的主循环函数。

**参数：**

- `target_len` (`int`)：目标文本长度阈值
- `detect_sleep` (`float`)：检测间隔（秒）
- `class_keyword` (`str`)：窗口类名过滤关键字

**说明：**

函数会通过 Windows API 枚举前台窗口中的所有子控件，识别匹配类名的编辑框，并记录文本变化。当检测到父类名包含 `ATL:00`（火绒窗口特征）时，自动触发截图。

---

### `capture_screen(filename)`

截取全屏并保存为 BMP 格式图片。

**参数：**

- `filename` (`str`)：保存路径

**返回值：**

- `bool`：截图成功返回 `True`，失败返回 `False`

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 代码规范

- 使用 PEP 8 代码风格
- 所有新增函数需包含 docstring
- Windows API 调用需添加详细注释说明
- 提交前请确保代码在 Windows 环境下可正常运行

### 提交 Pull Request

1. Fork 本项目到你的仓库
2. 创建新的功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开 Pull Request，清晰描述改动内容和目的

---

## ⚠️ 免责声明

**PeekPassword 仅供安全研究、调试测试和授权审计使用。**

使用者须遵守所在国家/地区的法律法规，并自行承担使用本软件所带来的一切风险与责任。**开发者不对任何滥用行为导致的后果承担任何直接或间接责任。**

请勿将本工具用于：

- 未经授权的信息窃取
- 恶意软件行为
- 侵犯他人隐私

---

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

---

## 🙏 致谢

- [colorlog](https://github.com/borntyping/python-colorlog) - 彩色控制台日志输出
- [PyInstaller](https://pyinstaller.org/) - Python 应用打包工具
- 微软 Windows SDK - Windows API 技术支持

---

## 📮 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 [GitHub Issue](https://github.com/yangsongh/PeekPassword/issues)
- 邮件联系：18675864731@163.com

---

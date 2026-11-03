# auto-tool

个人自动化测试工具集。结构对齐学习参考仓库 `automation-toolkit/`（DUElost 克隆，**不纳入本仓**）。

> 公开仓库请注意脱敏（Token / 内网地址 / 账号口令等）。

## 目录结构

```
D:\auto-tool\
├── automation-toolkit/     # [忽略] DUElost 克隆，只读学习
├── python-tools/           # Python 工具（主阵地）
├── windows-tools/          # Windows 专属
├── linux-tools/            # Linux 专属
├── macos-tools/            # macOS 专属
├── android-tools/          # Android 工具
├── shared/python-utils/    # 跨工具共享库
├── docs/                   # 全景文档（权威来源）
├── AGENTS.md               # AI / 协作最小契约
└── README.md
```

## 已收录工具

| 工具 | 说明 |
|------|------|
| [check_language&country_list](python-tools/check_language&country_list/) | OOBE/设置 语言与国家列表核对（与 Excel 基准比对） |

## 工具命名（学习自 automation-toolkit）

| 前缀 | 含义 | 示例 |
|------|------|------|
| `stability_` | 稳定性 | `stability_Start-Log-Scan` |
| `performance_` | 性能 | `performance_SMT_ResultFiller` |
| `universal_` | 通用流程 | `universal_Factory-Reset` |
| `system_` | 系统侧 | `system_MemoryFusion` |

目录放在对应语言分类下，例如：`python-tools/stability_Start-Log-Scan/`。

## 快速开始

```powershell
cd D:\auto-tool

# 查看入库流程与规范
notepad docs\project-guide.md
notepad docs\onboarding.md

# 新工具脚手架（复制模板）
Copy-Item -Recurse python-tools\_template python-tools\stability_Your-Tool-Name
```

## 与 DUElost 仓库的关系

| 路径 | 用途 |
|------|------|
| `automation-toolkit/` | 官方/同事工具集克隆，对照实现与文档风格 |
| 本仓其余目录 | 你自己维护并推送到 Hasadeh/auto-tool 的代码 |

## 上传前检查清单

见 [`docs/onboarding.md`](docs/onboarding.md)。

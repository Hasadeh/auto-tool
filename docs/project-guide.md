# auto-tool 项目指南

> 个人自动化工具集本地仓  
> 版本：见根目录 `VERSION`  
> 本文档是全景信息的权威来源；`AGENTS.md` / `CLAUDE.md` 只链接、不镜像。

---

## 变更记录

| 日期 | 变更内容 |
|------|----------|
| 2026-11-03 | 收录 `python-tools/check_language&country_list`（语言/国家列表核对） |
| 2026-11-03 | 初始化本地仓骨架：目录分类、入库规范、脱敏清单；`automation-toolkit/` 作只读学习参考 |

---

## 项目愿景

1. **统一落盘**：个人开发的测试工具集中到 `D:\auto-tool`，避免散落各处  
2. **对齐成熟结构**：目录与文档习惯学习 `automation-toolkit/`（DUElost）  
3. **安全上传**：默认按 Private 远程准备，上传前脱敏  
4. **便于 AI 协作**：薄契约 + 全景文档，减少重复说明  

---

## 架构总览

```
auto-tool/
├── automation-toolkit/   # [gitignore] DUElost 克隆，对照学习
├── python-tools/         # Python 工具
├── windows-tools/
├── linux-tools/
├── macos-tools/
├── android-tools/
├── shared/python-utils/  # 共享库
└── docs/
```

命名习惯（与参考仓一致）：

- `stability_*` / `performance_*` / `universal_*` / `system_*`
- 新模块优先：`领域_功能简述`，目录内自带 `README.md`、`requirements.txt`（如有）

---

## 模块索引

| 模块路径 | 语言 | 职责 | 状态 |
|----------|------|------|------|
| [python-tools/check_language&country_list](../python-tools/check_language&country_list/README.md) | Python | OOBE/设置语言与国家列表核对，输出着色 Excel | 活跃 |

待迁入候选（当前在根目录，已被 gitignore，需整理后再纳入版本库）：

- `stability_Start-Log-Scan_20261020/` → 建议目标：`python-tools/stability_Start-Log-Scan/`

---

## 编码规范

- Python：PEP 8，UTF-8，日志用 `logging`
- 密钥不进仓；配置提供 `*.example` / `config.example.json`
- 大数据、报告、日志、压缩包不进仓（见根 `.gitignore`）

---

## 与参考仓对照学习

| 参考路径 | 学什么 |
|----------|--------|
| `automation-toolkit/README.md` | 工具索引表写法 |
| `automation-toolkit/docs/project-guide.md` | 全景文档结构 |
| `automation-toolkit/AGENTS.md` | AI 契约分层 |
| `automation-toolkit/python-tools/*` | 单工具自包含：入口、依赖、说明 |
| `automation-toolkit/.gitignore` | 忽略数据/venv/密钥 |

入库与上传步骤见 [`onboarding.md`](onboarding.md)。

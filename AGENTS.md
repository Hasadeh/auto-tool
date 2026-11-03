# AGENTS.md

本文件是 AI Coding Harness 的最小启动契约。模块索引与业务细节见
[`docs/project-guide.md`](docs/project-guide.md)；入库流程见
[`docs/onboarding.md`](docs/onboarding.md)。

## 总原则

- 先读代码、测试与当前文档再改；冲突时以代码与测试为准，并同步权威文档。
- 只改当前任务必需内容，不顺手重构无关模块。
- **禁止**读取、打印、提交凭据（Token / Cookie / `.env` / 私钥 / 内网口令）。
- `automation-toolkit/` 是只读学习参考，**不要修改后提交到本仓**（已被 `.gitignore`）。
- 新工具放入对应分类目录，并更新 `README.md` 与 `docs/project-guide.md` 模块索引。

## 按需入口

| 需要的内容 | 权威入口 |
|---|---|
| 愿景 / 结构 / 模块索引 / 规范 | [`docs/project-guide.md`](docs/project-guide.md) |
| 本地入库 / 脱敏 / 上传远程 | [`docs/onboarding.md`](docs/onboarding.md) |
| 各工具说明 | 模块目录内 `README.md` / `CLAUDE.md` |

## 测试与验证

- 优先运行模块自带测试；未跑过的检查标为 pending。
- 只报告实际执行过的命令与结果。

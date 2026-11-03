# Cursor Skill · Python Tool Development

## 目标
为最终用户开发可维护、可发布、可扩展的 Python 工具项目。

## 默认开发原则

1. 优先保证工具稳定性与可读性。
2. 所有核心逻辑必须模块化。
3. 避免把业务逻辑写进单文件脚本。
4. 优先使用标准库，减少不必要依赖。
5. 所有用户输入必须校验。
6. 所有异常必须给出明确错误信息。
7. 输出日志必须可定位问题。
8. 配置项必须集中管理。
9. 保持跨平台兼容（Windows/macOS/Linux）。
10. 默认支持 UTF-8。

---

# 推荐项目结构

```text
project_name/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── services/
│   ├── models/
│   ├── utils/
│   └── core/
├── tests/
├── docs/
├── scripts/
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
└── pyproject.toml
```

---

# Cursor 开发规范

## 代码风格

- 遵循 PEP8
- 函数必须单一职责
- 避免超过 200 行的大文件
- 避免超过 50 行的大函数
- 使用类型注解
- 使用 dataclass 或 pydantic 管理结构数据

## 命名规范

- 类名：PascalCase
- 函数名：snake_case
- 常量：UPPER_CASE
- 文件名：snake_case

---

# 工程要求

## 必须实现

- 日志系统
- 配置系统
- 错误处理
- CLI 或 GUI 入口
- requirements.txt
- README.md
- 基础测试

## 推荐实现

- 自动化测试
- 打包脚本
- CI/CD
- Docker 支持
- 多语言支持

---

# 日志规范

推荐使用：

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
```

日志等级：

- DEBUG
- INFO
- WARNING
- ERROR
- CRITICAL

---

# 配置规范

推荐：

- .env
- config.yaml
- config.json

禁止：

- 硬编码 API Key
- 硬编码路径
- 硬编码数据库配置

---

# 用户体验规范

## 输出要求

- 错误信息可理解
- 操作结果明确
- 关键步骤有提示
- 长任务显示进度

## 输入要求

- 校验用户输入
- 给出示例
- 避免程序直接崩溃

---

# Python 工具推荐技术栈

## CLI 工具

推荐：

- typer
- click
- rich
- loguru

## GUI 工具

推荐：

- PySide6
- tkinter
- flet

## 数据处理

推荐：

- pandas
- openpyxl
- polars

## 网络请求

推荐：

- httpx
- requests

---

# Cursor 执行规则

当 Cursor 生成代码时：

1. 优先生成完整模块。
2. 自动拆分复杂逻辑。
3. 自动补充注释。
4. 自动添加类型。
5. 自动添加异常处理。
6. 自动生成 README 示例。
7. 自动生成 requirements.txt。
8. 自动避免重复代码。

---

# README 最低要求

README 必须包含：

- 项目简介
- 安装方式
- 使用方式
- 配置说明
- 常见错误
- 开发说明
- License

---

# 发布规范

发布前必须检查：

- 所有功能可运行
- requirements 正确
- README 可读
- 无调试代码
- 无硬编码密钥
- 日志正常
- 测试通过

---

# 推荐 Cursor Prompt 模板

```text
请基于 Python 开发一个可维护的工具项目。

要求：
1. 使用模块化结构
2. 包含日志系统
3. 包含配置系统
4. 包含错误处理
5. 使用类型注解
6. 代码符合 PEP8
7. 自动生成 README
8. 自动生成 requirements.txt
9. 提供完整项目结构
10. 输出可直接运行
```

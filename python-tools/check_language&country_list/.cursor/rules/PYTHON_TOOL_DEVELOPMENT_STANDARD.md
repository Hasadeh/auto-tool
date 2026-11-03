# Python 工具项目开发规范

## 项目目标

本项目用于开发可交付给最终用户使用的 Python 工具。

核心要求：

- 稳定
- 易维护
- 易扩展
- 易部署
- 易阅读

---

# 开发原则

## 1. 模块化

禁止：

- 所有代码堆积在 main.py
- 超长脚本
- 复制粘贴逻辑

推荐：

- services
- utils
- core
- models
- api

---

## 2. 配置集中管理

所有配置必须统一管理。

推荐：

```python
from dataclasses import dataclass

@dataclass
class Settings:
    debug: bool = False
```

禁止：

- 硬编码 Token
- 硬编码路径
- 硬编码 URL

---

## 3. 日志规范

必须记录：

- 启动信息
- 错误信息
- 关键操作
- 外部请求

推荐格式：

```python
import logging

logger = logging.getLogger(__name__)
```

---

## 4. 错误处理

禁止：

```python
except:
    pass
```

推荐：

```python
except Exception as e:
    logger.exception(e)
```

---

# 推荐目录结构

```text
project/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── services/
│   ├── core/
│   ├── utils/
│   └── models/
├── tests/
├── docs/
├── scripts/
├── requirements.txt
├── README.md
└── pyproject.toml
```

---

# 代码规范

## 类型注解

推荐：

```python
def load_data(path: str) -> list[str]:
    pass
```

---

## 函数长度

推荐：

- 单函数不超过 50 行
- 单文件不超过 200 行

---

## 命名规范

| 类型 | 规范 |
|---|---|
| 类 | PascalCase |
| 方法 | snake_case |
| 常量 | UPPER_CASE |
| 文件 | snake_case |

---

# 用户体验规范

## 必须实现

- 明确报错
- 输入校验
- 进度提示
- 操作反馈

---

# README 模板

README 至少包含：

```text
# 项目名称

## 功能介绍

## 安装方式

## 使用示例

## 配置说明

## 常见问题

## 开发说明
```

---

# requirements.txt 规范

依赖必须：

- 有版本号
- 删除无用依赖
- 避免过多大型库

示例：

```text
pandas>=2.0.0
openpyxl>=3.1.0
rich>=13.0.0
```

---

# 测试规范

推荐：

- pytest
- 基础单元测试
- 核心功能测试

示例：

```bash
pytest tests/
```

---

# 发布检查清单

发布前确认：

- [ ] README 完整
- [ ] requirements 正确
- [ ] 无调试代码
- [ ] 无 print 调试
- [ ] 日志正常
- [ ] 配置独立
- [ ] 测试通过
- [ ] 可以直接运行

---

# Cursor 推荐系统 Prompt

```text
你是一名专业 Python 工程师。

请遵循以下规则：

1. 保持模块化
2. 使用类型注解
3. 自动生成 README
4. 自动生成 requirements.txt
5. 自动处理异常
6. 自动添加日志
7. 避免重复代码
8. 保持代码可维护
9. 保持目录结构清晰
10. 输出完整可运行项目
```

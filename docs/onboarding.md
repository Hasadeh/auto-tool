# 本地入库与上传方案

面向：`D:\auto-tool` 个人仓 →（可选）Hasadeh GitHub **Private** 仓库。

---

## 环境准备（一次）

1. 已安装 Git（本机可用）。  
2. 本目录已是 Git 仓库（`git status` 可执行）。  
3. 学习参考：`D:\auto-tool\automation-toolkit`（DUElost 克隆，只读，勿改后提交）。  
4. 建议远程：GitHub 个人账号下新建 **Private** 空仓库，例如 `Hasadeh/auto-tool`。  
5. Python 工具按模块各自 `requirements.txt`；不要在根目录强行统一一个巨大 venv（可按工具建 `.venv`，已被忽略）。

绑定远程示例：

```powershell
cd D:\auto-tool
git remote add origin https://github.com/Hasadeh/auto-tool.git
git push -u origin main
```

（需已登录有写权限的 GitHub 账号；公司内网 Git 与 GitHub 凭据分开。）

---

## 新工具入库流程

```text
1. 在对应分类下建目录
   python-tools/<前缀_工具名>/
2. 拷贝代码（不要带 venv、logs、xls 报告、.env）
3. 补 README.md（用途、依赖、运行命令）
4. 敏感配置改为 example：config.example.json / .env.example
5. 更新根 README.md 工具表 + docs/project-guide.md 模块索引
6. git add / commit（确认 git status 无密钥文件）
```

可用模板：

```powershell
Copy-Item -Recurse python-tools\_template python-tools\stability_Your-Tool-Name
```

---

## 从根目录「工作副本」迁入

当前根下这些目录**默认不进 Git**（见 `.gitignore`），避免半成品/大数据误传：

| 现状 | 建议 |
|------|------|
| `stability_Start-Log-Scan_20261020/` | 整理后复制到 `python-tools/stability_Start-Log-Scan/`，去掉 `logs/`、`tmp/`、本地结果 |
| `check_language&country_list/` | 改名迁入 `python-tools/`，去掉 `&` 等不便路径字符 |

迁入并确认可运行后，再从 `.gitignore` 去掉对应根目录规则（或直接删除根目录副本）。

---

## 上传前脱敏清单

- [ ] 无 Token / 密码 / Cookie / 私钥  
- [ ] 无飞书/钉钉 Webhook 完整 URL（或已轮换）  
- [ ] 无内网绝对路径写死在默认配置（改为可配置）  
- [ ] 无真实设备 SN、客户机密数据、大体积日志/xls  
- [ ] `git status` / `git diff` 人工扫一眼  
- [ ] 远程为 **Private**（若含内部工具）  

误传密钥：立刻**轮换**密钥，不要只靠删文件（历史仍在）。

---

## 推荐日常节奏

1. 开发可在根目录临时文件夹或直接在 `python-tools/` 下进行。  
2. 稳定一版 → 按上面清单提交。  
3. 需要备份/多机同步 → `git push` 到 Private 远程。  
4. 向 DUElost/automation-toolkit 贡献时：单独 fork/PR，不要把本仓整包推进去。

# 语言和国家列表核对工具

核对开机向导（OOBE）中的语言列表、国家列表，并与 Excel 基准表比对后输出结果文件。

## 功能介绍

- 滑动采集 OOBE 语言列表和国家列表
- 跳过 OOBE 后进入系统「添加语言」界面，再核对语言列表
- 与 Excel A 列精确比对
- 另存结果文件：C 列为 OOBE 语言结果，D 列为系统添加语言结果，并着色
- 手机多出来的项追加到 A 列末尾
- 控件、跳过命令、页面包名、颜色、滑动参数全部放在 JSON，方便换项目

## 安装方式

```text
pip install -r requirements.txt
```

需要本机已安装 `adb`，设备已开启 USB 调试。

## 使用示例

按模式把设备停在对应界面后执行：

```text
python -m app 1
python -m app 0
python -m app 4
python -m app 1 -s 设备序列号
python -m app --help
```

| 参数  | OOBE 语言 | OOBE 国家 | 跳过 OOBE | 设置添加语言 | 设备起始页     |
| --- | ------- | ------- | ------- | ------ | --------- |
| `0` | 做       | 不做      | 做       | 做      | OOBE 语言列表 |
| `1` | 做       | 做       | 做       | 做      | OOBE 语言列表 |
| `2` | 做       | 做       | 做       | 不做     | OOBE 语言列表 |
| `3` | 做       | 不做      | 不做      | 不做     | OOBE 语言列表 |
| `4` | 不做      | 做       | 不做      | 不做     | OOBE 国家列表 |
| `5` | 不做      | 不做      | 不做      | 做      | 已过开机向导    |
| `6` | 做       | 做       | 不做      | 不做     | OOBE 语言列表 |
| `7` | 做       | 不做      | 做       | 不做     | OOBE 语言列表 |

## 配置说明

默认配置：`configs/default.json`

换项目时复制该文件，主要改这些字段：

- `project`：结果文件名前缀
- `package`：OOBE 包名
- `screens.*.list_container_id`：列表容器控件
- `screens.*.item_text_id`：列表项文本控件
- `screens.oobe_language.next_button`：下一步按钮
- `screens.settings_add_language.activity`：系统添加语言页包名
- `skip_oobe.commands`：跳过开机向导的命令

默认 Excel：`语言列表和国家列表.xlsx`

第 1 行为表头，从第 2 行开始核对。

- `语言列表` A 列：语言显示名；C 列 OOBE 结果；D 列系统添加语言结果。某一侧多出来的项只在对应列标「多余」，另一列留空
- `国家列表` A 列中文、B 列英文。`country_name_column` 决定比对哪一列：真机是中文改成 `1`，是英文用 `2`

配置文件支持 `//` 注释，每个字段的含义写在 `configs/default.json` 里。

结果文件输出到 `results/项目_年月日时分.xlsx`，例如 `X1102D_202609092001.xlsx`。运行日志写入同文件的「日志」sheet，避免中文乱码。执行前会读取 `ro.build.display.id` 并写入日志。

C 列颜色：

- 存在：`00B050`
- 不存在：`FF0000`
- 多余：`FFFF00`

比对规则：去掉首尾空格后精确匹配。

## 常见问题

**未检测到设备**  
检查 `adb devices` 是否为 `device` 状态。

**多台设备**  
使用 `-s 序列号`。

**未找到列表控件**  
确认当前停在对应界面，或检查 JSON 里的 resource-id 是否与该项目一致。

**第一次连接较慢**  
`uiautomator2` 首次会在手机上安装 atx-agent。

**跳过 OOBE 失败**  
部分版本 `adb root` 会失败。工具会继续下发 settings 命令，失败原因见 `logs/check.log`。

## 打包给用户

```text
pip install pyinstaller
python scripts/build_release.py
```

生成文件：`dist/语言国家列表核对.zip`。发给用户解压后即可使用，需本机已安装 `adb`。

## 开发说明

```text
python -m pytest tests/
```

扩展新项目：

1. 复制 `configs/default.json`
2. 改包名、控件 id、按钮文案、跳过命令
3. 用 `--config` 指向新文件

License: Internal use.

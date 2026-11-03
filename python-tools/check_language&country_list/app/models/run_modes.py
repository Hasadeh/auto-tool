from dataclasses import dataclass


@dataclass(frozen=True)
class RunMode:
    code: int
    description: str
    check_oobe_language: bool
    check_oobe_country: bool
    skip_oobe: bool
    check_settings_language: bool
    start_hint: str


RUN_MODES: dict[int, RunMode] = {
    0: RunMode(0, "核对OOBE语言和设置语言", True, False, True, True, "OOBE语言列表"),
    1: RunMode(1, "全部核对", True, True, True, True, "OOBE语言列表"),
    2: RunMode(2, "核对OOBE语言和国家并过开机向导", True, True, True, False, "OOBE语言列表"),
    3: RunMode(3, "只核对OOBE语言", True, False, False, False, "OOBE语言列表"),
    4: RunMode(4, "只核对OOBE国家", False, True, False, False, "OOBE国家列表"),
    5: RunMode(5, "只核对设置语言", False, False, False, True, "已过开机向导"),
    6: RunMode(6, "核对OOBE语言和国家，不过向导", True, True, False, False, "OOBE语言列表"),
    7: RunMode(7, "核对OOBE语言并过开机向导", True, False, True, False, "OOBE语言列表"),
}


def get_run_mode(code: int) -> RunMode:
    if code not in RUN_MODES:
        raise ValueError(f"不支持的运行模式: {code}，可选 0-7")
    return RUN_MODES[code]


def mode_help_text() -> str:
    lines = ["运行模式："]
    for code in range(8):
        mode = RUN_MODES[code]
        lines.append(f"  {code}  {mode.description}（设备停在{mode.start_hint}）")
    return "\n".join(lines)

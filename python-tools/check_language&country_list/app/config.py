import json
import sys
from pathlib import Path

from app.models.schemas import (
    ExcelConfig,
    ProjectConfig,
    ScreenConfig,
    Selector,
    SkipOobeConfig,
    StatusTexts,
    SwipeConfig,
)

def _runtime_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


def _bundle_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS", _runtime_root()))
    return Path(__file__).resolve().parent.parent


def _first_existing(*candidates: Path) -> Path:
    for path in candidates:
        if path.exists():
            return path
    return candidates[0]


ROOT_DIR = _runtime_root()
DEFAULT_CONFIG = _first_existing(
    ROOT_DIR / "configs" / "default.json",
    _bundle_root() / "configs" / "default.json",
)
DEFAULT_EXCEL = _first_existing(
    ROOT_DIR / "语言列表和国家列表.xlsx",
    _bundle_root() / "语言列表和国家列表.xlsx",
)
DEFAULT_OUTPUT = ROOT_DIR / "results"
DEFAULT_LOG_DIR = ROOT_DIR / "logs"


def _load_jsonc(path: Path) -> dict:
    return json.loads(_strip_json_comments(path.read_text(encoding="utf-8")))


def _strip_json_comments(text: str) -> str:
    result: list[str] = []
    in_string = False
    escape = False
    index = 0
    while index < len(text):
        char = text[index]
        nxt = text[index + 1] if index + 1 < len(text) else ""
        if in_string:
            result.append(char)
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_string = False
            index += 1
            continue
        if char == '"':
            in_string = True
            result.append(char)
        elif char == "/" and nxt == "/":
            while index < len(text) and text[index] != "\n":
                index += 1
            continue
        else:
            result.append(char)
        index += 1
    return "".join(result)


def _parse_selector(data: dict | None) -> Selector | None:
    if not data:
        return None
    return Selector(
        resource_id=data.get("resource_id"),
        text=data.get("text"),
    )


def _parse_screens(data: dict) -> dict[str, ScreenConfig]:
    screens: dict[str, ScreenConfig] = {}
    for name, raw in data.items():
        screens[name] = ScreenConfig(
            list_container_id=raw["list_container_id"],
            item_text_id=raw["item_text_id"],
            next_button=_parse_selector(raw.get("next_button")),
            wait_timeout=float(raw.get("wait_timeout", 15)),
            activity=raw.get("activity"),
        )
    return screens


def load_project_config(
    config_path: Path | None = None,
    excel_path: Path | None = None,
    project_name: str | None = None,
) -> ProjectConfig:
    path = config_path or DEFAULT_CONFIG
    if not path.exists():
        raise FileNotFoundError(f"找不到项目配置: {path}")

    raw = _load_jsonc(path)
    status = raw.get("status_texts", {})
    excel = raw.get("excel", {})
    swipe = raw.get("swipe", {})
    skip = raw.get("skip_oobe", {})

    return ProjectConfig(
        project=project_name or raw["project"],
        package=raw["package"],
        screens=_parse_screens(raw["screens"]),
        skip_oobe=SkipOobeConfig(
            commands=skip.get("commands", []),
            need_root=bool(skip.get("need_root", True)),
        ),
        excel=ExcelConfig(
            language_sheet=excel.get("language_sheet", "语言列表"),
            country_sheet=excel.get("country_sheet", "国家列表"),
            data_start_row=int(excel.get("data_start_row", 2)),
            name_column=int(excel.get("name_column", 1)),
            country_name_column=int(excel.get("country_name_column", 2)),
            result_column=int(excel.get("result_column", 3)),
            settings_result_column=int(excel.get("settings_result_column", 4)),
        ),
        colors=raw.get("colors", {}),
        swipe=SwipeConfig(**swipe) if swipe else SwipeConfig(),
        status_texts=StatusTexts(
            exist=status.get("exist", "存在"),
            missing=status.get("missing", "不存在"),
            extra=status.get("extra", "多余"),
        ),
        excel_path=str(excel_path or DEFAULT_EXCEL),
        output_dir=str(DEFAULT_OUTPUT),
    )

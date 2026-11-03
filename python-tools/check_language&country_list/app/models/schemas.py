from dataclasses import dataclass, field


@dataclass
class Selector:
    resource_id: str | None = None
    text: str | None = None


@dataclass
class ScreenConfig:
    list_container_id: str
    item_text_id: str
    next_button: Selector | None = None
    wait_timeout: float = 15.0
    activity: str | None = None


@dataclass
class SwipeConfig:
    start_ratio: float = 0.65
    end_ratio: float = 0.25
    duration: float = 0.4
    settle_seconds: float = 0.5
    max_swipes: int = 100
    no_new_limit: int = 2


@dataclass
class SkipOobeConfig:
    commands: list[str] = field(default_factory=list)
    need_root: bool = True


@dataclass
class ExcelConfig:
    language_sheet: str = "语言列表"
    country_sheet: str = "国家列表"
    data_start_row: int = 2
    name_column: int = 1
    country_name_column: int = 2
    result_column: int = 3
    settings_result_column: int = 4


@dataclass
class StatusTexts:
    exist: str = "存在"
    missing: str = "不存在"
    extra: str = "多余"


@dataclass
class ProjectConfig:
    project: str
    package: str
    screens: dict[str, ScreenConfig]
    skip_oobe: SkipOobeConfig
    excel: ExcelConfig
    colors: dict[str, str]
    swipe: SwipeConfig
    status_texts: StatusTexts
    excel_path: str
    output_dir: str


@dataclass
class CompareItem:
    name: str
    status: str

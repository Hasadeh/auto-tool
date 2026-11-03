import logging

from app.core.device import start_activity
from app.models.run_modes import RunMode
from app.models.schemas import CompareItem, ProjectConfig
from app.services.comparer import compare_lists
from app.services.excel_io import name_column_for, read_expected_names, write_result_workbook
from app.services.oobe import skip_oobe
from app.services.ui_scraper import click_next, collect_list_texts

logger = logging.getLogger("check_list")


def run_oobe_check(
    device,
    serial: str,
    config: ProjectConfig,
    mode: RunMode,
    log_lines: list[str],
) -> str:
    logger.info("运行模式 %s：%s（设备应停在%s）", mode.code, mode.description, mode.start_hint)
    language_results = _maybe_check_oobe_language(device, config, mode)
    country_results = _maybe_check_oobe_country(device, config, mode)
    if mode.skip_oobe:
        skip_oobe(serial, config.skip_oobe)
    settings_results = None
    if mode.check_settings_language:
        settings_results = _check_settings_language(device, serial, config)

    logger.info("开始写入结果文件")
    output = write_result_workbook(
        config,
        language_results,
        country_results,
        log_lines,
        settings_results,
    )
    logger.info("结果已写入: %s", output)
    return str(output)


def _maybe_check_oobe_language(device, config: ProjectConfig, mode: RunMode):
    if not mode.check_oobe_language:
        return None
    return _check_screen(
        device,
        config,
        screen_key="oobe_language",
        sheet_name=config.excel.language_sheet,
        label="OOBE语言",
    )


def _maybe_check_oobe_country(device, config: ProjectConfig, mode: RunMode):
    if not mode.check_oobe_country:
        return None
    if mode.check_oobe_language:
        click_next(device, config.screens["oobe_language"].next_button)
    return _check_screen(
        device,
        config,
        screen_key="oobe_country",
        sheet_name=config.excel.country_sheet,
        label="OOBE国家",
    )


def _check_settings_language(device, serial: str, config: ProjectConfig) -> list[CompareItem]:
    screen = config.screens.get("settings_add_language")
    if screen is None:
        raise KeyError("配置中缺少界面: settings_add_language")
    if screen.activity:
        start_activity(serial, screen.activity)
    return _check_screen(
        device,
        config,
        screen_key="settings_add_language",
        sheet_name=config.excel.language_sheet,
        label="系统添加语言",
    )


def _check_screen(
    device,
    config: ProjectConfig,
    screen_key: str,
    sheet_name: str,
    label: str,
) -> list[CompareItem]:
    if screen_key not in config.screens:
        raise KeyError(f"配置中缺少界面: {screen_key}")

    logger.info("开始核对%s列表", label)
    expected = read_expected_names(
        config.excel_path,
        sheet_name,
        name_column_for(config.excel, sheet_name),
        config.excel.data_start_row,
    )
    actual = collect_list_texts(device, config.screens[screen_key], config.swipe)
    results = compare_lists(expected, actual, config.status_texts)
    _log_summary(label, results, config)
    return results


def _log_summary(label: str, results: list[CompareItem], config: ProjectConfig) -> None:
    texts = config.status_texts
    exist = sum(item.status == texts.exist for item in results)
    missing = sum(item.status == texts.missing for item in results)
    extra = sum(item.status == texts.extra for item in results)
    logger.info("%s列表结果: 存在 %s，不存在 %s，多余 %s", label, exist, missing, extra)

import re
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import PatternFill

from app.models.schemas import (
    CompareItem,
    ExcelConfig,
    ProjectConfig,
    ScreenConfig,
    SkipOobeConfig,
    StatusTexts,
    SwipeConfig,
)
from app.services.excel_io import read_expected_names, write_result_workbook


def _make_config(excel_path: Path, output_dir: Path) -> ProjectConfig:
    return ProjectConfig(
        project="DEMO",
        package="demo",
        screens={"oobe_language": ScreenConfig("rv", "name")},
        skip_oobe=SkipOobeConfig(),
        excel=ExcelConfig(),
        colors={"存在": "00B050", "不存在": "FF0000", "多余": "FFFF00"},
        swipe=SwipeConfig(),
        status_texts=StatusTexts(),
        excel_path=str(excel_path),
        output_dir=str(output_dir),
    )


def _build_template(path: Path) -> None:
    workbook = Workbook()
    language = workbook.active
    language.title = "语言列表"
    language["A1"] = "语言（对应国家语言）"
    language["B1"] = "语言（对应国家汉语）"
    language["C1"] = "OOBE界面"
    language["D1"] = "设置界面"
    language["A2"] = "English"
    language["B2"] = "英语"
    language["A3"] = "Français"
    country = workbook.create_sheet("国家列表")
    country["A1"] = "国家列表（中文）"
    country["B1"] = "国家列表（英语）"
    country["C1"] = "是否存在"
    country["A2"] = "中国"
    country["B2"] = "China"
    workbook.save(path)
    workbook.close()


def test_read_and_write_result(tmp_path: Path) -> None:
    source = tmp_path / "template.xlsx"
    _build_template(source)
    config = _make_config(source, tmp_path / "out")
    language_results = [
        CompareItem("English", "存在"),
        CompareItem("Français", "不存在"),
        CompareItem("Italiano", "多余"),
    ]
    logs = [
        "2026-09-09 20:01:00 - INFO - 版本号 ro.build.display.id: X1102D-test",
        "2026-09-09 20:01:01 - INFO - 开始核对语言列表",
    ]
    country_results = [
        CompareItem("China", "存在"),
        CompareItem("Kenya", "多余"),
    ]
    output = write_result_workbook(config, language_results, country_results, logs)
    assert output.exists()
    assert re.fullmatch(r"DEMO_\d{12}\.xlsx", output.name)

    workbook = load_workbook(output)
    sheet = workbook["语言列表"]
    assert sheet["C1"].value == "OOBE界面"
    assert sheet["C2"].value == "存在"
    assert sheet["C3"].value == "不存在"
    assert sheet["A4"].value == "Italiano"
    assert sheet["C4"].value == "多余"
    assert _fill_color(sheet["C2"].fill) == "00B050"
    assert _fill_color(sheet["C3"].fill) == "FF0000"
    assert _fill_color(sheet["C4"].fill) == "FFFF00"
    country = workbook["国家列表"]
    assert country["C1"].value == "是否存在"
    assert country["C2"].value == "存在"
    assert country["B3"].value == "Kenya"
    assert country["C3"].value == "多余"
    log_sheet = workbook["日志"]
    assert log_sheet["A1"].value == logs[0]
    assert "版本号" in log_sheet["A1"].value
    assert log_sheet["A2"].value == logs[1]
    workbook.close()

    names = read_expected_names(str(source), "语言列表", 1, 2)
    assert names == ["English", "Français"]
    country_names = read_expected_names(str(source), "国家列表", 2, 2)
    assert country_names == ["China"]


def test_write_settings_language_column_d(tmp_path: Path) -> None:
    source = tmp_path / "template.xlsx"
    _build_template(source)
    config = _make_config(source, tmp_path / "out")
    oobe_results = [
        CompareItem("English", "存在"),
        CompareItem("Français", "不存在"),
        CompareItem("Italiano", "多余"),
    ]
    settings_results = [
        CompareItem("English", "存在"),
        CompareItem("Français", "存在"),
        CompareItem("Deutsch", "多余"),
    ]
    output = write_result_workbook(config, oobe_results, None, [], settings_results)
    workbook = load_workbook(output)
    sheet = workbook["语言列表"]
    assert sheet["D1"].value == "设置界面"
    assert sheet["D2"].value == "存在"
    assert sheet["D3"].value == "存在"
    assert sheet["A4"].value == "Italiano"
    assert sheet["C4"].value == "多余"
    assert sheet["D4"].value is None
    assert sheet["A5"].value == "Deutsch"
    assert sheet["C5"].value is None
    assert sheet["D5"].value == "多余"
    assert _fill_color(sheet["D2"].fill) == "00B050"
    assert _fill_color(sheet["D5"].fill) == "FFFF00"
    workbook.close()


def test_write_settings_only_column_d(tmp_path: Path) -> None:
    source = tmp_path / "template.xlsx"
    _build_template(source)
    config = _make_config(source, tmp_path / "out")
    settings_results = [
        CompareItem("English", "存在"),
        CompareItem("Français", "不存在"),
        CompareItem("Deutsch", "多余"),
    ]
    output = write_result_workbook(config, None, None, [], settings_results)
    workbook = load_workbook(output)
    sheet = workbook["语言列表"]
    assert sheet["C2"].value is None
    assert sheet["D2"].value == "存在"
    assert sheet["D3"].value == "不存在"
    assert sheet["A4"].value == "Deutsch"
    assert sheet["D4"].value == "多余"
    workbook.close()


def _fill_color(fill: PatternFill) -> str:
    return (fill.fgColor.rgb or "")[-6:]

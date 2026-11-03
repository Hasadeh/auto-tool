from datetime import datetime
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.worksheet.worksheet import Worksheet

LOG_FONT = Font(name="Microsoft YaHei", size=11)

from app.models.schemas import CompareItem, ExcelConfig, ProjectConfig


def name_column_for(excel: ExcelConfig, sheet_name: str) -> int:
    if sheet_name == excel.country_sheet:
        return excel.country_name_column
    return excel.name_column


def read_expected_names(
    excel_path: str,
    sheet_name: str,
    name_column: int,
    start_row: int = 2,
) -> list[str]:
    workbook = load_workbook(excel_path, read_only=True, data_only=True)
    if sheet_name not in workbook.sheetnames:
        workbook.close()
        raise ValueError(f"Excel 中不存在 sheet: {sheet_name}")
    sheet = workbook[sheet_name]
    names: list[str] = []
    for row in sheet.iter_rows(
        min_row=start_row,
        min_col=name_column,
        max_col=name_column,
        values_only=True,
    ):
        value = str(row[0]).strip() if row[0] is not None else ""
        if value:
            names.append(value)
    workbook.close()
    if not names:
        raise ValueError(f"{sheet_name} 没有可核对的数据")
    return names


def write_result_workbook(
    config: ProjectConfig,
    language_results: list[CompareItem] | None,
    country_results: list[CompareItem] | None,
    log_lines: list[str] | None = None,
    settings_language_results: list[CompareItem] | None = None,
) -> Path:
    source = Path(config.excel_path)
    if not source.exists():
        raise FileNotFoundError(f"找不到 Excel 模板: {source}")

    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = _build_output_path(output_dir, config.project)

    workbook = load_workbook(source)
    excel = config.excel
    extra_status = config.status_texts.extra
    language_sheet = workbook[excel.language_sheet]
    if language_results is not None and settings_language_results is not None:
        _write_language_dual(
            language_sheet,
            language_results,
            settings_language_results,
            excel,
            config.colors,
            extra_status,
        )
    elif language_results is not None:
        _write_sheet(language_sheet, language_results, excel, config.colors, extra_status)
    elif settings_language_results is not None:
        _write_sheet(
            language_sheet,
            settings_language_results,
            excel,
            config.colors,
            extra_status,
            result_column=excel.settings_result_column,
        )
    if country_results is not None:
        _write_sheet(
            workbook[excel.country_sheet],
            country_results,
            excel,
            config.colors,
            extra_status,
            excel.country_name_column,
        )
    _write_log_sheet(workbook, log_lines or [])
    workbook.save(output_path)
    workbook.close()
    return output_path


def _write_sheet(
    sheet: Worksheet,
    results: list[CompareItem],
    excel: ExcelConfig,
    colors: dict[str, str],
    extra_status: str,
    name_column: int | None = None,
    result_column: int | None = None,
) -> None:
    name_col = name_column or excel.name_column
    result_col = result_column or excel.result_column
    start_row = excel.data_start_row
    expected = [item for item in results if item.status != extra_status]
    extras = [item for item in results if item.status == extra_status]
    for offset, item in enumerate(expected):
        _write_result_cell(
            sheet,
            start_row + offset,
            result_col,
            item.status,
            colors,
        )
    next_row = _last_name_row(sheet, name_col) + 1
    for item in extras:
        sheet.cell(row=next_row, column=name_col, value=item.name)
        _write_result_cell(sheet, next_row, result_col, item.status, colors)
        next_row += 1


def _write_language_dual(
    sheet: Worksheet,
    oobe_results: list[CompareItem],
    settings_results: list[CompareItem],
    excel: ExcelConfig,
    colors: dict[str, str],
    extra_status: str,
) -> None:
    start_row = excel.data_start_row
    oobe_expected = [item for item in oobe_results if item.status != extra_status]
    settings_expected = [item for item in settings_results if item.status != extra_status]
    for offset, item in enumerate(oobe_expected):
        _write_result_cell(
            sheet,
            start_row + offset,
            excel.result_column,
            item.status,
            colors,
        )
    for offset, item in enumerate(settings_expected):
        _write_result_cell(
            sheet,
            start_row + offset,
            excel.settings_result_column,
            item.status,
            colors,
        )

    oobe_extras = {item.name: item for item in oobe_results if item.status == extra_status}
    settings_extras = {
        item.name: item for item in settings_results if item.status == extra_status
    }
    extra_names = list(dict.fromkeys([*oobe_extras, *settings_extras]))
    next_row = _last_name_row(sheet, excel.name_column) + 1
    for name in extra_names:
        sheet.cell(row=next_row, column=excel.name_column, value=name)
        if name in oobe_extras:
            _write_result_cell(sheet, next_row, excel.result_column, extra_status, colors)
        if name in settings_extras:
            _write_result_cell(
                sheet,
                next_row,
                excel.settings_result_column,
                extra_status,
                colors,
            )
        next_row += 1


def _write_result_cell(
    sheet: Worksheet,
    row: int,
    column: int,
    status: str,
    colors: dict[str, str],
) -> None:
    cell = sheet.cell(row=row, column=column, value=status)
    color = colors.get(status)
    if color:
        cell.fill = PatternFill(start_color=color, end_color=color, fill_type="solid")


def _last_name_row(sheet: Worksheet, name_column: int) -> int:
    row = 1
    while sheet.cell(row=row, column=name_column).value not in (None, ""):
        row += 1
    return row - 1


def _write_log_sheet(workbook: Workbook, log_lines: list[str]) -> None:
    name = "日志"
    sheet = workbook[name] if name in workbook.sheetnames else workbook.create_sheet(name)
    sheet.delete_rows(1, sheet.max_row or 1)
    sheet.column_dimensions["A"].width = 120
    for index, line in enumerate(log_lines, start=1):
        cell = sheet.cell(row=index, column=1, value=line)
        cell.font = LOG_FONT


def _build_output_path(output_dir: Path, project: str) -> Path:
    stamp = datetime.now().strftime("%Y%m%d%H%M")
    path = output_dir / f"{project}_{stamp}.xlsx"
    if not path.exists():
        return path
    stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return output_dir / f"{project}_{stamp}.xlsx"

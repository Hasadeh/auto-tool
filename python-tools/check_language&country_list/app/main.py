import argparse
import sys
from pathlib import Path

from app.config import DEFAULT_LOG_DIR, load_project_config
from app.core.device import DeviceError, connect_u2, get_display_id, resolve_serial
from app.models.run_modes import get_run_mode, mode_help_text
from app.services.ui_scraper import UiScrapeError
from app.services.workflow import run_oobe_check
from app.utils.logging_setup import setup_logging


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="核对 OOBE / 设置中的语言和国家列表",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=mode_help_text(),
    )
    parser.add_argument(
        "mode",
        type=int,
        choices=range(8),
        metavar="mode",
        help="运行模式 0-7，详见下方说明",
    )
    parser.add_argument("-s", "--serial", help="设备序列号，多设备时必填")
    parser.add_argument("--config", type=Path, help="项目 JSON 配置路径")
    parser.add_argument("--excel", type=Path, help="语言/国家列表 Excel 路径")
    parser.add_argument("--project", help="覆盖配置中的项目名，用于结果文件命名")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if getattr(sys, "frozen", False) and argv is None and len(sys.argv) == 1:
        print(mode_help_text())
        print("用法: 语言国家列表核对.exe 模式号")
        input("按回车退出")
        return 0
    logger, log_handler = setup_logging(DEFAULT_LOG_DIR)
    args = parse_args(argv)

    try:
        config = load_project_config(args.config, args.excel, args.project)
        mode = get_run_mode(args.mode)
        serial = resolve_serial(args.serial)
        display_id = get_display_id(serial)
        logger.info("版本号: %s", display_id)
        device = connect_u2(serial)
        output = run_oobe_check(device, serial, config, mode, log_handler.records)
    except (DeviceError, UiScrapeError, FileNotFoundError, ValueError, KeyError) as exc:
        logger.error("%s", exc)
        return 1
    except Exception:
        logger.exception("执行失败")
        return 1

    logger.info("核对完成: %s", output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

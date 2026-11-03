import shutil
import subprocess
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
RELEASE_DIR = DIST / "语言国家列表核对"
EXE_NAME = "语言国家列表核对.exe"
ZIP_NAME = "语言国家列表核对.zip"


def main() -> int:
    _run_pyinstaller()
    _assemble_release()
    zip_path = _zip_release()
    print(f"打包完成: {zip_path}")
    return 0


def _run_pyinstaller() -> None:
    excel_name = "语言列表和国家列表.xlsx"
    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--console",
        "--name",
        "语言国家列表核对",
        "--collect-all",
        "uiautomator2",
        "--collect-all",
        "adbutils",
        "--add-data",
        f"{ROOT / 'configs' / 'default.json'};configs",
        "--add-data",
        f"{ROOT / excel_name};.",
        str(ROOT / "run.py"),
    ]
    subprocess.run(command, cwd=ROOT, check=True)


def _assemble_release() -> None:
    if RELEASE_DIR.exists():
        shutil.rmtree(RELEASE_DIR)
    RELEASE_DIR.mkdir(parents=True)
    shutil.copy2(DIST / EXE_NAME, RELEASE_DIR / EXE_NAME)
    shutil.copy2(ROOT / "语言列表和国家列表.xlsx", RELEASE_DIR / "语言列表和国家列表.xlsx")
    (RELEASE_DIR / "configs").mkdir()
    shutil.copy2(ROOT / "configs" / "default.json", RELEASE_DIR / "configs" / "default.json")
    shutil.copy2(ROOT / "docs" / "用户使用说明.txt", RELEASE_DIR / "使用说明.txt")
    (RELEASE_DIR / "运行.bat").write_text(
        "\r\n".join(
            [
                "chcp 65001 >nul",
                "@echo off",
                "echo 语言和国家列表核对工具",
                "echo.",
                "type 使用说明.txt",
                "echo.",
                "set /p MODE=请输入运行模式 0-7: ",
                "语言国家列表核对.exe %MODE%",
                "pause",
                "",
            ]
        ),
        encoding="utf-8",
    )


def _zip_release() -> Path:
    zip_path = DIST / ZIP_NAME
    if zip_path.exists():
        zip_path.unlink()
    with ZipFile(zip_path, "w", ZIP_DEFLATED) as archive:
        for file in RELEASE_DIR.rglob("*"):
            if file.is_file():
                archive.write(file, file.relative_to(DIST))
    return zip_path


if __name__ == "__main__":
    raise SystemExit(main())

import logging
import subprocess

import uiautomator2 as u2

logger = logging.getLogger("check_list")


class DeviceError(RuntimeError):
    """设备连接或 ADB 执行失败。"""


def list_serials() -> list[str]:
    result = _run_adb(["devices"])
    serials: list[str] = []
    for line in result.splitlines()[1:]:
        parts = line.split()
        if len(parts) >= 2 and parts[1] == "device":
            serials.append(parts[0])
    return serials


def resolve_serial(serial: str | None) -> str:
    serials = list_serials()
    if serial:
        if serial not in serials:
            raise DeviceError(f"设备未连接: {serial}")
        return serial
    if not serials:
        raise DeviceError("未检测到设备，请连接手机并开启 USB 调试")
    if len(serials) > 1:
        raise DeviceError(f"检测到多台设备，请用 -s 指定: {serials}")
    return serials[0]


def connect_u2(serial: str) -> u2.Device:
    logger.info("正在连接设备 %s", serial)
    device = u2.connect(serial)
    device.implicitly_wait(5)
    logger.info("设备连接成功")
    return device


def get_display_id(serial: str) -> str:
    value = adb_shell(serial, "getprop ro.build.display.id").strip()
    return value or "(空)"


def start_activity(serial: str, component: str) -> None:
    logger.info("启动界面: %s", component)
    adb_shell(serial, f"am start -n {component}")


def adb_root(serial: str) -> None:
    _run_adb(["-s", serial, "root"])


def adb_shell(serial: str, command: str) -> str:
    return _run_adb(["-s", serial, "shell", command])


def _run_adb(args: list[str]) -> str:
    completed = subprocess.run(
        ["adb", *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).strip()
        raise DeviceError(f"adb {' '.join(args)} 失败: {detail}")
    return completed.stdout

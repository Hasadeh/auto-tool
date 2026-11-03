import logging

from app.core.device import DeviceError, adb_root, adb_shell
from app.models.schemas import SkipOobeConfig

logger = logging.getLogger("check_list")


def skip_oobe(serial: str, config: SkipOobeConfig) -> None:
    if config.need_root:
        try:
            adb_root(serial)
            logger.info("已执行 adb root")
        except DeviceError as exc:
            logger.warning("adb root 失败，继续尝试跳过 OOBE: %s", exc)

    for command in config.commands:
        logger.info("跳过 OOBE: %s", command)
        output = adb_shell(serial, command)
        if output.strip():
            logger.debug(output.strip())
    logger.info("已跳过 OOBE")

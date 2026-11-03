import logging
import time

import uiautomator2 as u2

from app.models.schemas import ScreenConfig, Selector, SwipeConfig

logger = logging.getLogger("check_list")


class UiScrapeError(RuntimeError):
    """界面抓取或点击失败。"""


def wait_for_screen(device: u2.Device, screen: ScreenConfig) -> None:
    deadline = time.time() + screen.wait_timeout
    while time.time() < deadline:
        list_ready = device(resourceId=screen.list_container_id).exists
        item_ready = device(resourceId=screen.item_text_id).exists
        if list_ready and item_ready:
            return
        time.sleep(0.4)
    raise UiScrapeError(f"等待界面超时，未找到列表控件: {screen.list_container_id}")


def collect_list_texts(
    device: u2.Device,
    screen: ScreenConfig,
    swipe: SwipeConfig,
) -> list[str]:
    wait_for_screen(device, screen)
    collected: list[str] = []
    seen: set[str] = set()
    no_new = 0

    for index in range(swipe.max_swipes):
        added = _collect_visible(device, screen.item_text_id, collected, seen)
        logger.info(
            "第 %s 次采集，本屏新增 %s 个，累计 %s 个",
            index + 1,
            added,
            len(collected),
        )
        if added == 0:
            no_new += 1
            if no_new >= swipe.no_new_limit:
                break
        else:
            no_new = 0
        _swipe_list(device, screen.list_container_id, swipe)
        time.sleep(swipe.settle_seconds)

    if not collected:
        raise UiScrapeError(f"未采集到任何列表项: {screen.item_text_id}")
    logger.info("列表采集完成，共 %s 项", len(collected))
    return collected


def click_next(device: u2.Device, button: Selector | None) -> None:
    if button is None:
        raise UiScrapeError("当前界面未配置下一步按钮")
    if button.resource_id and device(resourceId=button.resource_id).exists:
        device(resourceId=button.resource_id).click()
        logger.info("已点击下一步: %s", button.resource_id)
        return
    if button.text and device(text=button.text).exists:
        device(text=button.text).click()
        logger.info("已点击下一步: %s", button.text)
        return
    raise UiScrapeError("未找到下一步按钮")


def _collect_visible(
    device: u2.Device,
    item_text_id: str,
    collected: list[str],
    seen: set[str],
) -> int:
    added = 0
    elements = device(resourceId=item_text_id)
    for index in range(elements.count):
        text = (elements[index].get_text() or "").strip()
        if text and text not in seen:
            collected.append(text)
            seen.add(text)
            added += 1
    return added


def _swipe_list(device: u2.Device, container_id: str, swipe: SwipeConfig) -> None:
    container = device(resourceId=container_id)
    if not container.exists:
        raise UiScrapeError(f"列表控件不存在: {container_id}")
    bounds = container.info["bounds"]
    center_x = (bounds["left"] + bounds["right"]) // 2
    height = bounds["bottom"] - bounds["top"]
    start_y = int(bounds["top"] + height * swipe.start_ratio)
    end_y = int(bounds["top"] + height * swipe.end_ratio)
    device.swipe(center_x, start_y, center_x, end_y, swipe.duration)

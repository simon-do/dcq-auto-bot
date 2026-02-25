import asyncio
import os

from playwright.async_api import Page

from core.ai.vision import find_and_click
from core.logger import get_logger

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")

log = get_logger("daily_checkin")


def template(name: str) -> str:
    return os.path.join(TEMPLATES_DIR, name)


async def daily_checkin(page: Page):
    """Daily check-in: Nhiệm vụ → Điểm danh → Nhận quà."""

    found = await find_and_click(page, template("nhiem_vu_icon.png"), "Nhiệm vụ")
    if not found:
        log.error("Could not find 'Nhiệm vụ' icon, aborting")
        return

    await asyncio.sleep(1)
    found = await find_and_click(page, template("phu_de_icon.png"), "Phủ đệ")
    if not found:
        log.error("Could not find 'Phủ đệ' icon, aborting")
        return

    await asyncio.sleep(1)
    found = await find_and_click(page, template("nap_han_gio_icon.png"), "Nạp hạn giờ")
    if not found:
        log.error("Could not find 'Nạp hạn giờ' icon, aborting")
        return

    log.info("✔ daily_checkin complete")

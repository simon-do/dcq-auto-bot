import asyncio
import os

from playwright.async_api import Page

from core.ai.vision import (
    find_any_on_screen,
    load_template,
    take_screenshot,
    wait_for_template,
)
from core.logger import get_logger

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")

log = get_logger("close_banners")

BLANK_AREA_CLICK = (20, 880)
MAX_ROUNDS = 10
WAIT_AFTER_CLOSE = 1.5


def template(name: str):
    return os.path.join(TEMPLATES_DIR, name)


async def close_starting_banners(page: Page):
    """Dismiss all startup popups by detecting close buttons or 'click blank area' text."""

    await wait_for_template(page, template("confirm_button_1.png"), "Confirm button", timeout=30)

    confirm_button = [
        ("confirm_button_1", load_template(template("confirm_button_1.png"))),
    ]

    close_buttons = [
        ("close_button_1", load_template(template("close_button_1.png"))),
        ("close_button_2", load_template(template("close_button_2.png"))),
    ]

    blank_area_indicators = [
        ("click_blank_area_1", load_template(template("click_blank_area_to_close_1.png"))),
        ("click_blank_area_2", load_template(template("click_blank_area_to_close_2.png"))),
    ]

    all_templates = confirm_button + close_buttons + blank_area_indicators
    closed = 0

    for round in range(MAX_ROUNDS):
        await asyncio.sleep(WAIT_AFTER_CLOSE)
        screenshot = await take_screenshot(page)

        match = find_any_on_screen(screenshot, all_templates)

        if match is None:
            log.info(f"No more popups detected (closed {closed} total)")
            break

        label, x, y = match

        if label.startswith("close_button") or label.startswith("confirm_button"):
            log.info(f"Found '{label}' at ({x}, {y}), clicking it")
            await page.mouse.click(x, y)
        else:
            log.info(f"Found '{label}', clicking blank area at {BLANK_AREA_CLICK}")
            await page.mouse.click(*BLANK_AREA_CLICK)

        closed += 1

    else:
        log.warning(f"Reached max rounds ({MAX_ROUNDS}), some popups may remain")

    log.info(f"✔ close_starting_banners complete ({closed} popups closed)")

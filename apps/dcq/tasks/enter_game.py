import asyncio
import json
import os

from playwright.async_api import Page

from core.logger import get_logger, log_step

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.json")

log = get_logger("enter_game")


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


async def click_point(page: Page, point: dict, label: str, delay: float):
    x = point["x"]
    y = point["y"]
    with log_step(log, f"Click {label} at ({x}, {y})"):
        await page.mouse.click(x, y)
        await asyncio.sleep(delay)


async def enter_game(page: Page):
    """Click through server selection and enter game using viewport coordinates."""
    cfg = load_config(CONFIG_PATH)
    pts = cfg["points"]
    delay = cfg.get("delay_between_clicks", 0.5)

    await click_point(page, pts["close_popup"], "Close popup (P1)", 2)
    await click_point(page, pts["change_region"], "Change region (P2)", delay)
    await click_point(page, pts["my_server"], "My server (P3)", delay)
    await click_point(page, pts["target_server"], "Target server (P4)", delay)
    await click_point(page, pts["start_game"], "Start game (P5)", delay)

    log.info("✔ enter_game complete")

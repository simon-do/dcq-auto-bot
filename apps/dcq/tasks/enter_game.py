import os

from playwright.async_api import Page

from core.ai.vision import find_and_click
from core.logger import get_logger

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")

log = get_logger("enter_game")


def template(name: str) -> str:
    return os.path.join(TEMPLATES_DIR, name)


async def enter_game(page: Page):
    """Navigate through server selection using template matching."""

    steps = [
        ("update_info_close_button.png", "Close Update Information"),
        ("change_region_button.png", "Change region"),
        ("my_server_option.png", "My server"),
        ("phu_quy_s3_option.png", "Phú Quý S3"),
        ("start_game_button.png", "Start game"),
    ]

    for tmpl_name, label in steps:
        found = await find_and_click(page, template(tmpl_name), label, timeout=30)
        if not found:
            log.error(f"Could not find '{label}', aborting enter_game")
            return

    log.info("✔ enter_game complete")

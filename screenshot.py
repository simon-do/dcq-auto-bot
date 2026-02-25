import asyncio
import os
from datetime import datetime

from core.browser.browser import launch_browser
from core.logger import get_logger
from core.ai.vision import take_screenshot
from apps.dcq.tasks.login import login
from apps.dcq.tasks.enter_game import enter_game

import cv2

SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), "apps", "dcq", "screenshots")

log = get_logger("screenshot")


async def main():
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

    pw, browser, page = await launch_browser()
    log.info("▶ Browser launched")

    await login(page)

    log.info("⏳ Waiting 10s for game to load...")
    await asyncio.sleep(10)

    await enter_game(page)

    log.info("⏳ Waiting 5s for game main screen...")
    await asyncio.sleep(5)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"game_{timestamp}.png"
    filepath = os.path.join(SCREENSHOTS_DIR, filename)

    screenshot = await take_screenshot(page)
    cv2.imwrite(filepath, screenshot)
    log.info(f"✔ Screenshot saved: {filepath}")

    log.info("📸 You can take more screenshots. Press Enter after each one.")
    log.info("📝 Type 'q' + Enter to quit.")

    while True:
        user_input = input("\n[Enter] = screenshot, [q] = quit: ").strip()
        if user_input.lower() == "q":
            break

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"game_{timestamp}.png"
        filepath = os.path.join(SCREENSHOTS_DIR, filename)

        screenshot = await take_screenshot(page)
        cv2.imwrite(filepath, screenshot)
        log.info(f"✔ Screenshot saved: {filepath}")

    await browser.close()
    await pw.stop()


asyncio.run(main())

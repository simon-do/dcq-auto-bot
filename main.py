import asyncio

from core.browser.browser import launch_browser
from core.logger import get_logger
from core.ai.vision import wait_for_template
from apps.dcq.tasks.login import login
from apps.dcq.tasks.enter_game import enter_game
from apps.dcq.tasks.close_banners import close_starting_banners
from apps.dcq.tasks.daily_checkin import daily_checkin

CONFIRM_BTN_TEMPLATE = "apps/dcq/templates/confirm_button_1.png"

log = get_logger("main")


async def main():
    pw, browser, page = await launch_browser()
    log.info("▶ Browser launched")

    await login(page)

    log.info("⏳ Waiting 10s for game to load...")
    await asyncio.sleep(10)

    await enter_game(page)

    await wait_for_template(page, CONFIRM_BTN_TEMPLATE, "Confirm button", timeout=30)

    await close_starting_banners(page)

    await daily_checkin(page)

    log.info("✔ All tasks complete. Browser stays open.")
    input("Press Enter to close browser...")

    await browser.close()
    await pw.stop()


asyncio.run(main())

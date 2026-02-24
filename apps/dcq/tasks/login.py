import os

from dotenv import load_dotenv
from playwright.async_api import Page

from core.logger import get_logger, log_step

load_dotenv()

log = get_logger("login")

URL = os.getenv("DCQ_URL", "")
USERNAME = os.getenv("DCQ_USERNAME", "")
PASSWORD = os.getenv("DCQ_PASSWORD", "")


async def login(page: Page):
    """Navigate to game URL and login with credentials from .env."""
    with log_step(log, "Navigate to game URL"):
        await page.goto(URL)

    with log_step(log, "Fill username and password"):
        await page.fill("#loginAccountInput", USERNAME)
        await page.fill("#loginPassInput", PASSWORD)

    with log_step(log, "Click login button"):
        await page.click("button.j-account-login-btn")

    log.info("✔ login complete")

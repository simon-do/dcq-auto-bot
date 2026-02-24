from playwright.async_api import async_playwright, Playwright, Browser, Page


WINDOW_WIDTH = 500
WINDOW_HEIGHT = 1000
VIEWPORT_WIDTH = 500
VIEWPORT_HEIGHT = 900


async def launch_browser() -> tuple[Playwright, Browser, Page]:
    """Launch Chromium with a fixed 500x900 viewport and window at top-left."""
    pw = await async_playwright().start()
    browser = await pw.chromium.launch(
        headless=False,
        args=[
            f"--window-size={WINDOW_WIDTH},{WINDOW_HEIGHT}",
            "--window-position=0,0",
        ],
    )
    context = await browser.new_context(
        viewport={"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT}
    )
    page = await context.new_page()
    return pw, browser, page

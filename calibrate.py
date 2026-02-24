import asyncio

from core.browser.browser import launch_browser
from core.logger import get_logger
from apps.dcq.tasks.login import login

log = get_logger("calibrate")

OVERLAY_JS = """
(() => {
    const overlay = document.createElement('div');
    overlay.style.cssText = `
        position: fixed; top: 8px; left: 8px; z-index: 999999;
        background: rgba(0,0,0,0.8); color: #0f0; padding: 6px 12px;
        font: bold 16px monospace; border-radius: 6px; pointer-events: none;
    `;
    overlay.textContent = 'Move mouse...';
    document.body.appendChild(overlay);
    document.addEventListener('mousemove', e => {
        overlay.textContent = `x: ${e.clientX}  y: ${e.clientY}`;
    });
    document.addEventListener('click', e => {
        console.log(`CLICK => { "x": ${e.clientX}, "y": ${e.clientY} }`);
    });
})();
"""


async def main():
    pw, browser, page = await launch_browser()
    log.info("▶ Browser launched")

    await login(page)

    log.info("⏳ Waiting 10s for game to load...")
    await asyncio.sleep(10)

    await page.evaluate(OVERLAY_JS)
    log.info("✔ Coordinate overlay injected!")
    log.info("👆 Move mouse to see viewport coordinates on screen")
    log.info("👆 Click anywhere — coordinates will print in this terminal")
    log.info("📝 Copy the coordinates to config.json")

    input("\nPress Enter to close browser...")
    await browser.close()
    await pw.stop()


asyncio.run(main())

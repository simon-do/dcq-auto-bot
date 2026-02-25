import asyncio
import os

import cv2
import numpy as np
from playwright.async_api import Page

from core.logger import get_logger, log_step

log = get_logger("vision")


async def take_screenshot(page: Page) -> np.ndarray:
    """Capture viewport screenshot and return as OpenCV BGR image."""
    png_bytes = await page.screenshot()
    arr = np.frombuffer(png_bytes, dtype=np.uint8)
    return cv2.imdecode(arr, cv2.IMREAD_COLOR)


def find_on_screen(
    screenshot: np.ndarray,
    template: np.ndarray,
    threshold: float = 0.7,
) -> tuple[int, int] | None:
    """Find template in screenshot using grayscale template matching.

    Returns (x, y) center of best match if confidence >= threshold, else None.
    """
    screen_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    tmpl_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(screen_gray, tmpl_gray, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val < threshold:
        return None

    h, w = tmpl_gray.shape
    cx = max_loc[0] + w // 2
    cy = max_loc[1] + h // 2

    log.debug(f"Match confidence: {max_val:.2f} at ({cx}, {cy})")
    return (cx, cy)


def find_any_on_screen(
    screenshot: np.ndarray,
    templates: list[tuple[str, np.ndarray]],
    threshold: float = 0.7,
) -> tuple[str, int, int] | None:
    """Try multiple templates, return the first match.

    Args:
        screenshot: OpenCV BGR image
        templates: List of (label, template_image) tuples
        threshold: Minimum match confidence

    Returns:
        (label, x, y) of first match, or None if nothing found.
    """
    for label, template in templates:
        pos = find_on_screen(screenshot, template, threshold)
        if pos is not None:
            return (label, pos[0], pos[1])
    return None


def load_template(template_path: str) -> np.ndarray:
    """Load a template image from disk."""
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if template is None:
        raise FileNotFoundError(f"Template not found: {template_path}")
    return template


async def find_and_click(
    page: Page,
    template_path: str,
    label: str,
    threshold: float = 0.7,
    timeout: float = 10.0,
    interval: float = 0.5,
) -> bool:
    """Take screenshots until template is found, then click its center.

    Args:
        page: Playwright page
        template_path: Path to template image file
        label: Human-readable name for logging
        threshold: Minimum match confidence (0.0 - 1.0)
        timeout: Max seconds to wait before giving up
        interval: Seconds between retry screenshots

    Returns:
        True if found and clicked, False if timed out.
    """
    template = load_template(template_path)
    elapsed = 0.0

    with log_step(log, f"Find and click '{label}'"):
        while elapsed < timeout:
            screenshot = await take_screenshot(page)
            pos = find_on_screen(screenshot, template, threshold)

            if pos is not None:
                log.info(f"Found '{label}' at ({pos[0]}, {pos[1]})")
                await page.mouse.click(pos[0], pos[1])
                return True

            await asyncio.sleep(interval)
            elapsed += interval

        log.warning(f"'{label}' not found after {timeout}s")
        return False


async def wait_for_template(
    page: Page,
    template_path: str,
    label: str,
    threshold: float = 0.7,
    timeout: float = 30.0,
    interval: float = 1.0,
) -> bool:
    """Wait until a template appears on screen (no click).

    Args:
        page: Playwright page
        template_path: Path to template image file
        label: Human-readable name for logging
        threshold: Minimum match confidence (0.0 - 1.0)
        timeout: Max seconds to wait before giving up
        interval: Seconds between retry screenshots

    Returns:
        True if template appeared, False if timed out.
    """
    template = load_template(template_path)
    elapsed = 0.0

    with log_step(log, f"Waiting for '{label}'"):
        while elapsed < timeout:
            screenshot = await take_screenshot(page)
            pos = find_on_screen(screenshot, template, threshold)

            if pos is not None:
                log.info(f"'{label}' appeared at ({pos[0]}, {pos[1]})")
                return True

            await asyncio.sleep(interval)
            elapsed += interval

        log.warning(f"'{label}' did not appear after {timeout}s")
        return False

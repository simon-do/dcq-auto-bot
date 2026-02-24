import json
import time

import pyautogui

CONFIG_PATH = "enter_game_config.json"


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def click_point(point: dict, label: str, delay: float):
    x = point["x"]
    y = point["y"]
    print(f"Click {label} at ({x}, {y})")
    pyautogui.moveTo(x, y)
    pyautogui.click()
    time.sleep(delay)


def main():
    cfg = load_config(CONFIG_PATH)
    pts = cfg["points"]
    delay = cfg.get("delay_between_clicks", 0.5)

    print("enter_game will start in 3 seconds...")
    time.sleep(3)

    # Get coordinates
    # pyautogui.displayMousePosition()

    # P1 -> P5
    click_point(pts["update_popup"], "update_popup (P1)", 2)
    click_point(pts["change_region"], "change_region (P2)", delay)
    click_point(pts["my_server"], "my_server (P3)", delay)
    click_point(pts["target_server"], "target_server (P4)", delay)
    click_point(pts["start_game"], "start_game (P5)", delay)

    print("Done enter_game sequence.")


if __name__ == "__main__":
    main()

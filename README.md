# dcq-auto-bot

Bot tự động đăng nhập và vào game **Gọi Ta Đại Chưởng Quỹ** (webgame) trên trình duyệt, sử dụng **Playwright (Python)**.

Hiện tại bot đã:
- Mở Chrome ở kích thước cố định 500×900.
- Tự động login bằng selector (username / password / nút Đăng nhập).
- Tự động xử lý màn hình chọn server bằng click tọa độ viewport để vào màn hình chính trong game.

---

## Kiến trúc nhanh

- `main.py` — Entry point, khởi chạy browser và chạy tuần tự các task.
- `core/browser/browser.py` — Launch Chromium với viewport 500×900.
- `core/logger.py` — Cấu hình logging với timestamp và đo thời gian mỗi bước.
- `apps/dcq/tasks/login.py` — Điền username / password, click nút Đăng nhập.
- `apps/dcq/tasks/enter_game.py` — Click theo tọa độ viewport: đóng popup, chọn server, bắt đầu game.
- `apps/dcq/config.json` — Tọa độ click cho các bước enter game.

---

## Yêu cầu

- Python 3.11+
- Git

---

## Cài đặt

```bash
git clone https://github.com/simon-do/dcq-auto-bot.git
cd dcq-auto-bot
pip install -r requirements.txt
playwright install chromium
```

## Chạy chương trình

```bash
python main.py
```

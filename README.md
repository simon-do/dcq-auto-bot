# dcq-auto-bot

Bot tự động đăng nhập và vào game **Gọi Ta Đại Chưởng Quỹ** (webgame) trên trình duyệt, sử dụng kết hợp **Puppeteer (Node.js)** và **PyAutoGUI (Python)**.

Hiện tại bot đã:
- Mở Chrome ở kích thước cố định 500×900.
- Tự động login bằng selector (username / password / nút Đăng nhập).
- Tự động xử lý màn hình chọn server bằng click tọa độ để vào màn hình chính trong game.

---

## Kiến trúc nhanh

- `open_game.ts`  
  - Dùng Puppeteer để:
    - Launch Chrome (headless: false).
    - Set viewport 500×900.
    - Mở URL game.
    - Điền username / password.
    - Click nút **Đăng nhập**.

- `enter_game.py` + `config.json`  
  - Dùng PyAutoGUI để click theo tọa độ màn hình (Windows):
    - Đóng popup cập nhật.
    - Chọn server đang chơi.
    - Click nút **Bắt đầu game**.

Bot hiện click theo **screen coordinates**, nên vị trí & kích thước cửa sổ Chrome phải cố định.

---

## Yêu cầu

- Node.js (v22+)
- Python 3.11+
- Git
- Hệ điều hành: Windows (PyAutoGUI + toạ độ màn hình)

---

## Cài đặt

```bash
git clone https://github.com/simon-do/dcq-auto-bot.git
cd dcq-auto-bot
pnpm install
pip install -r requirements.txt
```

## Chạy chương trình

```bash
pnpm run test
python ./enter_game.py
```

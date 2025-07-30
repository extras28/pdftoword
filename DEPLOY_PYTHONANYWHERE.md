# Deploy lên PythonAnywhere - Hướng dẫn

## Bước 1: Đăng ký

1. Truy cập: https://www.pythonanywhere.com
2. Tạo tài khoản miễn phí
3. Free tier: 1 web app, domain: `username.pythonanywhere.com`

## Bước 2: Upload code

1. Vào Dashboard → Files
2. Upload tất cả file của project
3. Hoặc clone từ GitHub:

```bash
git clone https://github.com/[username]/pdf-to-word-converter.git
```

## Bước 3: Cài đặt dependencies

1. Vào Console tab
2. Chạy:

```bash
pip3.10 install --user -r requirements.txt
```

## Bước 4: Cấu hình Web App

1. Vào Web tab → Add new web app
2. Chọn Flask framework
3. Point đến file `app.py`
4. Reload web app

## Ưu điểm:

-   ✅ Dễ setup cho Python
-   ✅ Console để debug
-   ✅ Miễn phí lâu dài

## Nhược điểm:

-   ❌ CPU/RAM hạn chế
-   ❌ Domain không tùy chỉnh được (free)

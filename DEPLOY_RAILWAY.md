# Deploy lên Railway - Hướng dẫn chi tiết

## Bước 1: Chuẩn bị code
1. Tạo tài khoản GitHub (nếu chưa có)
2. Tạo repository mới trên GitHub
3. Upload code của bạn lên GitHub:

```bash
git init
git add .
git commit -m "Initial commit - PDF to Word Converter"
git remote add origin https://github.com/[username]/pdf-to-word-converter.git
git push -u origin main
```

## Bước 2: Deploy lên Railway
1. Truy cập: https://railway.app
2. Đăng ký/đăng nhập bằng GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Chọn repository vừa tạo
5. Railway sẽ tự động detect và deploy!

## Bước 3: Cấu hình (nếu cần)
- Railway sẽ tự động đọc file `railway.toml` 
- App sẽ chạy trên domain miễn phí như: `https://your-app.railway.app`

## Lưu ý:
- Free tier: 500 giờ runtime/tháng
- Đủ cho khoảng 16-20 giờ/ngày
- Nếu hết quota có thể upgrade plan

# Deploy lên Vercel - Hướng dẫn

## Chuẩn bị cho Vercel
Vercel chủ yếu cho serverless functions. Cần tạo file `vercel.json`:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

## Bước deploy:
1. Tạo file `vercel.json` trong thư mục root
2. Truy cập: https://vercel.com
3. Import từ GitHub
4. Deploy tự động

## Ưu điểm:
- ✅ Rất nhanh
- ✅ Global CDN
- ✅ Miễn phí cho personal use

## Nhược điểm:
- ❌ Phức tạp hơn cho Flask app
- ❌ Giới hạn execution time (10s cho free tier)

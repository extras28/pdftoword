# Deploy lên Render - Hướng dẫn chi tiết

## Bước 1: Chuẩn bị
1. Upload code lên GitHub (tương tự Railway)
2. Truy cập: https://render.com
3. Đăng ký/đăng nhập

## Bước 2: Tạo Web Service
1. Click "New" → "Web Service"
2. Connect GitHub repository
3. Cấu hình:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Environment**: Python 3

## Bước 3: Deploy
- Render sẽ tự động build và deploy
- Domain miễn phí: `https://your-app.onrender.com`

## Ưu điểm:
- ✅ Hoàn toàn miễn phí
- ✅ Không giới hạn thời gian runtime
- ✅ SSL tự động

## Nhược điểm:
- ❌ App "ngủ" sau 15 phút không dùng
- ❌ Startup chậm khi app thức dậy (cold start)

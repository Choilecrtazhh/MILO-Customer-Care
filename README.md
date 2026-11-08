# MILO Customer Care — bản Python 3.15

## Bản này thay đổi gì?
Bản này dùng Python thuần (standard library), không cài Rasa và không cần `pip install`.
Lý do: cấu hình Rasa 3.6.20 cũ không tương thích Python 3.15. Chatbot trong bản này là chatbot tư vấn theo nhóm ý định/câu hỏi mẫu, phù hợp làm prototype học tập; không phải mô hình AI tạo sinh và không phải kênh chính thức của Nestlé/MILO.

## Chạy trên macOS
1. Cài Python 3.15.2 từ python.org nếu em muốn dùng phiên bản này.
2. Mở Terminal.
3. Gõ `cd ` (có dấu cách), kéo thư mục `MILO_Chatbot_Python315` vào Terminal, nhấn Enter.
4. Kiểm tra phiên bản: `python3.15 --version`
5. Chạy máy chủ: `python3.15 server.py`
   - Nếu lệnh trên không nhận, thử `python3 server.py` sau khi kiểm tra `python3 --version` hiển thị 3.15.2.
6. Mở Chrome/Safari tại `http://localhost:8000`.
7. Giữ Terminal mở khi dùng website. Nhấn Control+C trong Terminal để dừng.

## Tính năng
- Website responsive tông xanh MILO.
- Danh mục sản phẩm minh họa.
- Chatbot tư vấn: loại sản phẩm, thành phần/dinh dưỡng, cách pha, bảo quản, nơi mua, giá/khuyến mãi, phản ánh sản phẩm và hỗ trợ.
- API nội bộ: `POST /api/chat`, `GET /api/products`, `GET /api/health`.

## Giới hạn và lưu ý
- Ảnh sản phẩm hiện là ảnh placeholder minh họa, không phải ảnh bao bì chính thức.
- Không có giá, tồn kho, khuyến mãi theo thời gian thực.
- Thông tin thành phần/dinh dưỡng phải kiểm tra theo đúng bao bì và SKU.
- Không nhập thông tin cá nhân, dữ liệu thanh toán hoặc thông tin nhạy cảm vào bản demo.
- Đây là sản phẩm học tập độc lập, không đại diện Nestlé/MILO.

## Cấu trúc
- `server.py`: HTTP server + logic trả lời chatbot.
- `frontend/index.html`: giao diện website và khung chat.
- `docs/`: mô tả dự án và kịch bản kiểm thử.

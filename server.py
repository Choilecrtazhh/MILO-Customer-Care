#!/usr/bin/env python3
"""MILO Customer Care demo server. Uses only Python standard-library modules."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent
WEB = ROOT / "frontend"

PRODUCTS = [
    {"id":"ready","name":"MILO uống liền","type":"Thức uống đóng hộp/chai","description":"Dòng MILO pha sẵn, tiện mang theo khi đi học hoặc đi làm.","image":"https://placehold.co/480x320/0b6b3a/ffffff?text=MILO+Ready+to+Drink"},
    {"id":"powder","name":"MILO dạng bột","type":"Bột thức uống lúa mạch","description":"Dạng bột để pha theo hướng dẫn trên bao bì sản phẩm.","image":"https://placehold.co/480x320/0b6b3a/ffffff?text=MILO+Powder"},
    {"id":"less-sugar","name":"MILO ít đường","type":"Tùy chọn sản phẩm theo thị trường","description":"Kiểm tra đúng tên phiên bản và thông tin dinh dưỡng trên bao bì tại nơi bán.","image":"https://placehold.co/480x320/0b6b3a/ffffff?text=MILO+Less+Sugar"},
    {"id":"multipack","name":"MILO dạng lốc/hộp lớn","type":"Quy cách đóng gói","description":"Quy cách và dung tích có thể khác nhau tùy nhà bán lẻ và thị trường.","image":"https://placehold.co/480x320/0b6b3a/ffffff?text=MILO+Multipack"}
]

def answer(message):
    q = message.lower().strip()
    if not q:
        return "Em hãy nhập câu hỏi để MILO hỗ trợ nhé!"
    if any(x in q for x in ["xin chào","chào","hello","hi "]):
        return "Xin chào! Mình là trợ lý tư vấn MILO. Bạn muốn tìm hiểu sản phẩm, cách sử dụng, bảo quản hay nơi mua MILO?"
    if any(x in q for x in ["loại", "có những", "sản phẩm", "dòng milo", "danh mục"]):
        return "MILO có nhiều dạng sản phẩm tùy thị trường, thường gặp như MILO uống liền và MILO dạng bột. Bạn có thể xem danh mục minh họa trên website. Hãy kiểm tra tên, dung tích và bao bì thực tế tại điểm bán."
    if any(x in q for x in ["thành phần", "dinh dưỡng", "calo", "đường", "protein", "dị ứng"]):
        return "Thành phần và giá trị dinh dưỡng có thể khác nhau theo từng phiên bản và dung tích. Bạn vui lòng xem bảng thành phần, thông tin dị ứng và dinh dưỡng trên chính bao bì sản phẩm đang sử dụng. Nếu có dị ứng thực phẩm, hãy hỏi chuyên gia y tế khi chưa chắc chắn."
    if any(x in q for x in ["pha", "cách dùng", "sử dụng", "uống như thế nào"]):
        return "Với MILO dạng bột, hãy làm theo tỷ lệ pha và hướng dẫn ghi trên bao bì của đúng sản phẩm. Với MILO uống liền, dùng trực tiếp theo hướng dẫn bảo quản và hạn sử dụng trên hộp/chai."
    if any(x in q for x in ["bảo quản", "để tủ lạnh", "mở hộp", "hạn sử dụng"]):
        return "Bạn hãy bảo quản theo hướng dẫn trên bao bì, tránh nơi nóng và ánh nắng trực tiếp. Với sản phẩm đã mở, làm theo chỉ dẫn bảo quản sau mở nắp và thời gian sử dụng được nhà sản xuất ghi trên nhãn."
    if any(x in q for x in ["mua ở đâu", "địa chỉ", "siêu thị", "cửa hàng", "đặt mua"]):
        return "Bạn có thể tìm MILO tại siêu thị, cửa hàng tiện lợi hoặc gian hàng trực tuyến uy tín. Tình trạng hàng và giá bán thay đổi theo từng điểm bán; website demo này chưa kết nối dữ liệu tồn kho hoặc đơn hàng."
    if any(x in q for x in ["giá", "khuyến mãi", "ưu đãi", "mã giảm"]):
        return "Giá và khuyến mãi thay đổi theo dung tích, khu vực và nhà bán lẻ. Mình chưa kết nối dữ liệu giá theo thời gian thực, bạn vui lòng kiểm tra tại cửa hàng hoặc gian hàng chính hãng."
    if any(x in q for x in ["khiếu nại", "phản ánh", "lỗi", "hỏng", "móp", "mùi lạ"]):
        return "Mình rất tiếc vì trải nghiệm chưa tốt. Bạn hãy giữ lại bao bì, hạn sử dụng, số lô và hóa đơn (nếu có), đồng thời liên hệ kênh chăm sóc khách hàng chính thức được in trên bao bì để được tiếp nhận. Không nên tiếp tục sử dụng sản phẩm nếu có dấu hiệu bất thường."
    if any(x in q for x in ["nhân viên", "người thật", "tư vấn viên", "liên hệ"]):
        return "Đây là chatbot mô phỏng phục vụ bài tập. Website chưa có kết nối nhân viên trực tiếp. Bạn có thể liên hệ kênh chăm sóc khách hàng chính thức của nhà sản xuất được công bố trên bao bì."
    if any(x in q for x in ["cảm ơn", "thanks"]):
        return "Rất vui được hỗ trợ bạn! Bạn còn muốn tìm hiểu điều gì về MILO không?"
    return "Mình chưa hiểu rõ câu hỏi. Bạn có thể hỏi về: các loại MILO, thành phần, cách pha, bảo quản, nơi mua, giá/khuyến mãi hoặc phản ánh sản phẩm nhé."

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB), **kwargs)

    def _json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self._json({"ok": True})

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/products":
            return self._json({"products": PRODUCTS})
        if path == "/api/health":
            return self._json({"ok": True, "service": "MILO Customer Care"})
        if path == "/":
            self.path = "/index.html"
        return super().do_GET()

    def do_POST(self):
        if urlparse(self.path).path != "/api/chat":
            return self._json({"error": "Not found"}, 404)
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            message = str(payload.get("message", ""))[:1000]
            return self._json({"reply": answer(message)})
        except Exception:
            return self._json({"reply": "Mình chưa xử lý được câu hỏi này. Bạn thử gửi lại nhé."}, 400)

if __name__ == "__main__":
    print("MILO Customer Care đang chạy tại http://localhost:8000")
    print("Nhấn Control + C để dừng máy chủ.")
    ThreadingHTTPServer(("127.0.0.1", 8000), Handler).serve_forever()

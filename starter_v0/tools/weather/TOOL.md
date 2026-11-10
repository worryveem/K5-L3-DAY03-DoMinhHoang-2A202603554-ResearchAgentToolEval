---
name: weather
track: bonus
kind: live_api
provider: Open-Meteo Geocoding + Forecast API
requires_env: []
inputs: [location, country_code, units]
outputs: [location, timezone, units, current, current_units, condition, items]
side_effect: false
---
# weather

Tra thời tiết **hiện tại** của một thành phố bằng API thật, không cần API key
cho mục đích học tập phi thương mại. Điều kiện hiện tại do mô hình thời tiết
cung cấp, không phải số đo trực tiếp tại từng địa chỉ.

## Khi dùng

- User hỏi nhiệt độ, độ ẩm, gió hoặc thời tiết hiện tại tại một thành phố cụ thể.
- Không dùng cho ngày mai, dự báo nhiều ngày, lịch sử hoặc tin tức về thời tiết.
- Chưa có địa điểm: gọi `clarify`, không tự suy ra vị trí người dùng.

## Input

| Tham số | Quy ước |
|---|---|
| `location` | Bắt buộc, chuỗi 2–200 ký tự sau khi bỏ khoảng trắng; tên thành phố, có thể thêm vùng/quốc gia sau dấu phẩy. |
| `country_code` | Tùy chọn, mặc định rỗng. Hai chữ cái ISO, ví dụ `VN`, `US`; được chuẩn hóa thành chữ hoa. |
| `units` | `celsius` (mặc định) hoặc `fahrenheit`. Gió luôn tính bằng km/h. |

## Output và lỗi

- Thành công: địa điểm đã resolve, múi giờ, `current` và `current_units` từ API,
  nhãn WMO tiếng Việt, `items` có `title`, `summary`, `url`, `source`, `date`.
- `items` dùng trực tiếp được với `format`. URL nguồn chứa tọa độ và thông số
  đã truy vấn; timestamp kèm múi giờ ở kết quả để tránh coi dữ liệu là bất biến.
- Không tìm được: `error="location_not_found"`, `items=[]`; hỏi tên khác.
- Resolve địa điểm: ưu tiên tên khớp chính xác (bỏ dấu, khoảng trắng, hoa/thường)
  để loại các kết quả fuzzy như sân bay. Trong các tên khớp, ưu tiên duy nhất
  một thủ đô được API đánh dấu `feature_code=PPLC`; không tự suy ra quốc gia.
- Còn nhiều địa điểm sau bước lọc: `error="ambiguous_location"`, `candidates`, `items=[]`.
  Hỏi người dùng chọn thành phố/vùng/quốc gia rồi gọi lại; không chọn ngẫu nhiên.
- Input sai, thiếu dữ liệu từ upstream, timeout, HTTP 429/5xx hoặc JSON lỗi:
  trả `{tool, error, message, items: []}`, không ném exception ra agent.
- Tối đa 2 HTTP GET mỗi lần thành công, timeout 30 giây/request. Không tự retry
  để tránh nhân số request khi upstream giới hạn truy cập.

## Ví dụ

```python
from tools import TOOL_FUNCTIONS
result = TOOL_FUNCTIONS["weather"](location="Hanoi", country_code="VN")
result_f = TOOL_FUNCTIONS["weather"](location="Singapore", country_code="SG", units="fahrenheit")
```

Câu hỏi mẫu: “Thời tiết hiện tại ở Hà Nội thế nào, dùng độ C?”

Kiểm thử offline: `python -m pytest tests/test_tools_todo.py -k weather -q`.

## Tài liệu API

- [Geocoding API](https://open-meteo.com/en/docs/geocoding-api)
- [Forecast API và bảng mã WMO](https://open-meteo.com/en/docs)
- [Điều khoản và attribution](https://open-meteo.com/en/terms)

Khi hiển thị kết quả, giữ nguồn Open-Meteo và liên kết dữ liệu.

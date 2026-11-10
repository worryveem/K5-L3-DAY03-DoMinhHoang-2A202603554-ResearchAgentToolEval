# Thông tin nhóm và phân công công việc

- **Tên nhóm:** DoMinhHoang
- **Bài tập:** Day 03 — Research Agent Tool Evaluation
- **Repository:** [K5-L3-DAY03-DoMinhHoang-2A202603554-ResearchAgentToolEval](https://github.com/worryveem/K5-L3-DAY03-DoMinhHoang-2A202603554-ResearchAgentToolEval)

## Thành viên

| STT | Họ và tên | Mã học viên | Vai trò |
|---|---|---|---|
| 1 | Phạm Đức Hồng Đức | 2A202603558 | Agent Core, Prompt & Tool Spec |
| 2 | Đỗ Minh Hoàng | 2A202603554 | UI & Live Application |
| 3 | Vũ Đức Tâm | 2A202603522 | Tool Coder A — weather, github_search |
| 4 | Lê Xuân Hạ | 2A202603571 | Testing & Eval Suite |
| 5 | Nguyễn Trung Duy | 2A202603387 | Tool Coder B — deduplicate, citation_audit |


## Phân công công việc

| Phân công | Người phụ trách | Công việc chính | File / sản phẩm bàn giao | Đóng góp báo cáo |
|---|---|---|---|---|
| Agent Core, Prompt & Tool Spec | Phạm Đức Hồng Đức | Viết rules routing; quy định khi nào clarify/search; tối ưu mô tả tool và tham số; quản lý các vòng eval v0 → v1 → v2 → v3 | `artifacts/system_prompt.md`, `artifacts/tools.yaml`, `runs/*.json`, `artifacts/version_log.csv` | B1 — Version Evidence |
| Tool Coder A | Vũ Đức Tâm | Viết hai tool `weather`, `github_search`; xử lý đầu vào/lỗi; viết tài liệu và đăng ký tool | `tools/weather/`, `tools/github_search/`, `tools/__init__.py`, khai báo trong `artifacts/tools.yaml` | A2 — Danh sách tool |
| Tool Coder B | Nguyễn Trung Duy | Viết `deduplicate`, `citation_audit`; xử lý đầu vào/lỗi; viết tài liệu, đăng ký tool và kiểm thử | `tools/deduplicate/`, `tools/citation_audit/`, `tests/test_person3.py`, đăng ký trong `tools/__init__.py` và schema trong `artifacts/tools.yaml` | A2 — Hai tool mới; B5 — Bonus Evidence |
| Testing & Eval Suite | Lê Xuân Hạ | Hoàn thiện unit test cho tool toàn nhóm, tối thiểu 3 test/tool; mock network; viết 10 case eval gồm 5 single-turn và 5 multi-turn; phân tích lỗi thực tế | `tests/test_tools_todo.py`, `analysis/pytest_results.txt` , `data/eval_group.json`, kết quả pytest/eval | B2 — Failure Analysis; B3 — Team Eval Cases |
| UI & Live Application | Đỗ Minh Hoàng | Xây dựng giao diện Streamlit, hiển thị tool call/kết quả Markdown, chọn phiên bản và lưu hội thoại thực tế | `app.py`, `ui.css`, `.streamlit/config.toml`, `assets/fonts/`, `transcripts/*.transcript.json` | A1 — Giới thiệu; A3 — Câu hỏi mẫu; B4 — Live Chat Evidence |

## Phạm vi phần Phạm Đức Hồng Đức - 2A202603558

1. Thiết lập baseline và phân tích lỗi v0
- Chạy đủ 20 case của bộ `base`, lưu kết quả tại `runs/v0_B_base_openai_20261110T110804866669.json`; baseline đạt 14/20 case, case accuracy 0.70.
- Liệt kê và đối chiếu sáu case thất bại của v0: `R08`, `R10`, `R11`, `R12`, `R13`, `R14`; phân loại theo `out_of_scope`, `missing_info`, `wrong_boundary`, `wrong_tool` và kiểm tra thêm `observed_mismatch` để xác định lỗi argument thực tế.
- Ghi mốc baseline, artifact hash, giả thuyết và metric vào `artifacts/version_log.csv`.

2. Tối ưu system prompt ở v1
- Chỉnh sửa `artifacts/system_prompt.md`, loại bỏ các chỉ dẫn xấu của starter như tự đoán thông tin còn thiếu, gửi khi chưa xác nhận và ép mọi yêu cầu vào một bước.
- Bổ sung giới hạn phạm vi research; quy tắc hỏi lại khi thiếu handle/URL; routing giữa `timeline`, `social_search`, `lookup`, `fetch`; xử lý nhiều tool và xác nhận trước hành động gửi.
- Chạy lại bộ base và lưu `runs/v1_B_base_openai_20261110T135423515714.json`; kết quả tăng từ 0.70 lên 0.90, đạt 18/20 case.

3. Hoàn thiện tool declaration ở v2
- Viết lại mô tả các tool trong `artifacts/tools.yaml`, nêu rõ chức năng, khi nào dùng và khi nào không dùng.
- Chuẩn hóa contract tham số: handle không có `@`, `topic=news` cho tin tức, quy ước `timeframe`, `search_type=Top|Latest`, bắt buộc `clarify.response_type`, và `send` chỉ được gọi với `confirmed=true` sau xác nhận.
- Chạy và lưu `runs/v2_B_base_openai_20261110T144126484826.json`; kết quả 18/20 case, case accuracy 0.90.

4. Sửa các lỗi còn lại ở v3
- Cập nhật `artifacts/system_prompt.md` và `artifacts/tools.yaml` để lệnh hủy/chuyển nguồn mới nhất được ưu tiên hơn yêu cầu cũ, không gọi thừa tool đã bị loại bỏ.
- Quy định xác nhận `yes_no` phải diễn ra trước khi hỏi nội dung gửi, khắc phục lỗi boundary của `send`.
- Chạy và lưu `runs/v3_B_base_openai_20261110T144745860762.json`; đạt 20/20 case và 1.00 ở case accuracy, tool routing, argument accuracy và multi-turn accuracy.

5. Quản lý bằng chứng eval và đóng góp báo cáo
- Hoàn thiện các dòng v0 → v3 trong `artifacts/version_log.csv`, gồm artifact version/hash, lý do thay đổi, giả thuyết, metric trước/sau và đường dẫn run.
- Khởi tạo bộ case nhóm trước đó, chạy v3 và lưu `runs/v3_B_group_openai_20261110T151111781188.json` (6/10). Bộ `data/eval_group.json` được cập nhật sau run này; Hạ chạy bộ hiện tại ở v1 và lưu `runs/v1_B_group_openai_20261110T172643256578.json` (9/10). Hai run dùng danh sách case khác nhau nên không so sánh trực tiếp.



## Phạm vi phần Vũ Đức Tâm - 2A202603522

1. Xây dựng tool weather
- Viết implementation tại starter_v0/tools/weather/tool.py.
- Tích hợp Open-Meteo để tìm tọa độ địa điểm và lấy dữ liệu thời tiết hiện tại.
- Hỗ trợ tên thành phố, mã quốc gia và đơn vị nhiệt độ Celsius/Fahrenheit.
- Trả về nhiệt độ, nhiệt độ cảm nhận, độ ẩm, tốc độ gió, trạng thái thời tiết, thời điểm dữ liệu và URL nguồn.
- Xử lý địa danh trùng tên: ưu tiên tên khớp chính xác và kết quả thủ đô được API xác định; trả danh sách lựa chọn nếu vẫn chưa xác định được địa điểm.
- Kiểm tra đầu vào và xử lý các trường hợp không tìm thấy địa điểm, timeout, lỗi HTTP hoặc dữ liệu API không hợp lệ.
- Chuẩn hóa kết quả thành items để sử dụng với tool format.
2. Xây dựng tool github_search
- Viết implementation tại starter_v0/tools/github_search/tool.py.
- Tích hợp GitHub REST API để tìm kiếm repository công khai.
- Hỗ trợ truy vấn theo chủ đề, ngôn ngữ, owner và số sao bằng cú pháp tìm kiếm GitHub.
- Hỗ trợ sắp xếp theo mức độ liên quan, stars, forks hoặc thời điểm cập nhật; giới hạn từ 1 đến 10 kết quả.
- Trả về tên repository, mô tả, URL, stars, forks, ngôn ngữ, license, topics và ngày cập nhật.
- Hỗ trợ GITHUB_TOKEN tùy chọn; token được gửi trong header.
- Kiểm tra tham số đầu vào, xử lý lỗi API và loại bỏ kết quả riêng tư hoặc thiếu thông tin cần thiết.
3. Viết tài liệu cho hai tool
Hoàn thiện hai file:
- starter_v0/tools/weather/TOOL.md
- starter_v0/tools/github_search/TOOL.md
Tài liệu gồm frontmatter đúng contract, chức năng, trường hợp sử dụng, tham số, kết quả trả về, cách xử lý lỗi, ví dụ gọi tool và liên kết tài liệu API.
4. Đăng ký và tích hợp vào agent
- Đăng ký hai hàm trong TOOL_FUNCTIONS tại starter_v0/tools/__init__.py.
- Bổ sung schema trong starter_v0/artifacts/tools.yaml, gồm mô tả chức năng, quy tắc chọn tool, tham số bắt buộc, giá trị mặc định và giới hạn đầu vào.
5. Đóng góp tài liệu và báo cáo
- Bổ sung hai tool vào bảng A2 – Tool agent có trong starter_v0/artifacts/REPORT.md.

## Phạm vi phần Nguyễn Trung Duy - 2A202603387

- `deduplicate`: lọc URL trùng sau khi chuẩn hóa tracking/fragment, giữ nguồn đầu tiên; không so sánh nội dung bài viết.
- `citation_audit`: kiểm tra thiếu `title`, `source`, `url`, URL sai hoặc trùng; không kiểm chứng sự thật hay độ tin cậy của nguồn.
- Test riêng `tests/test_person3.py`: **26 passed** ở lần kiểm tra khi cập nhật B5. Không dùng kết quả này thay điểm eval hay kết quả test toàn nhóm.
- Viết `TOOL.md`, đăng ký hàm trong `tools/__init__.py` và khai báo schema trong `artifacts/tools.yaml` cho hai tool mới.
- Phụ trách mô tả hai tool tại A2 và bằng chứng tại B5 trong `artifacts/REPORT.md`.

## Phạm vi phần Lê Xuân Hạ - 2A202603571
1. Hoàn thiện bộ unit test offline (`starter_v0/tests/test_tools_todo.py`)
- Hoàn thành toàn bộ 14 bài TODO starter cho các tool core và bonus (`clarify`, `format`, `send`, `lookup`, `fetch`, `timeline`, `social_search`, `policy`), sử dụng mock HTTP/network hoàn toàn offline.
- Bổ sung 43 test case kiểm thử cho 4 tool mới của nhóm (vượt mức tối thiểu 3 test/tool):
  - Tool của Vũ Đức Tâm: `weather` và `github_search` (tham số, lỗi đầu vào, chuẩn hóa kết quả, mock HTTP/timeout/lỗi dữ liệu).
  - Tool của Nguyễn Trung Duy: `deduplicate` và `citation_audit` (chuẩn hóa URL/tracking params, không làm biến đổi dữ liệu đầu vào, kiểm tra thiếu `title`/`source`, `invalid_url`, trùng URL và lỗi đầu vào).
- Tổng cộng 57 test case trong `starter_v0/tests/test_tools_todo.py`; sau khi thêm hai test xác nhận UI, toàn bộ bộ test (`pytest tests/ -v`) đạt **168 passed, 0 skipped, 0 failed** (log tại `starter_v0/analysis/pytest_results.txt`).
2. Xây dựng bộ eval case của nhóm (`starter_v0/data/eval_group.json`)
- Viết mới 10 eval case (`G01`–`G10`), gồm 5 single-turn và 5 multi-turn, bao phủ 4 tool mới (`weather`, `github_search`, `deduplicate`, `citation_audit`) và các bẫy routing/argument/boundary thường gặp (`missing_info`, `wrong_tool`, `unnecessary_tool`, sửa constraint và hủy/chuyển tool nhiều lượt).
3. Phần đóng góp Báo cáo(`starter_v0/artifacts/REPORT.md`) Mục B2 (Failure Analysis) và Mục B3 (Team Eval Cases).


## Phạm vi phần Đỗ Minh Hoàng - 2A202603554

1. Xây dựng giao diện web tại `starter_v0/app.py` và `starter_v0/ui.css`
- Tạo khung chat, câu hỏi mẫu, sidebar liệt kê tool và trạng thái kết nối OpenAI; hiển thị câu trả lời bằng Markdown.
- Hiển thị tên tool, tham số JSON, kết quả thực tế và trạng thái từng vòng gọi tool trong hội thoại.
- Cho phép chọn artifact v0–v3, đặt số lượt ngữ cảnh/vòng công cụ và bắt đầu phiên mới.

2. Hoàn thiện trải nghiệm và lưu bằng chứng
- Cấu hình theme Streamlit trong `starter_v0/.streamlit/config.toml`; nhúng font Be Vietnam Pro từ `starter_v0/assets/fonts/` để hiển thị tiếng Việt ổn định.
- Hiển thị câu hỏi `clarify` và nút chọn nhanh cho câu trả lời dạng lựa chọn/xác nhận.
- Với `send`, hiển thị nguyên văn tin nhắn và chỉ gọi tool từ nút xác nhận trên UI; nút hủy kết thúc yêu cầu mà không gửi.
- Bổ sung `starter_v0/tests/test_app_ui.py`: xác minh nút hủy không gọi `send` và nút xác nhận gọi đúng nội dung với `confirmed=True` bằng provider/tool giả, không dùng mạng.
- Lưu mỗi lượt hội thoại vào `starter_v0/transcripts/*.transcript.json`, kèm phiên bản artifact, provider/model, tool calls và kết quả; cho phép tải JSON từ sidebar.

3. Đóng góp báo cáo
- Viết A1 (giới thiệu khả năng agent), A3 (năm câu hỏi thử UI) và B4 (live chat evidence) trong `starter_v0/artifacts/REPORT.md`.
- Đối chiếu các transcript OpenAI được dẫn trong B4 với lượt chat và tool call thực tế; không coi transcript thử nghiệm là điểm eval v3.

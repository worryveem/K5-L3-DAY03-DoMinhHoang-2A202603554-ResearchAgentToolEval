# Báo cáo Research Agent — Day 03

## Thông tin nhóm

- **Nhóm:** DoMinhHoang.
- **Thành viên:** Phạm Đức Hồng Đức, Đỗ Minh Hoàng, Vũ Đức Tâm, Lê Xuân Hạ, Nguyễn Trung Duy.
- **Provider / model đánh giá:** OpenAI / `gpt-4o-mini`.
- **Repository:** [ResearchAgentToolEval](https://github.com/worryveem/K5-L3-DAY03-DoMinhHoang-2A202603554-ResearchAgentToolEval).
- **Phân công chi tiết:** [TEAM.md](TEAM.md).

# PHẦN A — Giới thiệu agent

## A1. Agent này làm được gì

Research Agent hỗ trợ tìm kiếm web, bài đăng công khai trên X/Twitter, đọc URL,
tra cứu paper arXiv, policy nội bộ, thời tiết hiện tại và repository GitHub.
Agent nhận yêu cầu bằng ngôn ngữ tự nhiên, chọn tool phù hợp, xử lý kết quả
và tổng hợp câu trả lời. Khi thiếu thông tin bắt buộc, agent hỏi lại người dùng.

Quy trình xử lý nguồn có thể kết hợp tìm kiếm, lọc URL trùng bằng `deduplicate`
và kiểm tra thông tin trích dẫn bằng `citation_audit`. Hai tool xử lý nguồn
chạy local và không cần API key. Việc kiểm tra trích dẫn đánh giá metadata,
không xác minh tính đúng sai của nội dung hay độ tin cậy của website.

Giao diện Streamlit tại `app.py` có khung chat, câu hỏi mẫu, danh sách tool,
chi tiết từng tool call và kết quả, câu trả lời Markdown, chọn phiên bản v0–v3,
xác nhận đúng nội dung trước khi gọi `send` và tải transcript JSON. Font Be Vietnam Pro được đóng gói trong repository để
hiển thị tiếng Việt. Ứng dụng được kiểm chứng qua hội thoại local; báo cáo sử
dụng run JSON, transcript và unit test làm bằng chứng, không có URL triển khai
public.

## A2. Tool agent có

| Tên tool | Chức năng | Đóng góp |
|---|---|---|
| `clarify` | Hỏi lại khi thiếu dữ kiện hoặc cần làm rõ yêu cầu. | Tool starter |
| `timeline` | Đọc bài đăng gần đây của một tài khoản X/Twitter. | Tool starter |
| `social_search` | Tìm bài đăng công khai theo từ khóa. | Tool starter |
| `lookup` | Tìm nguồn trên web qua Tavily. | Tool starter |
| `fetch` | Đọc nội dung URL qua Firecrawl. | Tool starter |
| `format` | Trình bày dữ liệu đã có thành digest Markdown. | Tool starter |
| `policy` | Tìm thông tin trong policy nội bộ. | Tool starter |
| `papers` | Tìm paper và metadata từ arXiv. | Tool starter |
| `paper_text` | Lấy văn bản paper arXiv để nghiên cứu. | Tool starter |
| `send` | Gửi tin nhắn Telegram sau khi người dùng duyệt đúng nội dung trong giao diện; cần cấu hình bot/chat. | Tool starter, guardrail nhóm |
| `weather` | Tra cứu thời tiết hiện tại theo địa điểm và đơn vị. | Tool mới — Vũ Đức Tâm |
| `github_search` | Tìm repository GitHub công khai theo chủ đề và điều kiện. | Tool mới — Vũ Đức Tâm |
| `deduplicate` | Lọc URL trùng sau khi bỏ tracking/fragment, giữ nguồn đầu tiên. | Tool mới — Nguyễn Trung Duy |
| `citation_audit` | Phát hiện thiếu tên bài, tên nguồn, URL; URL sai định dạng hoặc trùng. | Tool mới — Nguyễn Trung Duy |

Registry và schema khai báo 14 tool, trong đó nhóm bổ sung bốn tool mới.
Phạm Đức Hồng Đức phụ trách prompt/schema và eval; Lê Xuân Hạ phụ trách
kiểm thử và case nhóm; Đỗ Minh Hoàng phụ trách UI và hội thoại tương tác.

## A3. Câu hỏi mẫu để thử
1. “Tìm 3 nguồn về AI agent evaluation, lọc URL trùng rồi kiểm tra thông tin trích dẫn trước khi tổng hợp.”
2. “Thời tiết hiện tại ở Hà Nội như thế nào? Dùng độ C.”
3. “Tìm 3 repository GitHub về RAG, sắp xếp theo số sao giảm dần.”
4. “Tìm paper arXiv về đánh giá AI agent và trả kèm đường dẫn nguồn.”
5. “Lọc hai link https://example.com/ai và https://example.com/ai?utm_source=test, rồi kiểm tra nguồn có tiêu đề Bài AI nhưng chưa có tên nguồn.”

# PHẦN B — Chi tiết và bằng chứng

## B1. Version Evidence

Nguồn bằng chứng: `artifacts/version_log.csv` và các run JSON tương ứng trong `runs/`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Starter cố ý sẽ lỗi ở phạm vi, thông tin bị thiếu, xác nhận gửi và định tuyến nhiều tool. | — | 0.70 | `runs/v0_B_base_openai_20261110T110804866669.json` |
| v1 | `system_prompt.md` | Bỏ chỉ dẫn xấu và thêm ranh giới routing/clarify/send sẽ sửa lỗi tự đoán, gọi tool ngoài phạm vi và sai multi-tool. | 0.70 | 0.90 | `runs/v1_B_base_openai_20261110T135423515714.json` |
| v2 | `tools.yaml` | Description và schema tường minh sẽ sửa lỗi thiếu `response_type` và tăng độ chính xác argument. | 0.90 | 0.90 | `runs/v2_B_base_openai_20261110T144126484826.json` |
| v3 | `system_prompt.md` + `tools.yaml` | Ưu tiên lệnh hủy/chuyển nguồn và xác nhận `yes_no` sẽ loại tool thừa và sửa boundary Telegram còn lại. | 0.90 | 1.00 | `runs/v3_B_base_openai_20261110T144745860762.json` |

Phân tích tác động thay đổi: phần Phạm Đức Hồng Đức chủ động thay đổi ở v1 là `system_prompt.md`, nhưng tools hash cũng đổi từ `5b22a2476d41` ở v0 sang `55b439405a40` ở v1 do đồng bộ tool mới của nhóm. Vì vậy mức tăng 0.70 → 0.90 là bằng chứng của artifact v1 hoàn chỉnh, không được diễn giải là tác động thuần túy chỉ của prompt.

| Phiên bản | Case đạt / tổng | Case accuracy | Tool routing | Argument accuracy | Multi-turn accuracy |
|---|---:|---:|---:|---:|---:|
| v0 | 14/20 | 0.70 | 0.75 | 0.70 | 1.00 |
| v1 | 18/20 | 0.90 | 1.00 | 0.90 | 1.00 |
| v2 | 18/20 | 0.90 | 0.95 | 0.90 | 0.8333 |
| v3 | 20/20 | 1.00 | 1.00 | 1.00 | 1.00 |

Các run trong bảng đều đo đủ 20 case và không có provider error. Run v0
trước đó `runs/v0_B_base_openai_20261110T105415460273.json` có năm provider
error, nên baseline dùng cho so sánh là run đầy đủ trong bảng B1.

## B2. Failure Analysis

Các lỗi dưới đây được đối chiếu từ `results[*].result.failures`, `actual_tool_calls` và `observed_mismatch` trong run JSON.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| v0/R08_out_of_scope | `out_of_scope` | `send` | Câu toán ngoài phạm vi nhưng model dùng `send` như tool trả lời. | Thêm rule ngoài phạm vi: không gọi tool; cấm dùng `send` để trình bày câu trả lời. |
| v0/R10_missing_handle | `missing_info` | `timeline` | Thiếu tài khoản nhưng model tự đoán `sama`. | Thiếu handle phải gọi `clarify(response_type="text")`; không tự chọn tài khoản nổi tiếng. |
| v0/R11_missing_url | `missing_info` | `fetch` | Model tự tạo `https://example.com/article` khi chưa có URL. | Chỉ dùng `fetch` với URL có thật trong hội thoại; thiếu URL phải hỏi `clarify(text)`. |
| v0/R12_confirm_before_send | `wrong_boundary` | `send` | Gọi `send` trước khi người dùng xác nhận. | Bắt buộc hỏi `clarify(response_type="yes_no")` trước mọi hành động gửi/đăng. |
| v0/R13_parallel_web_and_tweets | `wrong_tool` | `lookup`, `social_search` | Đúng hai tool nhưng `lookup.query="AI news"` và thiếu `topic="news"`; mismatch thực tế là `wrong_arg_value`. | Giữ `query="AI"`, tách loại tin vào `topic="news"` và thời gian vào `timeframe="day"`. |
| v0/R14_out_of_scope_coding | `out_of_scope` | `send` | Yêu cầu coding ngoài phạm vi nhưng model tạo code rồi đưa vào `send`. | Không gọi tool cho coding thuần túy và không dùng `send` như output channel. |
| v1/R11_missing_url | `missing_info` | `clarify` | Chọn đúng tool nhưng bỏ `response_type`; expected `text`. | Bắt buộc `response_type` trong schema và mô tả rõ từng enum. |
| v1/R12_confirm_before_send | `wrong_boundary` | `clarify` | Chọn đúng tool nhưng dùng `response_type="text"` thay vì `"yes_no"`. | Nêu rõ xác nhận side effect phải dùng `yes_no`. |
| v2/R12_confirm_before_send | `wrong_boundary` | `clarify` | Model vẫn ưu tiên hỏi nội dung bằng `text` trước xác nhận. | V3 quy định xác nhận `yes_no` luôn là bước đầu tiên, kể cả khi nội dung còn thiếu. |
| v2/M06_switch_tool | `wrong_tool` | `lookup`, `social_search` | `lookup` đúng nhưng gọi thừa `social_search` sau khi người dùng nói bỏ Twitter; mismatch thực tế là `extra_tool_call`. | V3 cho lệnh hủy/chuyển nguồn ưu tiên cao hơn multi-tool và cấm gọi tool đã bị thay thế. |
| v1/G04_weather_vs_news_trap | `wrong_tool` | `lookup`, `social_search` | Đúng `lookup(topic="news", timeframe="day")` nhưng gọi thừa `social_search`; mismatch là `extra_tool_call`. | Củng cố quy tắc chỉ gọi nguồn người dùng yêu cầu; không suy ra cần Twitter từ câu hỏi tin tức. |

## B3. Team Eval Cases

Bộ `data/eval_group.json` có 10 case (5 single-turn, 5 multi-turn), bao phủ
`weather`, `github_search`, `deduplicate`, `citation_audit` và các bẫy định
tuyến/tham số. Run `runs/v1_B_group_openai_20261110T172643256578.json` đạt
**9/10 PASS** (`case_accuracy: 0.9`, `multiturn_accuracy: 1.0`). Đây là run
v1 của bộ nhóm hiện tại. Run v3 cũ
`runs/v3_B_group_openai_20261110T151111781188.json` đạt 6/10 nhưng dùng
**mười case khác** (cùng `dataset_id`, ID/nội dung case không trùng bộ hiện tại),
nên hai điểm không dùng để so sánh tiến bộ v1 → v3.

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| `G01_weather_fahrenheit_routing` | Single-turn (`weather`): phân biệt `weather` với `lookup` và trích xuất `units="fahrenheit"` | `weather(location="Tokyo", units="fahrenheit")` | PASS |
| `G02_weather_missing_location_trap` | Single-turn trap (`missing_info`, `weather`): hỏi thời tiết không có thành phố | `clarify(response_type="text")` (không đoán vị trí) | PASS |
| `G03_github_search_stars_limit` | Single-turn (`github_search`): định tuyến tìm repo sang `github_search` với `sort="stars"`, `max_results=3` | `github_search(sort="stars", max_results=3)` | PASS |
| `G04_weather_vs_news_trap` | Single-turn trap (`wrong_tool`, `weather` vs `lookup`): tin bão/mưa trên báo chí, không gọi `weather` hoặc tool thừa | `lookup(topic="news", timeframe="day")` | FAIL (`extra tool call social_search`) |
| `G05_unnecessary_tool_capabilities_trap` | Single-turn trap (`unnecessary_tool`): hỏi meta về các công cụ `weather`, `github_search`, `deduplicate`, `citation_audit` | `no_tool: true` (trả lời trực tiếp) | PASS |
| `G06_mt_weather_clarify_then_fill` | Multi-turn (3 lượt, `missing_info`, `weather`): bổ sung địa điểm `Seoul` và đơn vị độ C | `weather(location="Seoul", units="celsius")` | PASS |
| `G07_mt_github_correction_sort_limit` | Multi-turn (3 lượt, `wrong_arg_value`, `github_search`): sửa `stars` → `updated` và `5` → `2` | `github_search(sort="updated", max_results=2)` | PASS |
| `G08_mt_deduplicate_existing_items` | Multi-turn (2 lượt, `wrong_tool`, `deduplicate`): lọc trùng URL trên nguồn có sẵn (`removed_count=1`) | `deduplicate` (không gọi `lookup`/`fetch`/`format`) | PASS |
| `G09_mt_citation_audit_existing_items` | Multi-turn (2 lượt, `wrong_tool`, `citation_audit`): kiểm tra metadata trích dẫn lỗi (`missing_title`, `missing_source`, `invalid_url`) | `citation_audit` (không gọi `fetch`) | PASS |
| `G10_mt_switch_weather_to_github` | Multi-turn (2 lượt, `wrong_tool`, `weather` → `github_search`): hủy yêu cầu thời tiết, chuyển sang tìm 2 repo GitHub cập nhật gần nhất về FastMCP | `github_search(sort="updated", max_results=2)` (không gọi `weather`) | PASS |

## B4. Live Chat Evidence

| Hội thoại / lượt | Yêu cầu | Tool thực tế | Kết quả | File bằng chứng |
|---|---|---|---|---|
| Nghiên cứu, lượt 2 | Tìm 3 nguồn về AI agent evaluation. | `papers` | Trả ba nguồn paper, trạng thái `answered`. | `transcripts/v0_openai_20261110T123917769770.transcript.json` |
| Nghiên cứu, lượt 3 | Lọc trùng và kiểm tra trích dẫn các kết quả vừa tìm. | `deduplicate`, `citation_audit` | Giữ ba nguồn, loại 0; metadata không có lỗi, `passed=true`. | `transcripts/v0_openai_20261110T123917769770.transcript.json` |
| Nghiên cứu, lượt 4 | Xử lý danh sách ba nguồn mẫu có tracking và thiếu tên nguồn. | `deduplicate`, `citation_audit` | Từ ba nguồn còn hai, `removed_count=1`; phát hiện `missing_source` ở nguồn có index 1, `passed=false`. | `transcripts/v0_openai_20261110T123917769770.transcript.json` |
| Thời tiết, lượt 1–2 | Hỏi thời tiết chưa có địa điểm, sau đó cung cấp Hà Nội. | `clarify` → `weather` | Hỏi địa điểm trước, sau đó trả một kết quả thời tiết. | `transcripts/v0_openai_20261110T120343293078.transcript.json` |
| Tìm repository, lượt 3 | Tìm repository GitHub về MCP. | `github_search` | Trả năm repository, trạng thái `answered`. | `transcripts/v0_openai_20261110T115237434966.transcript.json` |

Các transcript trên ghi nhận hội thoại OpenAI thử nghiệm trước v3, không phải
run chấm điểm v3. `papers` và hai tool xử lý nguồn đã có lượt chạy thành công;
một số lượt `lookup` gặp lỗi dịch vụ. `citation_audit` chỉ kiểm tra metadata.

## B5. Bonus Evidence

| Đóng góp | Hành vi đã kiểm chứng | Bằng chứng |
|---|---|---|
| `weather` — Vũ Đức Tâm | Chọn tool theo địa điểm, hỏi lại khi thiếu địa điểm; có kết quả thời tiết trong hội thoại thực tế. | `tools/weather/tool.py`, `tools/weather/TOOL.md`, transcript thời tiết ở B4 |
| `github_search` — Vũ Đức Tâm | Tìm repository công khai; hội thoại MCP trả năm kết quả. | `tools/github_search/tool.py`, `tools/github_search/TOOL.md`, transcript GitHub ở B4 |
| `deduplicate` — Nguyễn Trung Duy | Lọc URL trùng, giữ nguồn đầu tiên và không sửa đầu vào. Demo ba nguồn loại được một nguồn trùng. | `tools/deduplicate/tool.py`, `tools/deduplicate/TOOL.md`, transcript nghiên cứu lượt 4 |
| `citation_audit` — Nguyễn Trung Duy | Kiểm tra trường trích dẫn, URL sai/trùng; demo phát hiện `missing_source`. | `tools/citation_audit/tool.py`, `tools/citation_audit/TOOL.md`, transcript nghiên cứu lượt 3–4 |
| Guardrail `send` | Tool chỉ nhận xác nhận từ host cho đúng nội dung; UI hiển thị bản xem trước và nút xác nhận/hủy trước khi thực thi. Hai test UI giả lập xác nhận/hủy, không gửi Telegram thật. | `tools/send/tool.py`, `tools/send/TOOL.md`, `app.py`, `tests/test_person3.py`, `tests/test_app_ui.py` |
| UI Streamlit — Đỗ Minh Hoàng | Chat tương tác, hiển thị tool call và kết quả JSON, render Markdown, chọn v0–v3, lưu/tải transcript; font tiếng Việt đi kèm. | `app.py`, `ui.css`, `.streamlit/config.toml`, `assets/fonts/`, transcript ở B4 |
| Tool unit tests (`tests/`) | Hoàn tất 14 stub core/bonus và 43 test case cho bốn tool mới = **57 test case** trong `test_tools_todo.py`; thêm hai test UI. | `tests/test_tools_todo.py`, `tests/test_app_ui.py`, `analysis/pytest_results.txt` (`pytest tests/ -v`: 168 passed, 0 skipped, 0 failed) |

### Vũ Đức Tâm — Tool thời tiết và tìm repository GitHub

#### Tool `weather`

- **Chức năng:** Tra thời tiết hiện tại theo thành phố bằng Open-Meteo Geocoding và Forecast API.
- **Đầu vào:** `location` bắt buộc; `country_code` ISO hai ký tự tùy chọn; `units` là `celsius` hoặc `fahrenheit`.
- **Đầu ra:** Địa điểm, múi giờ, nhiệt độ, độ ẩm, gió, trạng thái thời tiết và `items` có URL nguồn.
- **Xử lý lỗi và giới hạn:** Báo địa điểm không tìm thấy hoặc mơ hồ; trả error dict khi input sai, timeout, HTTP/API lỗi. Chỉ hỗ trợ thời tiết hiện tại.
- **Ví dụ sử dụng:** `weather(location="Hanoi", country_code="VN", units="celsius")`.
- **Bằng chứng kiểm thử / hội thoại:** `tests/test_tools_todo.py`; transcript thời tiết ở B4.

#### Tool `github_search`

- **Chức năng:** Tìm metadata repository GitHub công khai bằng GitHub REST Search API.
- **Đầu vào:** `query` bắt buộc; `sort` (`best_match`, `stars`, `forks`, `updated`), `order` và `max_results` (1–10).
- **Đầu ra:** `items` chứa tên, mô tả, URL, sao, forks, ngôn ngữ, license, topics và ngày cập nhật.
- **Xử lý lỗi và giới hạn:** Loại repo riêng tư/thiếu URL; trả error dict khi input sai, timeout hoặc API lỗi; `GITHUB_TOKEN` là tùy chọn. Tool không đọc hay chạy mã nguồn.
- **Ví dụ sử dụng:** `github_search(query="RAG language:Python", sort="stars", max_results=3)`.
- **Bằng chứng kiểm thử / hội thoại:** `tests/test_tools_todo.py`; transcript GitHub ở B4.

### Nguyễn Trung Duy — Hai tool xử lý nguồn nghiên cứu

**Mã học viên:** `2A202603387`.

#### Tool `deduplicate` — Lọc nguồn trùng lặp

- **Chức năng:** Lọc URL trùng, giữ nguồn đầu tiên.
- **Đầu vào:** `items`, tối đa 100 nguồn có URL HTTP(S).
- **Đầu ra:** `items`, `input_count`, `removed_count`.
- **Xử lý lỗi và giới hạn:** Trả lỗi khi đầu vào sai; chỉ so sánh URL, không so sánh nội dung.
- **Ví dụ sử dụng:** Hai URL chỉ khác `utm_source` được giữ lại một nguồn.
- **Bằng chứng kiểm thử / hội thoại:** `tests/test_person3.py`; transcript nghiên cứu lượt 4 lọc ba nguồn còn hai.

#### Tool `citation_audit` — Kiểm tra thông tin trích dẫn

- **Chức năng:** Phát hiện thiếu thông tin trích dẫn, URL sai hoặc trùng.
- **Đầu vào:** `items`, tối đa 100 nguồn với các trường `title`, `source`, `url`.
- **Đầu ra:** `item_count`, `issues`, `passed`, `scope`.
- **Xử lý lỗi và giới hạn:** Trả lỗi khi đầu vào sai; không xác minh sự thật hay truy cập URL.
- **Ví dụ sử dụng:** Nguồn thiếu tên nguồn được báo `missing_source`.
- **Bằng chứng kiểm thử / hội thoại:** `tests/test_person3.py`; transcript nghiên cứu lượt 3–4 kiểm tra metadata và phát hiện thiếu nguồn.

#### Tích hợp và giá trị sử dụng

Hai tool chạy local, không cần API key; có `TOOL.md`, đăng ký trong
`tools/__init__.py` và khai báo tại `artifacts/tools.yaml`.
Luồng sử dụng: tìm nguồn → lọc trùng → kiểm tra trích dẫn → tổng hợp.

Transcript bằng chứng: `transcripts/v0_openai_20261110T123917769770.transcript.json`.

### Kết quả kiểm thử và khả năng tái lập

Lệnh chạy từ thư mục `starter_v0`:

```powershell
.\.venv\Scripts\python.exe -X utf8 -m pytest tests/ -q
```

Kết quả tại thời điểm hoàn thiện báo cáo: **168 passed, 0 skipped**.
Unit test chạy offline với mock network, tách biệt với điểm eval lựa chọn
tool/tham số. Chưa có phép đo
riêng tổng số bug được phát hiện, nên báo cáo không gán số bug từ số test.

## B6. Reflection

- **Fix nào thuộc `system_prompt.md`?** Các quy tắc mang tính điều phối toàn cục: giới hạn phạm vi research, khi nào phải hỏi lại thay vì đoán, chọn `timeline`/`social_search`/`lookup`/`fetch`, cho phép nhiều tool, carry và sửa constraint qua nhiều lượt, ưu tiên lệnh hủy/chuyển nguồn, và bắt buộc xác nhận trước hành động gửi.
- **Fix nào thuộc `tools.yaml`?** Các contract gắn với từng tool: mô tả khi dùng/không dùng, handle không có `@`, `topic=news`, quy ước `timeframe`, `search_type=Top|Latest`, bắt buộc truyền rõ `clarify.response_type`, và chỉ cho `send.confirmed=true` sau xác nhận.
- **Failure nào cần manual review?** Ở v2, `M06_switch_tool` được dataset gán `failure_type=wrong_tool`, nhưng JSON cho thấy lỗi quan sát thực tế là `extra_tool_call`: model gọi đúng `lookup` nhưng gọi thừa `social_search`. `R12_confirm_before_send` cũng gọi đúng `clarify`; lỗi thật nằm ở argument `response_type="text"` thay vì `"yes_no"`. Cần đọc `observed_mismatch`, `actual_tool_calls` và `failures` thay vì chỉ nhìn nhãn tổng quát.
- **Sẽ cải thiện gì tiếp theo?** Rà soát expected args của G01/G02/G07 vì eval đang bắt buộc các giá trị đã có default (`celsius`, `desc`), và thiết kế lại G04 để phân biệt câu chữ “tôi xác nhận” với trusted UI approval. Sau đó bổ sung case paraphrase nhằm tránh tối ưu quá sát base eval và so sánh cùng artifact trên model/provider khác để kiểm tra độ ổn định.

## B7. Small Local Model Challenge

Nhóm sử dụng OpenAI `gpt-4o-mini` cho các run được báo cáo. Repository chưa
có run đánh giá Ollama/local model làm bằng chứng so sánh, nên báo cáo không
đưa kết quả hoặc điểm bonus cho hạng mục local model.

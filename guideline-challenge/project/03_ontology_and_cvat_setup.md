# Ontology + CVAT setup

Bảng ontology là **source of truth** cho schema CVAT: `03_cvat_labels.json` phải khớp từng dòng ở đây. Thay mọi
placeholder mới là xong (gate G2).

## Ontology table

| Name | Geometry | Type (class / attribute) | Allowed values | Default | Mutable? | Rationale |
|---|---|---|---|---|---|---|
| `traffic_light` | rectangle | class | — | — | — | Đơn vị instance: mỗi đầu đèn vật lý riêng biệt (housing độc lập). Downstream Behavior Planning cần tọa độ từng đầu đèn để tính xác suất liên quan. |
| `state` | — | attribute của `traffic_light` | `undefined`, `red`, `yellow`, `green`, `off`, `unknown` | `undefined` | true (mutable) | Tách `off` (xác định được đèn tắt hoàn toàn) và `unknown` (không đủ bằng chứng xác định) để downstream phân biệt: đèn tắt vs. ảnh mờ/lóa. Default `undefined` bắt lỗi annotator quên gán. |
| `relevance` | — | attribute của `traffic_light` | `undefined`, `ego_lane`, `other_lane`, `ambiguous` | `undefined` | true (mutable) | Liên quan đến làn xe chủ — attribute rủi ro cao nhất. Default `undefined` để bắt lỗi. Dùng `ambiguous` khi không đủ bằng chứng (không đoán). |
| `shape` | — | attribute của `traffic_light` | `undefined`, `circle`, `arrow`, `other` | `undefined` | false (immutable) | Hình dạng tín hiệu không đổi trong task annotation ảnh tĩnh. Immutable để tránh vô tình thay đổi khi sửa attribute khác. |
| `needs_review` | — | attribute của `traffic_light` | `false`, `true` | `false` | false (immutable) | Flag để annotator đánh dấu object cần QA review thêm (ví dụ: box không chắc, attribute khó xác định). Default `false` — annotator chủ động bật khi cần. |
| `image_escalate` | tag | class (image-level) | — | — | — | Tag image-level khi toàn bộ ảnh cần escalation do điều kiện cực đoan (sương mù dày, góc chụp lạ). Khác với `relevance=ambiguous` ở cấp đầu đèn. |

## Class hay attribute

- **`traffic_light` là class** vì: (1) đây là object type có geometry riêng (bounding box), (2) downstream cần detect và localize từng đầu đèn, (3) QA rule khác nhau cho từng instance (count, IoU).
- **`state`, `relevance`, `shape`, `needs_review` là attribute** vì: thuộc tính của cùng một object, không tạo object mới khi thay đổi. Tách `state` thành class sẽ tạo 6×4×4 = 96 tổ hợp không quản lý được.
- **Tại sao tách `off` và `unknown` thay vì gộp `off_or_unk`:** Downstream AEB cần phân biệt — đèn tắt (`off`) là trạng thái xác định an toàn (không yêu cầu dừng), còn không đọc được (`unknown`) là rủi ro (cần giảm tốc an toàn). Gộp chung mất thông tin này.
- **Default `undefined` có thể gây bias:** Annotator quên gán `relevance` → export ra `undefined` → downstream có thể mặc định `ego_lane` hoặc bỏ qua. `undefined` giữ nguyên để QA bắt được lỗi thiếu giá trị thay vì silently wrong.
- **`needs_review` default `false` (immutable):** Annotator chủ động bật khi nghi ngờ — không để mutable tránh vô tình tắt khi sửa attribute khác cùng lúc.

## CVAT

- **Phiên bản CVAT** (`make cvat-status`): CVAT 2.x (self-hosted, cài từ Day 2)
- **Tên task calibration** (có version guideline): `team03-calib-v1`
- **Guide của task đã dán `02_guideline.md`?** Có — paste toàn bộ nội dung vào tab Guide của task CVAT
- **Nhóm dùng Track hay Shape, vì sao:** Shape — dữ liệu ảnh tĩnh (không có video track), mỗi ảnh được gán độc lập theo mục 2 guideline. Track chỉ cần cho video và sẽ tạo annotation sai format.

## Setup test

**Người test:** Nguyễn Thị My (chưa tham gia setup CVAT task)

**Kết quả:** My mở task `team03-calib-v1` và xác nhận:
- Label gì: `traffic_light` (rectangle) cho từng đầu đèn vật lý, `image_escalate` (tag) nếu cả ảnh cần escalation
- Dùng tool nào: Shape → Rectangle; gán đủ 3 attributes trước khi chuyển ảnh
- Attribute nào: `state` (màu đèn), `relevance` (làn xe chủ), `shape` (hình dạng tín hiệu) — tất cả bắt buộc, không để `undefined` sau khi xem ảnh
- Khi nào escalate: `relevance=ambiguous` khi không xác định được làn; `image_escalate` tag khi cả ảnh không annotate được

**Chỗ vấp:** My ban đầu gộp 2 đầu đèn cùng cột vào 1 box → nhắc lại mục 2 (instance = 1 housing vật lý); sau đó làm đúng. Rule đã rõ trong guideline, không cần sửa.
    
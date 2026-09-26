# QA plan + quality gates

## Flow

Guideline → Calibration → Production → Self-QC → Review → Rework → Quality Gate.

- **Ai review, review bao nhiêu:** Lead annotator (người giữ gold) review 100% ảnh blind set; với production scale, review ngẫu nhiên tối thiểu 20% tổng output, ưu tiên 100% ảnh có tag `critical` hoặc `low_visibility`.
- **Chọn sample theo rule nào:** Ưu tiên theo rủi ro — tất cả ảnh `critical` và `low_visibility` review 100%; ảnh `edge` review 50% (random stratified); ảnh `normal` review 20% (random). Annotator mới: review 50% output trong tuần đầu.
- **Issue được ghi ở đâu, đóng thế nào:** Ghi vào `06_calibration_report.csv` (calibration) hoặc comment trong CVAT task (production). Issue đóng khi annotator đã rework và reviewer xác nhận lại. Issue kiểu `guideline_gap` mở ticket cập nhật guideline ngay.
- **Khi phát hiện guideline gap thì update và version ra sao:** Sửa `02_guideline.md`, tăng version (v1→v2→v3), ghi changelog dòng mới vào `08_revision_log.md`. Calibration phải chạy lại nếu rule thay đổi ảnh hưởng đến attribute `relevance` hoặc `state`.

## Defect severity

Nhóm mapping theo hậu quả downstream cho Behavior Planning / AEB Level 3–4:

| Severity | Định nghĩa cho project này | Ví dụ | Action mặc định |
|---|---|---|---|
| Critical | Lỗi gây AEB sai quyết định: bỏ sót đèn ego_lane, nhầm relevance gây phanh gấp hoặc không phanh | Gán `relevance=other_lane` cho đèn đỏ ego_lane; bỏ sót object ≥24×24px; box geometry sai làm detector out-of-distribution | REJECT — phải rework ngay, không pass dù tỷ lệ thấp |
| Major | Lỗi ảnh hưởng metric model nhưng không gây failure tức thì | Gán `state` sai (red↔green) khi màu rõ; đếm sai số đầu đèn ≥1 instance; box lệch >5px | REWORK — gửi lại reviewer trong ngày |
| Minor | Lỗi nhỏ, geometry hoặc attribute phụ không ảnh hưởng decision chính | Box lệch 2–5px trong tolerance; `shape` gán nhầm circle↔arrow khi đèn tắt | NOTE — ghi lại, accumulate; REWORK nếu ≥3 minor/ảnh |
| Question | Chỗ guideline chưa cover, cần escalation | Cảnh không có trong guideline; làn đường mất hoàn toàn do tuyết che | LOG — mở guideline gap ticket, annotator dùng `ambiguous` tạm thời |

## Metrics

| Metric | Cách tính | Vì sao phù hợp với bài toán |
|---|---|---|
| Critical Defect Escape Rate | Số critical defect không bị bắt / tổng critical defect × 100% | AEB safety-critical: 1 critical escape = 1 tai nạn tiềm năng, phải gần 0% |
| Decision Accuracy | Số decision đúng theo gold / tổng decision × 100% | Đo khả năng chuyển giao guideline qua blind test (= GTS component D) |
| Inter-annotator Agreement (Count) | % ảnh mà mọi annotator đồng thuận số lượng instance | Calibration: count sai là lỗi nền, mọi attribute tiếp theo đều sai |
| Attribute Agreement (Relevance) | % đầu đèn mà mọi annotator đồng thuận `relevance` | Relevance là attribute rủi ro cao nhất — disagreement ở đây = guideline gap về làn |
| Geometry Tolerance Pass Rate | % box có ≤2px lệch mỗi cạnh so với biên vỏ đèn | Geometry ảnh hưởng trực tiếp đến IoU score của object detector downstream |

Metric high-risk tách riêng: **Critical Defect Escape Rate** — threshold 0%; bất kỳ critical escape nào là REJECT toàn batch.

## Quality gate

Threshold là đề xuất của nhóm dựa trên downstream contract AEB Level 3/4 — trade-off giữa throughput và safety.

```text
PASS if:
  Critical Defect Escape Rate = 0%          (không có critical nào lọt qua review)
  Decision Accuracy ≥ 85%                    (≥85% decision khớp gold)
  Inter-annotator Agreement (Count) ≥ 80%   (sau calibration và rule fix)
  Attribute Agreement (Relevance) ≥ 75%     (relevance khó nhất; <75% = guideline gap chưa fix)
  Geometry Tolerance Pass Rate ≥ 90%        (≤10% box bị lệch >2px)

REWORK if:
  Decision Accuracy 70–85%                  (gửi lại annotator với ví dụ cụ thể từ gold)
  Inter-annotator Agreement (Count) 60–80%  (chạy lại calibration sau khi update guideline)
  Geometry Tolerance Pass Rate 80–90%       (reviewer mark từng box lỗi để annotator sửa)

REJECT / ESCALATE if:
  Critical Defect Escape Rate > 0%          (bất kỳ critical escape nào → reject toàn batch)
  Decision Accuracy < 70%                   (guideline không transferable → revise guideline trước khi tiếp tục)
  Attribute Agreement (Relevance) < 60%     (guideline gap nghiêm trọng về relevance → họp nhóm + rewrite rule)
```

Trade-off: Threshold Decision Accuracy 85% (không phải 95%) vì một số edge case có thể có nhiều đáp án đúng (ví dụ `ambiguous` thay cho `ego_lane` ở cảnh không rõ làn). Ưu tiên zero critical escape hơn là accuracy tuyệt đối — safety trumps throughput. Geometry 90% (không phải 100%) vì ±2px tolerance là thực tế với annotator tốc độ cao; dưới 90% mới gây ảnh hưởng IoU đáng kể.

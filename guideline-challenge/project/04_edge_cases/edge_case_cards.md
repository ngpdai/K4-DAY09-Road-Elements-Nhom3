# Edge-case library

Tối thiểu **8 card**, khuyến nghị 10–12. Một edge case tốt là case mà hai annotator hợp lý có thể làm khác nhau nếu
guideline chưa rõ. Tám ảnh dễ có label rõ ràng không được tính là edge-case library.

Cần có đủ độ đa dạng: occlusion / truncation / small-far · ambiguous semantics · conflicting road elements · **một case
critical-risk** · **một case guideline cho phép escalation**.

File này là kho nội bộ của nhóm, **không gửi cho peer**. Card dùng ảnh example/calibration thì chép rule + ví dụ sang
`02_guideline.md` (mục 7 và 9) để peer đọc được. Card về ảnh blind chỉ nằm ở đây, và decision của nó phải có trong
`gold_decisions.csv` trước `make freeze`.

`make status` đếm số dòng `CASE ID:` đã điền (đã thay placeholder). Copy khối dưới cho mỗi case.

---

CASE ID: EC-01
Sample: BDD07 (example)
Scene: Overcast daytime highway — nhiều đầu đèn song song trên một cột
Observation: Một cột đèn có 3 đầu: 1 mũi tên rẽ trái (arrow) + 2 hình tròn (circle). Cả ba cùng màu xanh.
Decision: LABEL — vẽ 3 bounding box riêng biệt
Expected: label=traffic_light x3; đầu arrow: shape=arrow, relevance=other_lane; hai đầu circle: shape=circle, relevance=ego_lane; state=green cho cả 3
Rationale: Mục 2 quy định mỗi đầu đèn vật lý riêng biệt là một instance. Gộp chung → count sai → downstream bỏ sót tín hiệu rẽ trái.
Common mistake: Vẽ 1 box lớn bao cả 3 đầu, hoặc gán relevance=ego_lane cho đầu arrow rẽ trái.
Diversity: ambiguity (multiple lights), conflict (relevance phân biệt)

---

CASE ID: EC-02
Sample: BDD08 (example)
Scene: Clear daytime highway — đèn bị cành cây che một phần
Observation: Đầu đèn bị nhánh cây che ~30% diện tích vỏ bên trên; bóng đèn đỏ vẫn nhìn thấy rõ.
Decision: LABEL — vẽ box ôm phần vỏ nhìn thấy
Expected: label=traffic_light; state=red; box ôm phần vỏ visible (không kéo dài ra phần bị che); relevance=ego_lane
Rationale: Mục 6 — bị che <50% và đèn phát sáng → vẽ box phần visible. Bỏ qua = critical escape.
Common mistake: Bỏ qua vì nghĩ "bị che = không label" hoặc kéo box bao luôn phần bị cành cây che.
Diversity: occlusion

---

CASE ID: EC-03
Sample: BDD18 (blind)
Scene: Clear night city street — đèn tạo quầng sáng lóa (glare/halo)
Observation: Đèn đỏ ban đêm tạo vầng sáng lan rộng gấp 3–4 lần kích thước thực. Khó phân biệt mép vỏ đèn.
Decision: LABEL — box căn theo vỏ đèn ước lượng, KHÔNG theo quầng sáng
Expected: label=traffic_light; geometry: box kích thước ước lượng vỏ thực ≈ kích thước đèn ban ngày cùng loại; state=red; relevance=ego_lane hoặc ambiguous
Rationale: Mục 6 — ban đêm glare box phải căn theo kích thước vỏ đèn thực tế. Box theo quầng sáng làm detector học sai kích thước object.
Common mistake: Kéo box bao toàn bộ quầng sáng (box phình 3–4× so với vỏ đèn thực); hoặc bỏ qua vì không thấy rõ mép.
Diversity: low_visibility, critical (geometry critical)

---

CASE ID: EC-04
Sample: BDD18 (blind)
Scene: Clear night city street — mất vạch kẻ đường trong bóng tối
Observation: Hai cột đèn gần nhau, một bên có mũi tên rẽ phải, một bên tròn. Vạch phân làn mờ hoàn toàn trong bóng tối.
Decision: ESCALATE — relevance=ambiguous cho cả hai đầu đèn tròn
Expected: label=traffic_light x2+ ; đầu tròn: relevance=ambiguous; đầu arrow rẽ phải: relevance=other_lane (arrow chỉ rõ làn)
Rationale: Mục 7 — không đủ bằng chứng xác định làn nào là ego lane → ambiguous. Downstream kích hoạt safe mode.
Common mistake: Đoán mò ego_lane vì xe đang đi thẳng; hoặc gán other_lane cho đèn tròn không có mũi tên.
Diversity: critical, escalation, low_visibility, ambiguity

---

CASE ID: EC-05
Sample: BDD17 (blind)
Scene: Rainy daytime city street — mưa tạo streaks trên kính
Observation: Vệt mưa chạy dọc qua đầu đèn; màu đèn nhìn thấy nhưng bị khuếch tán. Flare nước nhỏ quanh bóng đèn.
Decision: LABEL — vẽ box theo vỏ đèn, không bao vệt mưa
Expected: label=traffic_light; box ôm vỏ đèn ±2px (không kéo theo vệt mưa); state=green hoặc red nếu màu phân biệt được; nếu không rõ: state=unknown
Rationale: Mục 3 — tolerance ±2px. Vệt mưa là artifact, không thuộc vỏ đèn. Mục 6 — nếu màu bị khuếch tán hoàn toàn dùng unknown (đèn đang hoạt động nhưng không đọc được màu); dùng off chỉ khi xác định được đèn tắt hẳn.
Common mistake: Kéo box dọc theo vệt mưa; hoặc đoán màu xanh vì "đang giờ xanh" dù không thấy rõ.
Diversity: low_visibility, edge, geometry

---

CASE ID: EC-06
Sample: BDD24 (blind)
Scene: Snowy daytime city street — tuyết khuếch tán ánh sáng
Observation: Tuyết rơi + đọng tạo màu trắng đục phủ kính camera. Đầu đèn nhìn thấy nhưng màu bị wash-out (chỉ thấy điểm sáng trắng).
Decision: LABEL với state=unknown nếu không phân biệt được màu; hoặc state đúng nếu thấy rõ; state=off chỉ khi xác định được cả cụm tắt hẳn
Expected: label=traffic_light; state=unknown (nếu tuyết làm mờ màu hoàn toàn) HOẶC state=red/green (nếu thấy rõ qua tuyết) HOẶC state=off (nếu xác định đèn tắt hẳn); không đoán màu từ ngữ cảnh thời điểm.
Rationale: Mục 4 — unknown khi không xác định đáng tin cậy màu đang sáng; off khi cụm đèn tắt hoàn toàn. Mục 1 — không tự suy đoán màu từ context.
Common mistake: Gán green vì "ban ngày giờ cao điểm có đèn xanh"; bỏ qua object vì "không thấy rõ".
Diversity: low_visibility, edge, small_far

---

CASE ID: EC-07
Sample: BDD25 (blind)
Scene: Clear dawn/dusk city street — ánh sáng vàng nghiêng xóa vạch kẻ đường
Observation: Ánh mặt trời thấp chiếu xéo tạo bóng dài. Vạch phân làn gần như biến mất trong ánh sáng vàng. Hai đầu đèn cạnh nhau: 1 arrow trái + 1 tròn.
Decision: relevance=ambiguous cho đầu đèn tròn vì không xác định được làn xe chủ
Expected: đầu arrow rẽ trái: relevance=other_lane (mũi tên đã chỉ rõ hướng); đầu tròn: relevance=ambiguous (không rõ điều khiển làn nào khi mất vạch)
Rationale: Mục 7 — ambiguous khi không đủ bằng chứng xác định làn. Mũi tên vẫn là bằng chứng rõ ràng dù mất vạch.
Common mistake: Gán ego_lane cho tất cả vì xe đang đi thẳng; hoặc gán ambiguous cả arrow khi mũi tên thấy rõ.
Diversity: ambiguity, escalation, edge, conflict

---

CASE ID: EC-08
Sample: BDD13 (blind)
Scene: Clear daytime city street — đèn nhỏ/xa trong khung hình
Observation: Bên cạnh đèn gần rõ có thêm 2 đầu đèn nhỏ ở xa đường (~40×15px), khó phân biệt shape và state.
Decision: LABEL nếu ≥12×12px; IGNORE nếu <12×12px
Expected: đầu đèn gần: label đầy đủ; đầu đèn xa đo thực tế — nếu ≥12×12px: label=traffic_light với state và shape tốt nhất có thể thấy; nếu <12px: không tạo box
Rationale: Mục 1 — threshold 12×12px. Mục 5 — đèn phương tiện trong scope dù nhỏ/xa vẫn phải label nếu đủ kích thước.
Common mistake: Label đèn xa <12px; hoặc bỏ qua tất cả đèn xa không cần đo kích thước.
Diversity: small_far, occlusion

---

CASE ID: EC-09
Sample: BDD04 (calibration)
Scene: Partly cloudy daytime city street — đèn đang ở pha chuyển tiếp
Observation: Một đầu đèn vàng (yellow) đang sáng; bên cạnh có đèn đỏ của làn rẽ đang bật.
Decision: LABEL cả hai instance riêng biệt
Expected: đầu đèn vàng ego_lane: state=yellow, relevance=ego_lane; đầu đèn đỏ rẽ: state=red, relevance=other_lane
Rationale: Yellow là trạng thái hợp lệ theo taxonomy. Annotator hay nhầm yellow=unknown vì pha ngắn.
Common mistake: Gán state=unknown cho đèn vàng (yellow rõ ràng không nên dùng unknown); gộp 2 đèn vào 1 box.
Diversity: ambiguity (yellow state), conflict (hai pha cùng lúc)

---

CASE ID: EC-10
Sample: BDD01 (calibration)
Scene: Partly cloudy daytime highway — đèn bị cắt ở mép ảnh
Observation: Một đầu đèn ở góc trên phải ảnh bị viền hình cắt ngang ~40% phần trên.
Decision: LABEL — vẽ box ôm phần còn trong khung hình
Expected: label=traffic_light; box ôm phần nằm bên trong ảnh, cạnh box tiếp giáp mép ảnh; state theo phần nhìn thấy; relevance theo bối cảnh
Rationale: Mục 6 — truncation: vẽ box theo phần trong khung. Không bỏ qua object hợp lệ chỉ vì bị cắt.
Common mistake: Bỏ qua object bị cắt mép; hoặc kéo box ra ngoài giới hạn ảnh.
Diversity: occlusion (truncation)

---

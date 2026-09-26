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
Sample: 000000 (sample_id)
Scene: Giao lộ đô thị, nhiều traffic-light head nằm cạnh nhau trên cùng hướng tiếp cận.
Observation: Một đầu đèn hiển thị mũi tên rẽ trái màu đỏ, bên cạnh là một đầu đèn hình tròn màu đỏ. Hai đầu đèn có cùng trạng thái màu nhưng phục vụ các hướng di chuyển khác nhau.
Decision: LABEL
Expected: Tạo 2 bounding box độc lập, mỗi box ôm housing của một traffic-light head. Đèn mũi tên: class=traffic_light, state=red, shape=arrow, relevance=other_lane nếu ego đi thẳng. Đèn tròn: class=traffic_light, state=red, shape=circle, relevance=ego_lane nếu nó điều khiển luồng đi thẳng của ego.
Rationale: Đây là case kiểm tra việc không suy ra relevance từ state. Hai đèn cùng màu đỏ nhưng có thể điều khiển hai traffic flow khác nhau. Gán nhầm đèn rẽ cho ego có thể làm downstream hiểu sai tín hiệu mà ego phải tuân theo.
Common mistake: Gộp hai đầu đèn thành một box hoặc gán cả hai relevance=ego_lane chỉ vì cả hai đều màu đỏ.
Diversity: conflict / critical / multiple_instances

---

CASE ID: EC-02
Sample: 000005 (sample_id)
Scene: Cùng kiểu giao lộ nhiều đầu đèn, với một đèn mũi tên rẽ trái màu đỏ và một đèn tròn màu xanh. Ego đang tiếp cận giao lộ theo hướng đi thẳng.
Observation: Đèn rẽ trái đang đỏ trong khi đèn tròn bên cạnh đang xanh.
Decision: LABEL
Expected: Đèn mũi tên: class=traffic_light, state=red, shape=arrow, relevance=other_lane. Đèn tròn: class=traffic_light, state=green, shape=circle, relevance=ego_lane. Hai housing được vẽ thành hai bounding box riêng.
Rationale: Đây là critical-risk case vì trạng thái của hai traffic flow khác nhau tại cùng một vị trí. Nếu annotator gán đèn rẽ trái cho ego, downstream có thể nhận sai tín hiệu điều khiển luồng của ego.
Common mistake: Thấy đèn xanh nằm gần đèn đỏ rồi gán relevance theo vị trí gần ego thay vì xác định traffic flow; hoặc gán tất cả đèn nhìn về camera là ego_lane.
Diversity: conflict / critical / multiple_instances

---

CASE ID: EC-03
Sample: 000002 (sample_id)
Scene: Gantry ngang đường với nhiều traffic-light head ở nhiều vị trí, một số đầu đèn có mũi tên và một số đầu đèn hình tròn.
Observation: Nhiều đầu đèn xuất hiện đồng thời, khoảng cách giữa các housing nhỏ; một số cùng hiển thị màu đỏ nhưng hình dạng tín hiệu khác nhau.
Decision: LABEL
Expected: Mỗi housing độc lập là một instance và một bounding box riêng. Không gộp các housing trên cùng gantry. State được xác định riêng cho từng box; shape=arrow nếu tín hiệu mũi tên, shape=circle nếu tín hiệu tròn; relevance được xác định độc lập theo traffic flow.
Rationale: Guideline quy định mỗi traffic-light housing độc lập là một instance. Việc gộp các đầu đèn làm mất thông tin về state/shape/relevance của từng tín hiệu.
Common mistake: Vẽ một bounding box lớn bao trọn toàn bộ gantry hoặc gộp các đầu đèn nằm cạnh nhau.
Diversity: multiple_instances / conflict / geometry

---

CASE ID: EC-04
Sample: 000001 (sample_id)
Scene: Giao lộ có nhiều cây; một số traffic-light head nằm sát hoặc bị che một phần bởi tán cây và phương tiện lớn.
Observation: Một số housing vẫn nhận diện được nhưng background cây che một phần hình dạng/housing; một traffic-light head ở bên phải nằm gần xe bus.
Decision: LABEL
Expected: Với traffic-light head vẫn nhận diện được và đủ evidence, tạo bounding box ôm phần housing nhìn thấy. Không mở rộng box vào vùng cây/xe bus bị che. State lấy từ bóng đèn nếu màu đủ rõ; nếu không xác định được màu thì state=unknown.
Rationale: Annotator phải phân biệt “object bị occlusion” với “object không còn đủ evidence để annotate”. Không được tự đoán phần housing bị che.
Common mistake: Kéo box qua vùng cây để ước lượng toàn bộ housing hoặc bỏ qua object dù vẫn có đủ evidence nhận diện.
Diversity: occlusion

---

CASE ID: EC-05
Sample: 000006 (sample_id)
Scene: Hai traffic-light head màu xanh ở hai phía của cùng đoạn đường, phía dưới có nhiều phương tiện và biển báo giao thông.
Observation: Một traffic-light head có housing nhìn khá rõ; đầu còn lại chỉ có phần tín hiệu phát sáng nổi bật trong vùng cây, housing khó quan sát.
Decision: LABEL / ESCALATE tùy mức evidence
Expected: Nếu đủ evidence xác định phần phát sáng thuộc một traffic-light head trong scope: tạo box theo phần housing nhìn thấy và state=green. Nếu không đủ evidence xác định chính xác housing hoặc không thể phân biệt object với vùng sáng/background: không tự suy đoán; xử lý theo ambiguity/escalation rule.
Rationale: Đây là ranh giới giữa “known object with partial occlusion” và “insufficient evidence”. Nếu annotator không thể chứng minh object là traffic_light thì không được tạo label chỉ dựa trên một vùng sáng.
Common mistake: Nhìn thấy một đốm xanh là lập tức tạo traffic_light; hoặc ngược lại bỏ qua object dù housing vẫn đủ evidence.
Diversity: occlusion / ambiguity / escalation

---

CASE ID: EC-06
Sample: 000003 (sample_id)
Scene: Giao lộ nhìn từ xa, nhiều traffic-light head ở các khoảng cách khác nhau; một số đầu đèn ở xa có kích thước rất nhỏ.
Observation: Có traffic-light head rõ ở foreground và các đầu đèn nhỏ hơn ở background.
Decision: LABEL hoặc IGNORE theo kích thước thực tế
Expected: Traffic-light head có kích thước >=12×12 px và đủ evidence → LABEL. Đối tượng <12×12 px → IGNORE theo guideline v4.
Rationale: Các object rất nhỏ có thể không đủ thông tin để xác định state/shape/relevance đáng tin cậy. Threshold 12×12 px được guideline dùng để tạo boundary nhất quán giữa label và ignore.
Common mistake: Vẫn annotate các điểm sáng rất nhỏ ở xa chỉ vì chúng có màu đỏ/xanh.
Diversity: small_far

---

CASE ID: EC-07
Sample: 000004 (sample_id)
Scene: Giao lộ lớn với nhiều traffic-light head ở nhiều khoảng cách và nhiều hướng; có cả đèn đang sáng và housing tối.
Observation: Nhiều tín hiệu nằm chồng trong cùng vùng nhìn; một số đèn xanh, một số đèn đỏ, một số housing tối/khó xác định trạng thái.
Decision: LABEL / UNKNOWN / IGNORE tùy từng instance
Expected: Mỗi housing đủ evidence được tạo một box riêng. Đèn có màu xác định → state=red/yellow/green. Nếu housing xác định rõ là traffic light và toàn bộ bóng bên trong tắt hoàn toàn → state=off. Nếu xác định được traffic light nhưng không thể xác định đáng tin cậy màu/trạng thái từ ảnh → state=unknown. Đối tượng <12×12 px hoặc không đủ evidence xác định là traffic light → IGNORE.
Rationale: Case này kiểm tra rằng state được quyết định trên từng instance, đồng thời phân biệt rõ `off` (biết chắc toàn bộ bóng tắt) với `unknown` (không đủ evidence để xác định màu/trạng thái).
Common mistake: Gán state của đèn gần đó cho housing tối; gán `unknown` cho một housing rõ ràng đang tắt; hoặc mặc định housing tối là red/green.
Diversity: ambiguity / multiple_instances / off / unknown

---

CASE ID: EC-08
Sample: 000008 (sample_id)
Scene: Hai traffic-light head giống nhau được treo ở hai phía của cùng một giá đỡ; cả hai đang hiển thị đỏ và có bộ đếm số bên trong housing.
Observation: Hai housing có cấu trúc gần như giống nhau, đều có bóng tròn đỏ và hiển thị số đếm.
Decision: LABEL
Expected: Tạo 2 bounding box độc lập, mỗi box bao một housing. Cả hai: class=traffic_light, state=red, shape=circle. Với mỗi instance, phải gán `relevance` độc lập theo traffic flow. Nếu evidence trong ảnh cho thấy cả hai cùng điều khiển luồng ego → cả hai phải được gán `relevance=ego_lane`.
Rationale: Hai object giống nhau về hình dạng và trạng thái nhưng vẫn là hai instance vật lý độc lập. Cùng state không tự động quyết định relevance, nhưng không được bỏ relevance khi ảnh đã đủ evidence để xác định ego flow.
Common mistake: Gộp hai housing thành một box lớn; bỏ relevance; hoặc cho rằng cùng state thì relevance tự động giống nhau mà không kiểm tra traffic flow.
Diversity: multiple_instances / geometry / relevance

---

CASE ID: EC-09
Sample: 000009 (sample_id)
Scene: Ở phía xa có một cụm gồm 3 traffic-light housing riêng biệt.
Observation: Trong cụm 3 housing, 2 đèn đang hiển thị xanh và 1 housing tắt hoàn toàn.
Decision: LABEL / IGNORE tùy kích thước và evidence của từng instance
Expected: Mỗi housing độc lập được đánh giá và annotate riêng. Nếu từng housing đạt `12×12 px` và đủ evidence: tạo 3 bounding box riêng; 2 instance có `state=green`, 1 instance có `state=off`. Gán `relevance` độc lập cho từng instance theo traffic flow. Nếu một housing <12×12 px → IGNORE instance đó; không suy ra state/relevance từ hai đèn còn lại.
Rationale: Case này kiểm tra multiple instances, state độc lập, phân biệt `off` với `unknown`, threshold 12×12 px và relevance độc lập. Không được xử lý cả cụm như một object hoặc suy ra trạng thái của một đèn từ các đèn bên cạnh.
Common mistake: Gộp 3 housing thành một box; cho rằng cả 3 cùng state vì 2 đèn đang xanh; gán `unknown` cho đèn rõ ràng đang tắt; hoặc annotate đèn quá nhỏ chỉ vì vẫn nhìn thấy điểm sáng.
Diversity: multiple_instances / off / green / relevance / small_far

---

CASE ID: EC-10
Sample: 000007 (sample_id)
Scene: Hai traffic-light head màu xanh ở hai phía của cùng đoạn đường, phía dưới có nhiều phương tiện và biển báo giao thông.
Observation: Hai tín hiệu có hình dạng tương tự nhau, đều màu xanh; khoảng cách và vị trí khác nhau khiến annotator có thể không chắc chúng là hai instance độc lập hay một tín hiệu nhìn ở các vị trí khác nhau.
Decision: LABEL
Expected: Mỗi housing nhìn thấy độc lập được tạo một bounding box riêng. Không gộp hai housing. Nếu cả hai đều điều khiển cùng traffic flow của ego → cả hai có thể có relevance=ego_lane; relevance không phải thuộc tính duy nhất cho toàn bộ ảnh.
Rationale: Một giao lộ có thể có nhiều traffic-light head cùng phục vụ một traffic flow. Instance identity phải dựa trên housing vật lý, không dựa trên việc các đèn có cùng state/relevance.
Common mistake: Chỉ annotate một traffic light vì cho rằng các đèn còn lại là duplicate hoặc gán other_lane cho một đèn chỉ vì nó nằm bên trái/phải ego.
Diversity: multiple_instances / ambiguity / geometry

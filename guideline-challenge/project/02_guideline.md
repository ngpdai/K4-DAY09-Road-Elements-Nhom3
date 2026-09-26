# Annotation guideline — Traffic Light State & Ego-Relevance

**Version:** v5

## 1. Objective + scope

- **Mục tiêu:** Gán bounding box 2D và attributes cho các đầu đèn giao thông tại giao lộ phức tạp, tập trung phân biệt trạng thái đèn và mức liên quan đến làn xe chủ trong điều kiện ánh sáng kém. Nhãn phục vụ Behavior Planning và phanh khẩn cấp tự động (AEB) cho xe tự lái cấp độ 3/4.
- **Trong scope (bắt buộc gán nhãn):**
  - Các đầu đèn giao thông phát sáng hoặc tắt dành cho phương tiện giao thông đường bộ, có mặt đèn hướng về phía xe chủ.
  - Kích thước đối tượng tối thiểu là 12 × 12 pixel.
- **Ngoài scope (bỏ qua - Ignore):**
  - Đèn dành riêng cho người đi bộ.
  - Đèn dành riêng cho tàu hỏa hoặc làn xe buýt.
  - Đèn phản quang, biển báo không tự phát sáng, đèn xe khác, đèn chiếu sáng công cộng và hình ảnh phản chiếu.
  - Đối tượng nhỏ hơn 12 × 12 pixel.

## 2. Annotation unit

- **Loại đơn vị:** Bounding Box 2D dạng chữ nhật (`rectangle`) cho từng cụm đầu đèn độc lập (Instance-level).
- **Quy tắc tách instance:** Mỗi đầu đèn vật lý có hộp vỏ (housing) riêng biệt là một instance riêng. Cột đèn có 3 đầu đèn đặt cạnh nhau (ví dụ: 1 đầu rẽ trái, 2 đầu đi thẳng) phải được gán thành 3 bounding box riêng biệt, không gộp chung vào 1 box lớn.
- **Dạng dữ liệu:** Gán từng ảnh tĩnh bằng `Shape`; mỗi đầu đèn là một instance độc lập. Không tạo track.

## 3. Geometry rule

- **Quy chuẩn Bounding Box:**
  - Dạng hình học: `rectangle` (2D axis-aligned bounding box).
  - Độ bao phủ: Box ôm sát phần vỏ đèn nhìn thấy, bao gồm chụp che nếu có.
  - Không bao gồm chân đế, cột đỡ hoặc dây treo.
  - Dung sai cho phép (tolerance): Độ lệch mép box không vượt quá 2 pixel ở mỗi cạnh so với biên vật lý của vỏ đèn. Không được cắt lẹm vào bóng đèn phát sáng và không để chừa khoảng trống nền trời/cây cối quá 2 pixel.

## 4. Taxonomy

Cấu trúc taxonomy gồm 1 Class duy nhất và 3 thuộc tính (Attributes) bắt buộc:

- `undefined` là giá trị dùng khi trường attribute chưa có giá trị trong dữ liệu đầu vào. Không dùng `undefined` thay cho quyết định khi đã xem ảnh: màu/trạng thái không rõ dùng `unknown`, làn không rõ dùng `ambiguous`, hình dạng không rõ dùng `other`.

### Class: `traffic_light` (Shape: rectangle)

### Attribute 1: `state` (Trạng thái phát sáng của đèn)
- `undefined`: Dữ liệu đầu vào chưa có giá trị `state`.
- `red`: Đèn đang bật bóng đỏ (yêu cầu dừng).
- `yellow`: Đèn đang bật bóng vàng (chuẩn bị dừng / chuyển pha).
- `green`: Đèn đang bật bóng xanh (được phép di chuyển).
- `unknown`: Không thể xác định đáng tin cậy màu/trạng thái đang sáng từ bằng chứng hình ảnh.
- `off`: Cả cụm đèn không sáng bóng nào.
- Chọn `unknown` khi bằng chứng hình ảnh không đủ để xác định màu; không tự suy đoán. Chỉ chọn `off` khi xác định được cả cụm đèn đang tắt.

### Attribute 2: `relevance` (Độ liên quan đối với làn xe chủ)

- `undefined`: Dữ liệu đầu vào chưa có giá trị `relevance`.
- `ego_lane`: Đèn điều khiển làn đang đi (xe đi thẳng, đi rẽ,...).
- `other_lane`: Đèn điều khiển một làn phương tiện đường bộ khác với làn xe chủ, ví dụ đèn rẽ trái khi xe chủ đi thẳng.
- `ambiguous`: Không rõ làn (mất vạch kẻ đường, xe đang đè vạch chuyển làn, góc chụp quá xéo hoặc nhiều đèn san sát không rõ tương quan). Tuyệt đối không đoán mò.
- Không mặc định `ego_lane`: phải dựa trên hướng mặt đèn, mũi tên, vạch/làn đường và ngữ cảnh giao lộ.

### Attribute 3: `shape` (Hình dạng tín hiệu)

- `undefined`: Dữ liệu đầu vào chưa có giá trị `shape`.
- `circle`: Bóng đèn tròn đặc thông thường (kể cả khi đèn tắt nhưng mặt kính tròn trơn).
- `arrow`: Tín hiệu hình mũi tên chỉ hướng (rẽ trái/phải, đi thẳng; kể cả khi đèn tắt nhưng thấy rõ khuôn mũi tên).
- `other`: Dạng khác (đèn đếm giây, chữ X, hoặc bị lóa/che khuất không rõ hình dạng tròn hay mũi tên).

## 5. Inclusion / exclusion

### Bắt buộc gán nhãn (Inclusion):
- Mọi đầu đèn phương tiện giao thông phía trước hướng di chuyển của xe.
- Đèn đang sáng hoặc đang tắt, có kích thước ít nhất 12 × 12 pixel.
- Đèn bị che khuất một phần bởi cành cây, biển báo, xe tải nhưng vẫn nhận diện được tối thiểu 50% diện tích vỏ hoặc nhìn rõ bóng đèn phát sáng.

### Bỏ qua hoàn toàn (Exclusion):
- Đèn người đi bộ, đèn tàu hỏa và đèn dành riêng cho làn xe buýt.
- Đèn không hướng mặt về phía xe chủ hoặc không nhận diện được là đầu đèn giao thông thuộc scope.
- Đối tượng nhỏ hơn 12 × 12 pixel.
- Đèn phản quang, biển báo không tự phát sáng và vùng phản chiếu trên mặt đường, nắp capo hoặc kính.

## 6. Visibility / occlusion

- **Bị che khuất một phần (Occlusion):**
  - Nếu đầu đèn bị che khuất < 50% diện tích (ví dụ bị cành cây mảnh, dây điện che ngang): Vẽ box ôm sát phần vỏ nhìn thấy (visible part).
  - Nếu bị che > 50% nhưng bóng đèn đang phát sáng rõ rệt: Vẫn vẽ box bao quanh phần nhìn thấy của bóng đèn và vỏ đèn.
  - Nếu bị che > 50% và đèn tắt (không thể nhận diện rõ cấu trúc cụm đèn): Bỏ qua (Ignore).
- **Bị cắt ở mép ảnh (Truncation):** Nếu đầu đèn bị viền ảnh cắt ngang, vẽ box ôm sát phần nằm bên trong khung hình ảnh.
- **Điều kiện ban đêm và lóa đèn (Low Visibility / Glare):**
  - Ban đêm đèn phát sáng tạo vầng hào quang (halo/glare) tỏa rộng: Bounding box phải căn theo kích thước thực tế của vỏ đèn (hoặc ước lượng kích thước bóng đèn thực tế), **không** được vẽ bao trọn toàn bộ quầng sáng lóa tỏa ra bầu trời.
  - Nếu ánh sáng chói làm mờ hoàn toàn màu sắc: Đặt `state = unknown`.

## 7. Ambiguity / escalation

Quy định chuẩn hóa 4 mức quyết định để đảm bảo thể hiện minh bạch trong export CVAT:
1. **LABEL:** Đủ bằng chứng hình ảnh -> Vẽ box `traffic_light` và chọn các giá trị tương ứng (`state`, `relevance`, `shape`).
2. **IGNORE:** Đối tượng nằm ngoài scope hoặc nhỏ hơn 12 × 12 pixel -> Không tạo bounding box.
3. **UNKNOWN:** Khi nhận diện được đầu đèn nhưng không thể xác định màu/trạng thái đang sáng -> Gán `state = unknown`; nếu không phân biệt được hình dạng thì gán `shape = other`.
4. **ESCALATE / AMBIGUOUS:**
  - Nếu không đủ bằng chứng xác định đèn điều khiển làn nào: Đặt `relevance = ambiguous`, không đoán.
  - Downstream nhận `relevance = ambiguous` sẽ áp dụng quy tắc an toàn: giảm tốc và tăng khoảng cách an toàn.

## 8. Dữ liệu và định dạng đầu ra

- Gán nhãn 20 ảnh có đèn giao thông từ tập S2TLD 720x1280: [Kaggle dataset](https://www.kaggle.com/datasets/sovitrath/s2tld-720x1280-traffic-light-detection-xml-format/data).
- Mỗi ảnh được gán độc lập dưới dạng `Shape`; không áp dụng quy tắc track theo thời gian.
- Export CVAT ở định dạng Datumaro hoặc CVAT XML. Mỗi nhãn `traffic_light` phải có đủ `state`, `relevance` và `shape`.
- Giá trị theo contract: `state` (`undefined`, `red`, `yellow`, `green`, `unknown`, `off`), `relevance` (`undefined`, `ego_lane`, `other_lane`, `ambiguous`), `shape` (`undefined`, `circle`, `arrow`, `other`).
- Kết quả quyết định phải thể hiện được: LABEL (`traffic_light` cùng đủ attributes), IGNORE (không tạo box), UNKNOWN (`state = unknown`) hoặc ESCALATE (`relevance = ambiguous`).

## 9. Examples

Bổ sung ví dụ kèm `sample_id` sau khi chọn ảnh trong tập 20 ảnh; không tự tạo sample ID hoặc bằng chứng calibration.

| sample_id | Thấy gì | Expected output | Rule áp dụng |
|000016|Thấy 3 đèn giao thông|3 box gán cho 3 cụm đèn,2 ego_lane,1 other lane|Taxonomy,Geometry rule|


## 10. Common mistakes

1. **Gộp chung nhiều đầu đèn vào một box:** Vẽ 1 box lớn ôm cả cụm. *Khắc phục: Mỗi đầu đèn vật lý là một instance và một bounding box riêng.*
2. **Nhầm lẫn đèn làn rẽ thành đèn làn xe chủ:** Nhìn thấy đèn xanh bật ở làn rẽ trái liền gán `relevance = ego_lane`. *Khắc phục: Quan sát kỹ vạch kẻ đường, mũi tên trên mặt đường và hình dạng bóng đèn (shape=arrow) để xác định đúng làn.*
3. **Vẽ box phình to theo quầng sáng lóa ban đêm:** Kéo box rộng gấp 3 lần kích thước thật của đèn vì ánh hào quang ban đêm. *Khắc phục: Căn chỉnh viền box theo mép vỏ đèn hoặc đường kính bóng đèn thật.*
4. **Bỏ qua giới hạn kích thước hoặc loại đèn ngoài scope:** *Khắc phục: Chỉ gán đèn giao thông đường bộ hướng về xe chủ và có kích thước tối thiểu 12 × 12 pixel; bỏ qua đèn người đi bộ, tàu hỏa và làn xe buýt.*

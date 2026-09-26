# Problem statement + downstream contract

Tối đa nửa trang, viết **trước khi mở CVAT**. Đây là bằng chứng của gate G1 (topic lock). Thay mọi placeholder
mới là xong.

## Bài toán

Gán nhãn Bounding Box 2D và Attributes cho các đầu đèn giao thông (Traffic Lights) tại các giao lộ phức tạp có nhiều đầu đèn song song, giải quyết điểm khó về phân định màu tín hiệu và độ liên quan trực tiếp đến làn đường của xe chủ trong điều kiện ánh sáng kém.

## Downstream contract

1. **Downstream task / model / user là ai?** Module Lập kế hoạch hành vi (Behavior Planning) và Phanh khẩn cấp tự động (AEB) của hệ thống lái tự động Cấp độ 3/4.
2. **Output annotation nào thực sự cần?**
   - Geometry: 2D Bounding Box ôm sát phần vỏ thấy được của đầu đèn.
   - Class: `traffic_light`
   - Attributes: `state` (`undefined`/`red` / `yellow` / `green` / `unknown`/`off`), `relevance` (`undefined`/`ego_lane` / `other_lane` / `ambiguous`), `shape` (`undefined`/`circle` / `arrow` / `other`).
3. **Failure nào gây hậu quả lớn nhất?**
   - Gán nhãn `relevance = ego_lane` cho đèn rẽ trái đang đỏ trong khi xe chủ đi thẳng đang có đèn xanh riêng $\rightarrow$ Xe phanh gấp giữa giao lộ gây tai nạn phía sau.
   - Bỏ sót (Missed detection) hoặc gán `relevance = other_lane` cho đèn `ego_lane` đang đỏ $\rightarrow$ Xe lao vào giao lộ gây tai nạn trực diện (Critical Escape).
4. **Khi ambiguity không resolve được, ai / ở đâu là escalation path?** Khi không đủ chứng cứ thị giác để xác định đèn điều khiển làn nào, annotator bắt buộc gán attribute `relevance = ambiguous`. Hệ thống downstream khi nhận nhãn `ambiguous` sẽ tự động kích hoạt quy tắc an toàn (giảm tốc và tăng khoảng cách an toàn).

## Scope

- **Trong scope (bắt buộc label):** Tất cả các đầu đèn giao thông phát sáng hoặc tắt dành cho phương tiện giao thông đường bộ có mặt đèn hướng về phía xe chủ.
- **Ngoài scope (ignore):** Đèn giao thông dành riêng cho người đi bộ (biểu tượng hình người), đèn giao thông cho tàu hỏa/xe bus làn riêng, đèn phản quang/biển báo không tự phát sáng, và các mắt đèn nhỏ/xa kích thước dưới $12 \times 12\text{ px}$.
- **Geometry tolerance:** Box ôm sát phần vỏ đèn nhìn thấy được, lệch $\le 2\text{ px}$ mỗi cạnh là đạt; không vẽ thừa ra phần chân đế hoặc dây treo.

## Output chấm được

Trong file export CVAT (định dạng Datumaro / CVAT XML), mọi quyết định được phản ánh qua:
- **LABEL:** Class `traffic_light` kèm đầy đủ 3 attributes (`state`, `relevance`, `shape`).
- **IGNORE:** Không vẽ Bounding Box cho các đối tượng thuộc "Ngoài scope".
- **UNKNOWN:** Class `traffic_light` với attribute `state = off_or_unk`.
- **ESCALATE:** Class `traffic_light` với attribute `relevance = ambiguous`.

## Dữ liệu và giới hạn
Sử dụng 10 trong số 20 ảnh có đèn giao thông từ nguồn (https://www.kaggle.com/datasets/sovitrath/s2tld-720x1280-traffic-light-detection-xml-format/data) 

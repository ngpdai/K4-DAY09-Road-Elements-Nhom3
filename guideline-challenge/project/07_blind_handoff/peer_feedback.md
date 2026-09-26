# Peer feedback + owner response

Phần 1 do **nhóm peer** trả lời (gửi kèm file export). Phần 2 do **nhóm owner** điền. Thay mọi placeholder mới
là xong (gate G5).

- **Nhóm peer:** Nhóm 8
- **Người label blind:** Nhóm 8 annotator team

## 1. Peer trả lời

1. Rule nào rõ nhất / giúp quyết định nhanh nhất? Quy định phân tách mỗi housing là một instance độc lập và ngưỡng kích thước 12×12 px.
2. Rule nào mơ hồ hoặc phải tự suy diễn? Phân định relevance cho các đầu đèn rẽ mũi tên khi nằm chung một cụm với đèn tròn đi thẳng.
3. Sample nào khiến guideline "vỡ"? Sample 000000 (giao lộ ngã tư có cả đèn arrow rẽ trái và đèn tròn đi thẳng cùng màu đỏ).
4. Attribute / default nào trong CVAT dễ gây thao tác sai? Thuộc tính relevance và shape khi nhìn từ xa dễ nhầm giữa circle và other.
5. Một thay đổi cụ thể giúp annotator mới ít hỏi hơn? Thêm ví dụ trực quan về đèn mũi tên rẽ trái luôn thuộc other_lane khi xe chủ đi thẳng.

## 2. Owner phân loại

Owner không tranh luận để bảo vệ guideline. Mỗi feedback và mỗi decision peer làm sai được xếp vào một hướng xử lý.

| Feedback / decision sai | Nguyên nhân (guideline gap / data ambiguity / execution error) | Xử lý (accept + revise / reject with evidence / add escalation rule) | Bằng chứng |
|---|---|---|---|
| Sample 000000 (d2): Peer gán ego_lane cho cả đèn arrow rẽ trái thay vì other_lane | guideline_gap | accept + revise | Bổ sung rule và ví dụ minh họa giao lộ rẽ trái vào Mục 7 và Mục 9 của guideline |
| Feedback peer: Cần làm rõ ranh giới state=unknown vs state=off trong điều kiện mờ | guideline_gap | accept + revise | Đã bổ sung định nghĩa phân biệt rõ off (tắt hẳn) vs unknown (mờ) vào Guideline v5 |

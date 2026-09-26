# Team

Điền trước phút 15. Thay mọi placeholder; còn sót thì `make status` báo ở gate G1.

- **Team:** team03
- **Nhóm peer test bài của mình:** teamG04T031
- **Nhóm mình test bài của:** teamG04T031
- **Problem family:** Traffic light (state, relevance, direction)
- **Nguồn ảnh:** Lấy 10 mẫu ảnh từ trên mạng (https://www.kaggle.com/datasets/sovitrath/s2tld-720x1280-traffic-light-detection-xml-format/data)

| Thành viên | GitHub | Vai trò chính | File phụ trách |
|---|---|---|---|
| Nguyễn Phúc Đại | @ngpdai | Team Lead & Data Architect | `00_team.md`, `01_problem_statement.md` |
| Nghiêm Việt Quân | @Quan1242 | Guideline Specialist | `02_guideline.md`, `08_revision_log.md` |
| Trần Anh Duẩn | @duan-developer | CVAT & System Admin | `03_ontology_and_cvat_setup.md`, `03_cvat_labels.json`, `sample_pack.csv`, `09_cvat_export_or_task_reference.txt` |
| Ngô Văn Hưng | @ngohung01 | Gold Standard Annotator | `04_edge_cases/gold_decisions.csv`, `04_edge_cases/edge_case_cards.md` |
| Nguyễn Thị My | @nguyenmy133 | QA & Internal Auditor | `05_qa_plan.md`, `06_calibration_report.csv`, `07_blind_handoff/clarification_log.csv`, `07_blind_handoff/peer_feedback.md` |

Gợi ý chia vai (nhóm 2–3 người thì gộp): **spec owner** (`01`, `02`), **CVAT owner** (`03_*`, `sample_pack.csv`,
`09`), **gold owner** (`04_edge_cases/`), **QA owner** (`05`, `06`, `07_blind_handoff/`). Mỗi file một người sửa
chính để tránh xung đột git. Calibration thì mọi người cùng label.

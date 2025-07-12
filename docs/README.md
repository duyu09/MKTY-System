## 说明文档

>如有需要，请自行将本文档翻译成您的母语。本文恕不提供除简体中文之外其它语言的版本。
>
>If necessary, please translate this document into your native language by yourself. This document is not available in any language other than Simplified Chinese.
>
>Nếu cần, vui lòng tự dịch tài liệu này sang ngôn ngữ mẹ đẻ của bạn. Tài liệu này không có phiên bản nào khác ngoài tiếng Trung giản thể.

**项目名称：** 明康慧医——基于LLM与多模态人工智能的健康管理与辅助诊疗系统的设计与实现（简称: 明康慧医智慧医疗系统）

英文：Minh Khoe Tue Y — Design and Implementation of a Health Management and Diagnostic Assistance System Based on LLMs and Multimodal Artificial Intelligence (Abbreviation: MKTY Smart Healthcare System)

越南文：Minh Khỏe Tuệ Y  – Thiết kế và triển khai hệ thống quản lý sức khỏe và hỗ trợ chẩn đoán y tế dựa trên LLM và trí tuệ nhân tạo đa mô thức (Tên viết tắt: MKTY – Hệ Thống Y Liệu Trí Tuệ)

-----

此目录下包含本项目的毕业论文PDF文档与答辩用演示文稿PDF文档。这两份文档展示了项目的详细内容，旨在帮助使用者更好地理解项目的设计背景与核心逻辑。

本人欢迎任何形式的学习、借鉴与启发使用，特别是用于帮助项目使用者快速了解项目架构、实现机制或拓展构想。但请注意，这些文档作为项目的重要组成部分，仍受本项目所采用的修改版 `MPL-2.0` 协议约束。

请尊重创作劳动，严禁大篇幅抄袭、拼凑性剽窃或未标注引用的大量使用。如果您想引用或转载文档中的内容，请遵循开源协议，并在显著位置注明原项目（简体中文：明康慧医；英文：Minh Khoe Tue Y；越南文：Minh Khỏe Tuệ Y）、作者信息【项目与论文作者：杜宇（英文：Du Yu；越南文：Đỗ Vũ）；院校方指导教师：副教授 姜文峰（英文：Jiang Wenfeng；越南文：Khương Văn Phong）；企业方指导教师：高级软件工程师 李君（英文：Li Jun；越南文：Lý Quân）】以及论文与项目代码开源链接：[https://github.com/duyu09/MKTY-System](https://github.com/duyu09/MKTY-System)。

希望这份资料能为您带来启发，也感谢您的尊重与支持。

------

**著作权声明**

- 文件`MKTY-Paper.pdf`：齐鲁工业大学（山东省科学院）计算机科学与技术学部 2025届本科毕业设计论文，题目：《基于LLM与多模态人工智能的健康管理与辅助诊疗系统的设计与实现》
- 文件`MKTY-PPT`：齐鲁工业大学（山东省科学院）计算机科学与技术学部 2025届本科毕业设计论文答辩及推优答辩演示文稿
- 论文及演示文稿作者（所有权利持有者）：齐鲁工业大学（山东省科学院）计算机科学与技术学部 软件工程（软件开发）2021级（2025届）本科毕业生 杜宇（英文：Du Yu；越南文：Đỗ Vũ），学号No.202103180009
- 论文及项目指导教师：本人专业为校企合作专业，该论文及项目由院校和企业两单位共同执行指导。
    - 院校单位：齐鲁工业大学（山东省科学院）计算机科学与技术学部（英文：Faculty of Computer Science and Technology, Qilu University of Technology (Shandong Academy of Sciences)；越南文：Học bộ Khoa học và Kỹ thuật Máy tính, Đại học Công nghiệp Tề Lỗ (Viện Khoa học tỉnh Sơn Đông)）；
    - 企业单位：安博教育科技集团 山东师创软件实训学院（英文：Shandong Strong Software Training College, Ambow Education Group；越南文：Học viện Thực huấn Phần mềm Sư Sáng Sơn Đông, Tập đoàn Khoa kỹ Giáo dục An Bác）；
    - 院校方指导教师：副教授 姜文峰（英文：Jiang Wenfeng；越南文：Khương Văn Phong）；
    - 企业方指导教师：高级软件工程师 李君（英文：Li Jun；越南文：Lý Quân）
- 论文的授权说明页中已授权齐鲁工业大学（山东省科学院）关于本项目的论文及代码的多项权利，授权页中的内容如下：`本毕业设计（论文）作者完全了解学校有关保留、使用毕业设计（论文）的规定，即：学校有权保留、送交设计（论文）的复印件，允许设计（论文）被查阅和借阅，学校可以公布设计（论文）的全部或部分内容，可以采用影印、扫描等复制手段保存本设计（论文）。`（翻译版本仅供参考，以简体中文版为准）
- 此毕业论文及答辩用演示文稿的所有权利属于项目作者，即：杜宇。

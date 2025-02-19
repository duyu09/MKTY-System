<p align="center">
  <br>
  <img src="./image/mkty_cn_dark.svg#gh-dark-mode-only" style="width:60%;">
  <img src="./image/mkty_cn_light.svg#gh-light-mode-only" style="width:60%;">
</p>
<br>

# _Minh Khỏe Tuệ Y_ - Hệ Thống Y Tế Trí Tuệ

**Ngôn Ngữ Tài Liệu**

[**简体中文**](./README.md) | [**English**](./README_EN.md) | [**Tiếng Việt**](./README_VN.md)

Xin lưu ý rằng các phiên bản tiếng Anh và tiếng Việt của tài liệu này đều được dịch từ phiên bản tiếng Trung với sự hỗ trợ của LLM và có chỉnh sửa thủ công, tuy nhiên có thể có sai sót. Nếu có sự không nhất quán giữa các phiên bản tiếng Anh hoặc tiếng Việt và phiên bản tiếng Trung, phiên bản tiếng Trung sẽ được ưu tiên.

**Tên dự án:** Minh Khỏe Tuệ Y - Thiết kế và triển khai hệ thống quản lý sức khỏe và hỗ trợ chẩn đoán y tế dựa trên LLM và trí tuệ nhân tạo đa mô thức ( **Tên viết tắt:** Minh Khỏe Tuệ Y Hệ Thống Y Tế Trí Tuệ, **Tiếng Trung:** 明康慧医 - 基于LLM与多模态人工智能的健康管理与辅助诊疗系统设计与实现 (明康慧医智慧医疗系统) **Tiếng Anh:** Design and Implementation of *Minh Khoe Tue Y* - a Health Management and Assisted Diagnosis System Based on LLM and Multimodal Artificial Intelligence **hoặc** Minh Khoe Tue Y Smart Healthcare System, _MKTY_)

## Giới Thiệu Dự Án

&nbsp;&nbsp;&nbsp;&nbsp;Dự án này nhằm mục đích sử dụng các mô hình ngôn ngữ quy mô lớn (LLM) và công nghệ trí tuệ nhân tạo đa mô thức để nâng cao tính thông minh và cá nhân hóa của hệ thống quản lý sức khỏe và hỗ trợ chẩn đoán y tế. Thông qua cơ chế “thảo luận LLM” sáng tạo của chúng tôi, giúp giảm thiểu hiện tượng ảo tưởng của các mô hình lớn và phương pháp phân tích dữ liệu đa mô thức, hệ thống có thể xử lý thông tin hồ sơ bệnh án điện tử và dữ liệu sức khỏe của bệnh nhân một cách thông minh hơn, đưa ra các đề xuất chẩn đoán chính xác, giảm bớt gánh nặng cho bác sĩ và nâng cao hiệu quả chẩn đoán. Hệ thống còn hỗ trợ người bệnh tự chẩn đoán, giúp người dùng phòng ngừa bệnh tật sớm, giảm thiểu nhu cầu khám bệnh không cần thiết và tối ưu hóa phân bổ tài nguyên y tế. Kết hợp với công nghệ đa mô thức, hệ thống có thể tích hợp nhiều nguồn dữ liệu trong lĩnh vực y tế như văn bản y học, hình ảnh y tế,... từ đó nâng cao độ chính xác và tính khoa học của quyết định lâm sàng, thúc đẩy sự phát triển thông minh của dịch vụ y tế. Bên cạnh đó, hệ thống còn có chức năng cơ sở dữ liệu y học, cho phép người dùng tự do chia sẻ các kiến thức chất lượng cao trong lĩnh vực y tế, người dùng có thể tìm kiếm thông minh đa mô thức các kiến thức trong hệ thống và sử dụng các kiến thức này để nâng cao khả năng tạo nội dung của LLM. Tóm lại, dự án này khám phá sự kết hợp sâu sắc giữa AI và y học, mang đến một mô hình công nghệ và kinh nghiệm thực tế cho các ứng dụng trong lĩnh vực y tế và sức khỏe trong tương lai.  

## Tác Giả Dự Án

```
██\      ██\     ██\   ██\   ████████\  ██\     ██\
███\    ███ |    ██ | ██  |  \__██  __| \██\   ██  |
████\  ████ |    ██ |██  /      ██ |     \██\ ██  /
██\██\██ ██ |    █████  /       ██ |      \████  /
██ \███  ██ |    ██  ██<        ██ |       \██  /
██ |\█  /██ |    ██ |\██\       ██ |        ██ |
██ | \_/ ██ |██\ ██ | \██\ ██\  ██ |██\     ██ |██\
\__|     \__|\__|\__|  \__|\__| \__|\__|    \__|\__|
```

Dự án này là đồ án tốt nghiệp của tôi tại Đại học Công nghiệp Tề Lỗ (_Qilu_) (Viện Khoa học tỉnh Sơn Đông) năm 2025.

- **Tác Giả Dự Án**
  - **Đỗ Vũ** (Tiếng Trung: _杜宇_; Tiếng Anh: _DU Yu_; email: <202103180009@stu.qlu.edu.cn>), sinh viên tốt nghiệp năm 2025, Học bộ Khoa học và Kỹ thuật Máy tính, Đại học Công nghiệp Tề Lỗ (_Qilu_) (Viện Khoa học tỉnh Sơn Đông)

- **Giáo Viên Hướng Dẫn Đồ Án**
  - Giáo viên trường: **Khương Văn Phong** (Tiếng Trung: _姜文峰_; Tiếng Anh: _JIANG Wenfeng_), giảng viên Học bộ Khoa học và Kỹ thuật Máy tính, Đại học Công nghiệp Tề Lỗ (_Qilu_) (Viện Khoa học tỉnh Sơn Đông).
  - Giáo viên công ty: **Lý Quân** (Tiếng Trung: _李君_; Tiếng Anh: _LI Jun_), Học viện Đào tạo Phần mềm Strong (_Sư Sáng_) Sơn Đông, Tập đoàn Khoa kỹ Giáo dục Ambow (_An Bác_, [NYSE: AMBO](https://www.nyse.com/quote/XASE:AMBO)).

## Liên Kết Tình Bạn

- Đại học Công nghiệp Tề Lỗ (_Qilu_) (Viện Khoa học tỉnh Sơn Đông): [https://www.qlu.edu.cn/](https://www.qlu.edu.cn/)
  
- Trung tâm Tính toán Sơn Đông (Trung tâm Tính toán Siêu máy tính Quốc gia Tế Nam, _NSCCJN_): [https://www.nsccjn.cn/](https://www.nsccjn.cn/)

- Học bộ Khoa học và Kỹ thuật Máy tính, Đại học Công nghiệp Tề Lỗ (_Qilu_) (Viện Khoa học tỉnh Sơn Đông): [http://jsxb.scsc.cn/](http://jsxb.scsc.cn/)

- Trang GitHub của Đỗ Vũ: [https://github.com/duyu09/](https://github.com/duyu09/)

## Thống Kê Lượt Truy Cập

<div><b>Số lượt truy cập tổng cộng (Tất cả các dự án của Duyu09 trên GitHub): </b><br><img src="https://profile-counter.glitch.me/duyu09/count.svg" /></div> 

<div><b>Số lượt truy cập tổng cộng (MKTY): </b>
<br><img src="https://profile-counter.glitch.me/duyu09-MKTY-SYSTEM/count.svg" /></div> 

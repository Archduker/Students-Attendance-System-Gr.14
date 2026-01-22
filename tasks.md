# 📋 Task Breakdown - Student Attendance System

> **Team Size:** 5 người | **Leader:** Bạn | **Ngày tạo:** 21/01/2026

---

## 🏗️ Workflow GitHub

```
main (protected)
  └── develop (integration branch)
        ├── feature/auth-module
        ├── feature/student-module
        ├── feature/teacher-module
        ├── feature/admin-module
        └── feature/core-ui
```

**Quy tắc:**
- Tất cả feature branches được tạo từ `develop`
- Merge vào `develop` qua Pull Request + Code Review
- Chỉ merge `develop` → `main` khi release

---

## 👥 Phân Công Công Việc

| Thành viên | Module | Branch | Vai trò |
|------------|--------|--------|---------|
| **Leader** | Core Infrastructure & Review | `develop` | Quản lý, review code, integration |
| **Member 1** | Authentication & Security | `feature/auth-module` | Login, Reset Password, Security |
| **Member 2** | Student Module | `feature/student-module` | Student Dashboard, Attendance |
| **Member 3** | Teacher Module | `feature/teacher-module` | Teacher Dashboard, Sessions |
| **Member 4** | Admin Module | `feature/admin-module` | Admin Dashboard, User/Class Management |

---

## 📌 Chi Tiết Công Việc Theo Branch

---

### 🔐 MEMBER 1: `feature/auth-module`

**Mô tả:** Module xác thực người dùng

#### Công việc cần làm:

| # | Task | File/Folder | Ưu tiên |
|---|------|-------------|---------|
| 1.1 | Tạo Login Page UI | `views/pages/auth/login_page.py` | 🔴 High |
| 1.2 | Tạo Reset Password Page UI | `views/pages/auth/reset_password_page.py` | 🟡 Medium |
| 1.3 | Hoàn thiện AuthService | `services/auth_service.py` | 🔴 High |
| 1.4 | Kết nối Login với Database | `controllers/auth_controller.py` | 🔴 High |
| 1.5 | Tạo Session Management | `services/session_service.py` | 🟡 Medium |
| 1.6 | Gửi email reset password | `services/email_service.py` | 🟢 Low |
| 1.7 | Unit tests cho Auth | `tests/test_auth.py` | 🟡 Medium |

#### Checklist:
- [ ] Login page với username/password input
- [ ] Validation form (empty, format)
- [ ] Hiển thị error message khi login thất bại
- [ ] Remember me checkbox
- [ ] Forgot password link → Reset Password page
- [ ] Hash password với bcrypt
- [ ] Session token sau khi login thành công

---

### 🎓 MEMBER 2: `feature/student-module`

**Mô tả:** Module sinh viên - điểm danh và xem lịch sử

#### Công việc cần làm:

| # | Task | File/Folder | Ưu tiên |
|---|------|-------------|---------|
| 2.1 | Tạo Student Dashboard UI | `views/pages/student/dashboard.py` | 🔴 High |
| 2.2 | Tạo Attendance Submission Page | `views/pages/student/submit_attendance.py` | 🔴 High |
| 2.3 | Tạo Attendance History Page | `views/pages/student/attendance_history.py` | 🟡 Medium |
| 2.4 | Tạo Edit Profile Page | `views/pages/student/profile.py` | 🟢 Low |
| 2.5 | Tạo StudentService | `services/student_service.py` | 🔴 High |
| 2.6 | StudentController | `controllers/student_controller.py` | 🔴 High |
| 2.7 | Tích hợp QR Scanner | `views/components/qr_scanner.py` | 🟡 Medium |
| 2.8 | Unit tests cho Student | `tests/test_student.py` | 🟡 Medium |

#### Checklist:
- [ ] Dashboard hiển thị: tỷ lệ điểm danh, số buổi vắng, lịch học
- [ ] Submit attendance bằng QR Code scan
- [ ] Submit attendance bằng Token/Link
- [ ] Hiển thị countdown thời gian điểm danh còn lại
- [ ] Attendance history với filter theo ngày/lớp
- [ ] Edit profile: đổi mật khẩu, cập nhật thông tin

---

### 👨‍🏫 MEMBER 3: `feature/teacher-module`

**Mô tả:** Module giáo viên - quản lý phiên điểm danh

#### Công việc cần làm:

| # | Task | File/Folder | Ưu tiên |
|---|------|-------------|---------|
| 3.1 | Tạo Teacher Dashboard UI | `views/pages/teacher/dashboard.py` | 🔴 High |
| 3.2 | Tạo Session Management Page | `views/pages/teacher/session_management.py` | 🔴 High |
| 3.3 | Tạo Create Session Dialog | `views/pages/teacher/create_session.py` | 🔴 High |
| 3.4 | Tạo Class Attendance Report | `views/pages/teacher/class_report.py` | 🟡 Medium |
| 3.5 | Tạo Manual Attendance Page | `views/pages/teacher/manual_attendance.py` | 🟡 Medium |
| 3.6 | Hoàn thiện QRService | `services/qr_service.py` | 🔴 High |
| 3.7 | Tạo AttendanceSessionService | `services/attendance_session_service.py` | 🔴 High |
| 3.8 | TeacherController | `controllers/teacher_controller.py` | 🔴 High |
| 3.9 | Unit tests cho Teacher | `tests/test_teacher.py` | 🟡 Medium |

#### Checklist:
- [ ] Dashboard hiển thị: lớp phụ trách, tổng sinh viên, tỷ lệ điểm danh
- [ ] Tạo phiên điểm danh mới (QR/Token/Manual)
- [ ] Generate QR Code tự động refresh mỗi 30s
- [ ] Generate Link/Token điểm danh
- [ ] Manual attendance: chọn sinh viên → đánh dấu Present/Absent
- [ ] Xem danh sách sinh viên đã điểm danh realtime
- [ ] Auto-close session khi hết thời gian
- [ ] Export báo cáo lớp (CSV/Excel)

---

### 🛡️ MEMBER 4: `feature/admin-module`

**Mô tả:** Module admin - quản lý hệ thống

#### Công việc cần làm:

| # | Task | File/Folder | Ưu tiên |
|---|------|-------------|---------|
| 4.1 | Tạo Admin Dashboard UI | `views/pages/admin/dashboard.py` | 🔴 High |
| 4.2 | Tạo User Management Page | `views/pages/admin/user_management.py` | 🔴 High |
| 4.3 | Tạo Create/Edit User Dialog | `views/pages/admin/user_dialog.py` | 🔴 High |
| 4.4 | Tạo Class Management Page | `views/pages/admin/class_management.py` | 🔴 High |
| 4.5 | Tạo Create/Edit Class Dialog | `views/pages/admin/class_dialog.py` | 🟡 Medium |
| 4.6 | Tạo System Reports Page | `views/pages/admin/reports.py` | 🟡 Medium |
| 4.7 | Tạo AdminService | `services/admin_service.py` | 🔴 High |
| 4.8 | AdminController | `controllers/admin_controller.py` | 🔴 High |
| 4.9 | Export Reports (PDF/Excel/CSV) | `services/report_service.py` | 🟢 Low |
| 4.10 | Unit tests cho Admin | `tests/test_admin.py` | 🟡 Medium |

#### Checklist:
- [ ] Dashboard hiển thị: tổng users, tổng classes, hoạt động gần đây
- [ ] CRUD User: tạo, sửa, xóa, tìm kiếm user
- [ ] Phân quyền role: Admin/Teacher/Student
- [ ] CRUD Class: tạo, sửa, xóa lớp học
- [ ] Gán teacher cho class
- [ ] Thêm/xóa student khỏi class
- [ ] Báo cáo điểm danh toàn hệ thống
- [ ] Export báo cáo PDF/Excel/CSV

---

### 🎨 LEADER: Core Infrastructure & Integration

**Mô tả:** Thiết lập nền tảng, UI components, review & merge code

#### Công việc cần làm:

| # | Task | File/Folder | Ưu tiên |
|---|------|-------------|---------|
| L.1 | Thiết lập App Router/Navigation | `views/app.py` | 🔴 High |
| L.2 | Tạo Base Layout | `views/layouts/main_layout.py` | 🔴 High |
| L.3 | Tạo Sidebar Component | `views/components/sidebar.py` | 🔴 High |
| L.4 | Tạo Navbar Component | `views/components/navbar.py` | 🔴 High |
| L.5 | Tạo Common UI Components | `views/components/` | 🟡 Medium |
| L.6 | Thiết lập Theme/Styles | `views/styles/theme.py` | 🟡 Medium |
| L.7 | Database migrations | `data/migrations/` | 🔴 High |
| L.8 | Code Review tất cả PRs | GitHub PRs | 🔴 High |
| L.9 | Integration testing | `tests/test_integration.py` | 🟡 Medium |
| L.10 | Documentation | `docs/` | 🟢 Low |

#### UI Components cần tạo (`views/components/`):
- [ ] `button.py` - Custom button styles
- [ ] `input.py` - Text input, password input
- [ ] `table.py` - Data table với pagination
- [ ] `card.py` - Card component
- [ ] `modal.py` - Modal/Dialog
- [ ] `toast.py` - Toast notifications
- [ ] `loading.py` - Loading spinner

---

## 📅 Timeline Đề Xuất

| Tuần | Công việc | Branch hoạt động |
|------|-----------|------------------|
| **Tuần 1** | Setup infrastructure, Login UI | `develop`, `feature/auth-module` |
| **Tuần 2** | Hoàn thiện Auth, bắt đầu Dashboards | Tất cả branches |
| **Tuần 3** | Hoàn thiện chức năng chính mỗi module | Tất cả branches |
| **Tuần 4** | Integration, Testing, Bug fixes | `develop` |
| **Tuần 5** | Polish UI, Documentation | `main` release |

---

## 📝 Quy Trình Làm Việc

### Tạo branch mới:
```bash
git checkout develop
git pull origin develop
git checkout -b feature/your-module
```

### Commit message format:
```
<type>(<scope>): <description>

# Examples:
feat(auth): add login page UI
fix(student): fix attendance submission bug
docs(readme): update installation guide
```

### Tạo Pull Request:
1. Push branch lên GitHub
2. Tạo PR vào `develop`
3. Assign Leader review
4. Fix feedback nếu có
5. Merge sau khi approved

---

## ✅ Definition of Done

Một task được coi là **DONE** khi:
- [ ] Code hoạt động đúng yêu cầu
- [ ] Có unit tests (coverage > 70%)
- [ ] Không có lỗi lint/type
- [ ] Đã được code review
- [ ] Đã merge vào develop
- [ ] Documentation cập nhật (nếu cần)

---

## 🐳 Docker Deployment & Dev Tools

> **Mục tiêu:** Cấu hình dự án để deploy và phát triển với các tools chuẩn công nghiệp

### Phân công

| Task | Người thực hiện | Trạng thái |
|------|-----------------|------------|
| Docker Configuration | Leader | 🟡 In Progress |
| Bug Tracking Setup | Leader | ⬜ Pending |
| VS Code Config | Leader | ⬜ Pending |
| Test Cases Excel | Tất cả members | ⬜ Pending |

---

### ✅ Checklist Docker Files

- [ ] **Dockerfile** - Build image cho ứng dụng Python
  - Location: `/Dockerfile`
  - Base image: `python:3.11-slim`
  - Install system dependencies cho GUI libs (libzbar, OpenCV)

- [ ] **docker-compose.yml** - Orchestrate services
  - Location: `/docker-compose.yml`
  - Services: `app`, `mantis`, `mantis-db`
  - Ports: Mantis trên `8989`

- [ ] **.dockerignore** - Loại bỏ files không cần thiết
  - Location: `/.dockerignore`
  - Ignore: venv, __pycache__, .git, tests, docs

---

### ✅ Checklist VS Code Configuration

- [ ] **.vscode/settings.json** - Python settings
  - Auto format on save
  - Pytest enabled

- [ ] **.vscode/launch.json** - Debug configurations
  - Run App
  - Init Database
  - Run Tests

- [ ] **.vscode/extensions.json** - Recommended extensions
  - Python, Debugpy, Black Formatter, Docker

---

### ✅ Checklist Bug Tracking (Mantis)

- [ ] Chạy Mantis qua Docker Compose
- [ ] Truy cập http://localhost:8989
- [ ] Tạo project "Student Attendance System"
- [ ] Thêm categories: Login, Student, Teacher, Admin, General
- [ ] Thêm tất cả members vào project
- [ ] Tạo hướng dẫn sử dụng tại `docs/BUG_TRACKING.md`

---

### ✅ Checklist Test Cases (Excel)

- [ ] Tạo folder `docs/test_cases/`
- [ ] Tạo file `TEST_CASES_TEMPLATE.xlsx` với các sheets:
  - Sheet 1: **Login Module** - Test đăng nhập, reset password
  - Sheet 2: **Student Module** - Test điểm danh, xem lịch sử
  - Sheet 3: **Teacher Module** - Test tạo session, QR code
  - Sheet 4: **Admin Module** - Test CRUD users/classes

---

### ✅ Checklist GitHub

- [ ] Tạo `.github/PULL_REQUEST_TEMPLATE.md`
- [ ] Cập nhật README với Docker instructions
- [ ] Thêm GitHub Actions cho CI/CD (optional)

---

### 📝 Hướng dẫn chi tiết

Xem file **[docker_config.md](docker_config.md)** để có hướng dẫn từng bước về:
- Cách build Docker image
- Cách chạy Mantis Bug Tracker
- Troubleshooting các lỗi phổ biến

---

## 🔗 Resources

- [CustomTkinter Docs](https://customtkinter.tomschimansky.com/)
- [SQLite3 Python Docs](https://docs.python.org/3/library/sqlite3.html)
- [bcrypt Docs](https://pypi.org/project/bcrypt/)
- [qrcode Docs](https://pypi.org/project/qrcode/)

---

> **Ghi chú:** File này sẽ được cập nhật thường xuyên. Mọi thay đổi cần thông qua Leader.

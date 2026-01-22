# 🐳 Docker Configuration Guide

Hướng dẫn cấu hình và deploy dự án **Student Attendance System** với Docker.

---

## 📋 Mục Lục

1. [Tổng quan](#-tổng-quan)
2. [Yêu cầu hệ thống](#-yêu-cầu-hệ-thống)
3. [Cấu trúc Docker files](#-cấu-trúc-docker-files)
4. [Hướng dẫn sử dụng](#-hướng-dẫn-sử-dụng)
5. [Mantis Bug Tracker](#-mantis-bug-tracker)
6. [Checklist Deployment](#-checklist-deployment)
7. [Troubleshooting](#-troubleshooting)

---

## 🎯 Tổng Quan

### Mục đích sử dụng Docker

| Mục đích | Mô tả |
|----------|-------|
| **Development** | Đồng bộ môi trường phát triển giữa các thành viên |
| **Database** | Khởi tạo và seed database một cách nhất quán |
| **Bug Tracking** | Chạy Mantis Bug Tracker để theo dõi lỗi |
| **CI/CD** | Chạy tests tự động trong pipeline |

> ⚠️ **Lưu ý:** Ứng dụng sử dụng GUI (CustomTkinter) nên cần chạy trực tiếp trên máy local với display. Docker phục vụ cho các tác vụ không cần GUI.

---

## 💻 Yêu Cầu Hệ Thống

### Phần mềm cần cài đặt

| Software | Version | Download |
|----------|---------|----------|
| **Docker** | ≥ 20.10 | [docker.com](https://www.docker.com/get-started) |
| **Docker Compose** | ≥ 2.0 | Đi kèm với Docker Desktop |
| **Git** | ≥ 2.30 | [git-scm.com](https://git-scm.com/) |

### Kiểm tra cài đặt

```bash
# Kiểm tra Docker
docker --version
# Kết quả mong đợi: Docker version 20.10.x hoặc mới hơn

# Kiểm tra Docker Compose
docker-compose --version
# Kết quả mong đợi: Docker Compose version v2.x.x
```

---

## 📁 Cấu Trúc Docker Files

Sau khi setup, project sẽ có các files Docker sau:

```
Students-Attendance-System-Gr.14/
├── Dockerfile              # Build image cho ứng dụng
├── docker-compose.yml      # Orchestrate các services
├── .dockerignore           # Files bỏ qua khi build
└── docker_config.md        # File này - hướng dẫn sử dụng
```

---

## 🚀 Hướng Dẫn Sử Dụng

### Bước 1: Clone Repository (nếu chưa có)

```bash
git clone <repository-url>
cd Students-Attendance-System-Gr.14
```

### Bước 2: Build Docker Image

```bash
# Build image với tên "student-attendance"
docker build -t student-attendance .

# Kết quả mong đợi: "Successfully built..." và "Successfully tagged..."
```

### Bước 3: Khởi tạo Database

```bash
# Chạy container để init database với demo data
docker run --rm -v $(pwd)/database:/app/database student-attendance

# Kiểm tra file database được tạo
ls -la database/
# Kết quả mong đợi: có file attendance.db
```

### Bước 4: Chạy ứng dụng trên máy local

```bash
# Kích hoạt virtual environment
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate     # Windows

# Cài đặt dependencies
pip install -r requirements.txt

# Chạy ứng dụng GUI
python main.py
```

---

## 🐛 Mantis Bug Tracker

### Tại sao chọn Mantis?

| Tiêu chí | Đánh giá |
|----------|----------|
| **Chi phí** | ✅ Miễn phí 100% (Open-source) |
| **Cài đặt** | ✅ 1 lệnh Docker là xong |
| **Giao diện** | ✅ Đơn giản, dễ dùng |
| **Ngôn ngữ** | ✅ Hỗ trợ tiếng Việt |
| **Team size** | ✅ Phù hợp team nhỏ (5 người) |

### Khởi động Mantis

```bash
# Chạy Mantis + MySQL database
docker-compose up -d mantis mantis-db

# Chờ khoảng 30-60 giây để services khởi động
# Kiểm tra logs
docker-compose logs -f mantis
```

### Truy cập Mantis

| Thông tin | Giá trị |
|-----------|---------|
| **URL** | http://localhost:8989 |
| **Username** | `administrator` |
| **Password** | (Đặt lần đầu đăng nhập) |

### Setup ban đầu

1. Mở browser: `http://localhost:8989`
2. Đăng nhập với username `administrator`
3. Đổi password theo yêu cầu
4. Tạo project mới: **Manage > Manage Projects > Create New Project**
   - Project Name: `Student Attendance System`
   - Status: `development`
5. Thêm thành viên vào project

### Cách báo cáo Bug

1. Vào **Report Issue**
2. Chọn Project: `Student Attendance System`
3. Điền các thông tin:
   - **Category**: `[Login]`, `[Student]`, `[Teacher]`, `[Admin]`, `[General]`
   - **Severity**: Mức độ nghiêm trọng
   - **Summary**: Tóm tắt ngắn gọn bug
   - **Description**: Mô tả chi tiết
   - **Steps to Reproduce**: Các bước để tái hiện lỗi

### Dừng Mantis

```bash
# Dừng services nhưng giữ data
docker-compose stop mantis mantis-db

# Dừng và xóa containers (data vẫn được giữ trong volume)
docker-compose down
```

---

## ✅ Checklist Deployment

### Phase 1: Chuẩn bị môi trường

- [ ] Cài đặt Docker Desktop
- [ ] Cài đặt Docker Compose
- [ ] Clone repository về máy
- [ ] Kiểm tra `docker --version` chạy được

### Phase 2: Build và Test

- [ ] Tạo file `Dockerfile` trong project root
- [ ] Tạo file `docker-compose.yml` trong project root
- [ ] Tạo file `.dockerignore` trong project root
- [ ] Build image: `docker build -t student-attendance .`
- [ ] Kiểm tra build thành công (không có errors)

### Phase 3: Database

- [ ] Chạy init database qua Docker
- [ ] Kiểm tra file `database/attendance.db` được tạo
- [ ] Test kết nối database từ app

### Phase 4: Bug Tracking (Mantis)

- [ ] Chạy `docker-compose up -d mantis mantis-db`
- [ ] Truy cập http://localhost:8989 thành công
- [ ] Đổi password admin lần đầu
- [ ] Tạo project "Student Attendance System"
- [ ] Thêm các thành viên team vào project
- [ ] Test tạo issue mới

### Phase 5: Local Development

- [ ] Tạo virtual environment: `python -m venv venv`
- [ ] Cài dependencies: `pip install -r requirements.txt`
- [ ] Chạy app: `python main.py` - không có lỗi
- [ ] Chạy tests: `pytest` - tất cả pass

---

## 🔧 Troubleshooting

### Lỗi: "Cannot connect to Docker daemon"

```bash
# Linux: Đảm bảo Docker service đang chạy
sudo systemctl start docker

# Mac/Windows: Đảm bảo Docker Desktop đang chạy
```

### Lỗi: "Port 8989 already in use"

```bash
# Tìm process đang dùng port
lsof -i :8989

# Đổi port trong docker-compose.yml
# ports: "8990:80" thay vì "8989:80"
```

### Lỗi: "Permission denied" khi mount volume

```bash
# Linux: Thêm user vào docker group
sudo usermod -aG docker $USER
# Logout và login lại
```

### Xóa tất cả và làm lại từ đầu

```bash
# Dừng tất cả containers
docker-compose down -v

# Xóa image
docker rmi student-attendance

# Build lại
docker build -t student-attendance .
```

---

## 📚 Tài Liệu Tham Khảo

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Mantis Bug Tracker Wiki](https://mantisbt.org/wiki/)
- [CustomTkinter Documentation](https://customtkinter.tomschimansky.com/)

---

> **Cập nhật lần cuối:** 22/01/2026  
> **Người tạo:** Group 14 - SE - k24 - UTH

# Student Module - Feature Documentation

## 📋 Tổng quan

Module sinh viên (Student Module) cung cấp đầy đủ các chức năng cho sinh viên trong hệ thống điểm danh, bao gồm:

- ✅ Dashboard với thống kê điểm danh
- 📝 Điểm danh qua QR code hoặc token
- 📜 Xem lịch sử điểm danh
- 👤 Quản lý thông tin cá nhân

---

## 🗂️ Cấu trúc files đã tạo

### 1. **Services Layer** (Business Logic)

#### `services/student_service.py` 🔴 HIGH PRIORITY
**Chức năng:**
- `get_dashboard_stats()` - Lấy thống kê cho dashboard
- `get_class_schedule()` - Lấy lịch học
- `submit_attendance()` - Submit điểm danh
- `get_attendance_history()` - Lấy lịch sử điểm danh với filters
- `update_profile()` - Cập nhật thông tin cá nhân
- `get_student_info()` - Lấy thông tin sinh viên

**Dependencies:**
- UserRepository
- AttendanceRecordRepository
- AttendanceSessionRepository
- ClassRepository

---

### 2. **Controllers Layer** (Request Handlers)

#### `controllers/student_controller.py` 🔴 HIGH PRIORITY
**Chức năng:**
- `handle_get_dashboard()` - Xử lý request dashboard
- `handle_submit_attendance()` - Xử lý điểm danh
- `handle_get_attendance_history()` - Xử lý lấy lịch sử
- `handle_update_profile()` - Xử lý cập nhật profile
- `handle_get_student_info()` - Xử lý lấy thông tin
- `validate_student_code()` - Validate mã sinh viên

**Validation:**
- Input validation cho all requests
- Date format validation
- Email validation
- Error handling với user-friendly messages

---

### 3. **Views Layer** (UI Components)

#### `views/pages/student/dashboard.py` 🔴 HIGH PRIORITY

**Components:**
- Header với refresh button
- Statistics cards (4 cards):
  - 📈 Tỷ lệ điểm danh
  - 📚 Tổng số buổi
  - ✅ Có mặt
  - ❌ Vắng mặt
- 📅 Class schedule section
- 🕒 Recent attendance records (5 gần nhất)

**Features:**
- Auto-refresh
- Loading states
- Error handling
- Responsive layout với scrolling

---

#### `views/pages/student/submit_attendance.py` 🔴 HIGH PRIORITY

**Components:**
- Method selection (QR hoặc Manual)
- QR Scanner integration
- Manual input form:
  - Session ID entry
  - Token entry (optional)
- Submit button
- Success/Error feedback

**Phương thức điểm danh hỗ trợ:**
- 📷 QR Code scanning
- ⌨️ Manual token input
- 🔗 Link-based attendance

---

#### `views/pages/student/attendance_history.py` 🟡 MEDIUM PRIORITY

**Components:**
- Filter panel:
  - Start date picker
  - End date picker
  - Class ID filter
  - Apply/Clear buttons
- Records table với columns:
  - Ngày
  - Giờ
  - Lớp
  - Mã lớp
  - Trạng thái
- Summary counter
- Table header

**Features:**
- Date range filtering
- Class filtering
- Sorted by date (newest first)
- Color-coded status badges
- Scrollable list

---

#### `views/pages/student/profile.py` 🟢 LOW PRIORITY

**Components:**
- Profile info section:
  - Student code (readonly)
  - Full name input
  - Email input
  - Class name input
  - Save/Cancel buttons
- Change password section:
  - Old password input
  - New password input
  - Confirm password input
  - Change password button

**Features:**
- Form validation
- Password confirmation
- Success/Error feedback
- Auto-fill current info

---

### 4. **Components** (Reusable UI)

#### `views/components/qr_scanner.py` 🟡 MEDIUM PRIORITY

**Class: `QRScanner`**
- Camera integration với OpenCV
- Real-time QR scanning với pyzbar
- Threading để không block UI
- Start/Stop controls
- Success callback

**Function: `show_qr_scanner_dialog()`**
- Hiển thị scanner trong dialog window
- Modal dialog
- Auto-close khi scan thành công

**Features:**
- Camera preview
- Real-time detection
- 10-second timeout cho blocking scan
- Error handling
- Status messages

---

### 5. **Tests** (Unit Tests)

#### `tests/test_student.py` 🟡 MEDIUM PRIORITY

**Test Coverage:**

**StudentService Tests:**
- ✅ get_dashboard_stats (có/không có records)
- ✅ submit_attendance (success, errors)
- ✅ Session validation (not found, closed, expired)
- ✅ Duplicate submission check
- ✅ Token validation
- ✅ get_attendance_history
- ✅ update_profile (success, invalid email)

**StudentController Tests:**
- ✅ handle_get_dashboard
- ✅ handle_submit_attendance
- ✅ Validation errors
- ✅ Filter handling
- ✅ Profile updates
- ✅ Student code validation

**Integration Tests:**
- ✅ Full attendance flow

**Test Fixtures:**
- Mock repositories
- Sample student data
- Sample attendance records
- Sample sessions

---

## 📊 Luồng xử lý (Workflows)

### 1. Dashboard Loading Flow

```
User opens dashboard
    ↓
StudentDashboard._load_data()
    ↓
StudentController.handle_get_dashboard()
    ↓
StudentService.get_dashboard_stats()
    ↓
Query repositories:
  - attendance_record_repo.find_by_student()
  - class_repo.find_by_student()
  - user_repo.find_by_student_code()
    ↓
Calculate statistics
    ↓
Return formatted data
    ↓
Render UI components
```

### 2. Submit Attendance Flow

```
User chooses method (QR or Manual)
    ↓
[QR Path]                    [Manual Path]
QRScanner.start_scanning()   User enters Session ID + Token
    ↓                              ↓
Scan QR code ──────────────────────┘
    ↓
SubmitAttendancePage._submit_attendance()
    ↓
StudentController.handle_submit_attendance()
    ↓
StudentService.submit_attendance()
    ↓
Validations:
  - Session exists?
  - Session open?
  - In time window?
  - Not already submitted?
  - Token valid?
    ↓
Create AttendanceRecord
    ↓
attendance_record_repo.create()
    ↓
Return success/error
    ↓
Show feedback to user
```

### 3. View History Flow

```
User opens history page
    ↓
User sets filters (optional)
    ↓
AttendanceHistoryPage._apply_filters()
    ↓
StudentController.handle_get_attendance_history()
    ↓
Parse filter dates
    ↓
StudentService.get_attendance_history()
    ↓
Query attendance_record_repo
    ↓
Filter by:
  - Date range
  - Class ID
    ↓
Format records
    ↓
Sort by date (descending)
    ↓
Render table
```

---

## 🔧 Cấu hình & Dependencies

### Required Packages

```python
# GUI
customtkinter>=5.2.0
Pillow>=10.0.0

# QR Code
qrcode[pil]>=7.4.0
opencv-python>=4.8.0
pyzbar>=0.1.9

# Testing
pytest>=7.4.0
```

### Database Tables Used

- `Student` - Thông tin sinh viên
- `User` - Thông tin người dùng
- `attendance_records` - Bản ghi điểm danh
- `attendance_sessions` - Phiên điểm danh
- `Classes` - Lớp học
- `Classes-Student` - Liên kết sinh viên-lớp

---

## 🚀 Usage Examples

### Example 1: Initialize Student Dashboard

```python
from views.pages.student import StudentDashboard
from controllers import StudentController
from services import StudentService

# Setup dependencies
student_service = StudentService(
    user_repo=user_repo,
    attendance_record_repo=attendance_record_repo,
    attendance_session_repo=attendance_session_repo,
    class_repo=class_repo
)

student_controller = StudentController(student_service)

# Create dashboard
dashboard = StudentDashboard(
    parent=parent_frame,
    controller=student_controller,
    student_code="SV001"
)
dashboard.pack(fill="both", expand=True)
```

### Example 2: Setup QR Scanner

```python
from views.components import QRScanner

def on_scan_success(qr_data):
    print(f"Scanned: {qr_data}")
    # Parse and submit attendance

scanner = QRScanner(
    parent=parent_frame,
    on_scan_success=on_scan_success,
    camera_index=0
)
scanner.pack()
```

### Example 3: Submit Attendance

```python
result = student_controller.handle_submit_attendance(
    student_code="SV001",
    session_id="SESSION123",
    verification_data="TOKEN456"
)

if result["success"]:
    print("✅ Điểm danh thành công!")
else:
    print(f"❌ Lỗi: {result['message']}")
```

### Example 4: Get History with Filters

```python
filters = {
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "class_id": "CS101"
}

result = student_controller.handle_get_attendance_history(
    student_code="SV001",
    filters=filters
)

if result["success"]:
    for record in result["data"]["records"]:
        print(f"{record['date']}: {record['status']}")
```

---

## ✅ Checklist hoàn thành

### High Priority ✓
- [x] StudentService (`services/student_service.py`)
- [x] StudentController (`controllers/student_controller.py`)
- [x] Student Dashboard UI (`views/pages/student/dashboard.py`)
- [x] Submit Attendance Page (`views/pages/student/submit_attendance.py`)

### Medium Priority ✓
- [x] Attendance History Page (`views/pages/student/attendance_history.py`)
- [x] QR Scanner Component (`views/components/qr_scanner.py`)
- [x] Unit Tests (`tests/test_student.py`)

### Low Priority ✓
- [x] Edit Profile Page (`views/pages/student/profile.py`)

### Additional Tasks ✓
- [x] Updated `services/__init__.py`
- [x] Updated `controllers/__init__.py`
- [x] Updated `views/pages/student/__init__.py`
- [x] Updated `views/components/__init__.py`

---

## 🎨 UI Design Highlights

### Color Scheme (from theme.py)
- **Primary**: #3B82F6 (Blue)
- **Success**: #10B981 (Green)
- **Error**: #EF4444 (Red)
- **Warning**: #F59E0B (Yellow)

### Icons Used
- 📊 Dashboard
- 📝 Submit attendance
- 📜 History
- 👤 Profile
- 📷 QR Scanner
- ✅ Present
- ❌ Absent
- 📈 Statistics
- 📅 Schedule
- 🔄 Refresh

---

## 🧪 Testing

### Run Tests

```bash
# Run all student tests
pytest tests/test_student.py -v

# Run specific test class
pytest tests/test_student.py::TestStudentService -v

# Run with coverage
pytest tests/test_student.py --cov=services.student_service --cov=controllers.student_controller
```

### Test Statistics
- **Total test cases**: 20+
- **Service tests**: 10+
- **Controller tests**: 8+
- **Integration tests**: 2+

---

## 📝 Notes & Limitations

1. **QR Scanner**: Requires camera access, may need permissions
2. **Threading**: QR scan runs in separate thread to avoid UI blocking
3. **Date Format**: Expects YYYY-MM-DD format for filters
4. **Student Code**: Validated to be 6-10 characters
5. **Email Validation**: Basic validation (@, .)
6. **Session Timing**: Checked against current system time

---

## 🔮 Future Enhancements

- [ ] Export history to PDF/Excel
- [ ] Push notifications for attendance reminders
- [ ] Offline mode support
- [ ] Biometric authentication
- [ ] Multi-language support
- [ ] Dark mode toggle
- [ ] Advanced analytics dashboard
- [ ] Attendance prediction

---

## 👨‍💻 Development Notes

### Code Style
- Docstrings for all classes and public methods
- Type hints for function parameters
- Error handling with try-except
- Logging for debugging
- Separation of concerns (MVC pattern)

### Best Practices
✅ DRY principle (Don't Repeat Yourself)
✅ SOLID principles
✅ Input validation
✅ Error messages in Vietnamese
✅ User-friendly UI feedback
✅ Responsive design
✅ Accessibility considerations

---

**Created**: 2026-01-22
**Version**: 1.0.0
**Status**: ✅ Complete

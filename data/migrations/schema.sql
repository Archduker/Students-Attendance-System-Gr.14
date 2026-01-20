-- ============================================================================
-- Student Attendance System - Database Schema
-- ============================================================================
-- File: schema.sql
-- Description: SQLite database schema cho hệ thống điểm danh sinh viên
-- 
-- Cách sử dụng:
--   python -c "from data.migrations.init_db import init_database; init_database()"
-- ============================================================================

-- Drop tables nếu tồn tại (cho development)
DROP TABLE IF EXISTS attendance_records;
DROP TABLE IF EXISTS attendance_sessions;
DROP TABLE IF EXISTS classes_student;
DROP TABLE IF EXISTS classes;
DROP TABLE IF EXISTS dashboard;
DROP TABLE IF EXISTS users;

-- ============================================================================
-- USERS TABLE
-- ============================================================================
-- Lưu trữ thông tin tất cả người dùng (Admin, Teacher, Student)
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(256) NOT NULL UNIQUE,
    password_hash VARCHAR(256) NOT NULL,
    full_name VARCHAR(256) NOT NULL,
    email VARCHAR(256),
    role TEXT CHECK(role IN ('ADMIN', 'TEACHER', 'STUDENT')) NOT NULL,
    
    -- Role-specific fields (nullable)
    admin_id CHAR(10),           -- Cho Admin
    teacher_code CHAR(10),       -- Cho Teacher
    student_code VARCHAR(10),    -- Cho Student
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes
    UNIQUE(admin_id),
    UNIQUE(teacher_code),
    UNIQUE(student_code)
);

-- Index cho tìm kiếm
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

-- ============================================================================
-- CLASSES TABLE
-- ============================================================================
-- Lưu trữ thông tin lớp học
CREATE TABLE classes (
    class_id CHAR(12) PRIMARY KEY,
    class_name VARCHAR(256) NOT NULL,
    subject_code CHAR(12) NOT NULL,
    teacher_code CHAR(10),
    
    FOREIGN KEY (teacher_code) REFERENCES users(teacher_code)
);

CREATE INDEX idx_classes_teacher ON classes(teacher_code);
CREATE INDEX idx_classes_subject ON classes(subject_code);

-- ============================================================================
-- CLASSES_STUDENT TABLE (Junction Table)
-- ============================================================================
-- Bảng liên kết sinh viên và lớp học (Many-to-Many)
CREATE TABLE classes_student (
    class_id VARCHAR(12) NOT NULL,
    student_code CHAR(10) NOT NULL,
    
    PRIMARY KEY (class_id, student_code),
    FOREIGN KEY (class_id) REFERENCES classes(class_id),
    FOREIGN KEY (student_code) REFERENCES users(student_code)
);

-- ============================================================================
-- ATTENDANCE_SESSIONS TABLE
-- ============================================================================
-- Lưu trữ các phiên điểm danh
CREATE TABLE attendance_sessions (
    session_id VARCHAR(10) PRIMARY KEY,
    class_id CHAR(12) NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    attendance_link VARCHAR(256),
    attendance_method TEXT CHECK(attendance_method IN ('QR', 'LINK_TOKEN', 'MANUAL', 'AUTO')) NOT NULL,
    qr_window_minutes INT DEFAULT 1,
    late_window_minutes INT DEFAULT 15,
    token VARCHAR(100),
    status TEXT CHECK(status IN ('OPEN', 'CLOSED')) DEFAULT 'OPEN',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (class_id) REFERENCES classes(class_id)
);

CREATE INDEX idx_sessions_class ON attendance_sessions(class_id);
CREATE INDEX idx_sessions_status ON attendance_sessions(status);
CREATE INDEX idx_sessions_token ON attendance_sessions(token);

-- ============================================================================
-- ATTENDANCE_RECORDS TABLE
-- ============================================================================
-- Lưu trữ bản ghi điểm danh của từng sinh viên
CREATE TABLE attendance_records (
    record_id VARCHAR(10) PRIMARY KEY,
    session_id VARCHAR(10) NOT NULL,
    student_code CHAR(10) NOT NULL,
    attendance_time DATETIME,
    status TEXT CHECK(status IN ('PRESENT', 'ABSENT')) DEFAULT 'ABSENT',
    remark VARCHAR(256),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (session_id) REFERENCES attendance_sessions(session_id),
    FOREIGN KEY (student_code) REFERENCES users(student_code),
    
    UNIQUE(session_id, student_code)
);

CREATE INDEX idx_records_session ON attendance_records(session_id);
CREATE INDEX idx_records_student ON attendance_records(student_code);
CREATE INDEX idx_records_status ON attendance_records(status);

-- ============================================================================
-- DASHBOARD TABLE
-- ============================================================================
-- Lưu trữ thống kê dashboard
CREATE TABLE dashboard (
    dashboard_id CHAR(1) PRIMARY KEY,
    user_id INTEGER NOT NULL,
    num_present INT DEFAULT 0,
    num_late INT DEFAULT 0,
    num_absent INT DEFAULT 0,
    generated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

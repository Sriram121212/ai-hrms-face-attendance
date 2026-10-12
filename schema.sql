-- ============================================
-- Face Attendance System - Database Schema
-- ============================================

CREATE DATABASE IF NOT EXISTS attendance_system;
USE attendance_system;

-- ============================================
-- 1. EMPLOYEES (also acts as users table for auth)
-- ============================================
CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'employee') NOT NULL DEFAULT 'employee',
    department VARCHAR(100),
    designation VARCHAR(100),
    join_date DATE NOT NULL,
    base_salary DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    phone VARCHAR(15),
    face_encoding_path VARCHAR(255),   -- path to stored face embedding file/blob
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ============================================
-- 2. ATTENDANCE
-- ============================================
CREATE TABLE attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    date DATE NOT NULL,
    check_in_time DATETIME,
    check_out_time DATETIME,
    status ENUM('present', 'absent', 'half_day', 'leave') NOT NULL DEFAULT 'absent',
    check_in_method ENUM('face', 'manual') DEFAULT 'face',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE,
    UNIQUE KEY unique_employee_date (employee_id, date)   -- one attendance row per employee per day
);

-- ============================================
-- 3. LEAVES
-- ============================================
CREATE TABLE leaves (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    from_date DATE NOT NULL,
    to_date DATE NOT NULL,
    reason TEXT,
    status ENUM('pending', 'approved', 'rejected') NOT NULL DEFAULT 'pending',
    applied_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reviewed_by INT,                 -- admin employee_id who approved/rejected
    reviewed_on TIMESTAMP NULL,
    FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE,
    FOREIGN KEY (reviewed_by) REFERENCES employees(id) ON DELETE SET NULL
);

-- ============================================
-- 4. SALARY SLIPS
-- ============================================
CREATE TABLE salary_slips (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    month INT NOT NULL,              -- 1-12
    year INT NOT NULL,
    base_salary DECIMAL(10, 2) NOT NULL,
    days_present INT DEFAULT 0,
    days_absent INT DEFAULT 0,
    deduction DECIMAL(10, 2) DEFAULT 0.00,
    net_salary DECIMAL(10, 2) NOT NULL,
    generated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE,
    UNIQUE KEY unique_employee_month (employee_id, month, year)  -- one slip per employee per month
);

-- ============================================
-- 5. HR POLICY DOCS (metadata only - actual vectors live in ChromaDB)
-- ============================================
CREATE TABLE hr_policy_docs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    chunk_count INT DEFAULT 0,
    uploaded_by INT,                  -- admin employee_id
    uploaded_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('processing', 'ready', 'failed') DEFAULT 'processing',
    FOREIGN KEY (uploaded_by) REFERENCES employees(id) ON DELETE SET NULL
);

-- ============================================
-- 6. CHATBOT LOGS (optional but great for resume - shows cost tracking + agent usage)
-- ============================================
CREATE TABLE chat_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    chat_type ENUM('hr_policy_rag', 'admin_agent') NOT NULL,
    query TEXT NOT NULL,
    response TEXT,
    tokens_used INT DEFAULT 0,
    cost_usd DECIMAL(10, 6) DEFAULT 0.000000,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
);

-- ============================================
-- Indexes for common query patterns
-- ============================================
CREATE INDEX idx_attendance_date ON attendance(date);
CREATE INDEX idx_leaves_status ON leaves(status);
CREATE INDEX idx_chat_logs_employee ON chat_logs(employee_id, created_at);

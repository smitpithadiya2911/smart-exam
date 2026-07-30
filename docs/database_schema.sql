-- Companion MySQL 8.x Raw Database Schema for Smart Online Examination & Learning Analytics System
-- Laragon Database: online_exam_db

CREATE DATABASE IF NOT EXISTS `online_exam_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `online_exam_db`;

-- 1. Users Table
CREATE TABLE IF NOT EXISTS `accounts_user` (
    `id` CHAR(36) NOT NULL PRIMARY KEY,
    `password` VARCHAR(128) NOT NULL,
    `last_login` DATETIME(6) NULL,
    `is_superuser` TINYINT(1) NOT NULL DEFAULT 0,
    `email` VARCHAR(254) NOT NULL UNIQUE,
    `first_name` VARCHAR(100) NOT NULL,
    `last_name` VARCHAR(100) NOT NULL,
    `role` VARCHAR(20) NOT NULL DEFAULT 'STUDENT',
    `phone_number` VARCHAR(15) NULL,
    `avatar` VARCHAR(100) NULL,
    `dark_mode` TINYINT(1) NOT NULL DEFAULT 0,
    `is_active` TINYINT(1) NOT NULL DEFAULT 1,
    `is_staff` TINYINT(1) NOT NULL DEFAULT 0,
    `date_joined` DATETIME(6) NOT NULL,
    `last_login_ip` VARCHAR(45) NULL,
    INDEX `idx_user_email` (`email`),
    INDEX `idx_user_role` (`role`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Departments Table
CREATE TABLE IF NOT EXISTS `departments_department` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(150) NOT NULL UNIQUE,
    `code` VARCHAR(20) NOT NULL UNIQUE,
    `description` LONGTEXT NULL,
    `created_at` DATETIME(6) NOT NULL,
    `updated_at` DATETIME(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Courses Table
CREATE TABLE IF NOT EXISTS `courses_course` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(150) NOT NULL,
    `code` VARCHAR(20) NOT NULL UNIQUE,
    `duration_years` INT UNSIGNED NOT NULL DEFAULT 3,
    `description` LONGTEXT NULL,
    `created_at` DATETIME(6) NOT NULL,
    `department_id` BIGINT NOT NULL,
    FOREIGN KEY (`department_id`) REFERENCES `departments_department` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. Semesters Table
CREATE TABLE IF NOT EXISTS `semesters_semester` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `number` INT UNSIGNED NOT NULL,
    `name` VARCHAR(100) NOT NULL,
    `start_date` DATE NOT NULL,
    `end_date` DATE NOT NULL,
    `is_active` TINYINT(1) NOT NULL DEFAULT 1,
    `course_id` BIGINT NOT NULL,
    FOREIGN KEY (`course_id`) REFERENCES `courses_course` (`id`) ON DELETE CASCADE,
    CONSTRAINT `chk_sem_dates` CHECK (`end_date` > `start_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. Subjects Table
CREATE TABLE IF NOT EXISTS `subjects_subject` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(150) NOT NULL,
    `code` VARCHAR(20) NOT NULL UNIQUE,
    `credits` INT UNSIGNED NOT NULL DEFAULT 4,
    `description` LONGTEXT NULL,
    `created_at` DATETIME(6) NOT NULL,
    `assigned_teacher_id` CHAR(36) NULL,
    `semester_id` BIGINT NOT NULL,
    FOREIGN KEY (`assigned_teacher_id`) REFERENCES `accounts_user` (`id`) ON DELETE SET NULL,
    FOREIGN KEY (`semester_id`) REFERENCES `semesters_semester` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. Questions Bank Table
CREATE TABLE IF NOT EXISTS `questions_question` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `question_type` VARCHAR(10) NOT NULL DEFAULT 'MCQ',
    `chapter` VARCHAR(150) NULL,
    `topic` VARCHAR(150) NULL,
    `marks` DECIMAL(5,2) NOT NULL DEFAULT 1.00,
    `difficulty` VARCHAR(10) NOT NULL DEFAULT 'MEDIUM',
    `prompt_text` LONGTEXT NOT NULL,
    `option_a` VARCHAR(500) NULL,
    `option_b` VARCHAR(500) NULL,
    `option_c` VARCHAR(500) NULL,
    `option_d` VARCHAR(500) NULL,
    `correct_answer` LONGTEXT NOT NULL,
    `explanation` LONGTEXT NULL,
    `image` VARCHAR(100) NULL,
    `tags` VARCHAR(255) NULL,
    `created_at` DATETIME(6) NOT NULL,
    `updated_at` DATETIME(6) NOT NULL,
    `subject_id` BIGINT NOT NULL,
    FOREIGN KEY (`subject_id`) REFERENCES `subjects_subject` (`id`) ON DELETE CASCADE,
    INDEX `idx_q_subj_diff` (`subject_id`, `difficulty`, `question_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 7. Exams Table
CREATE TABLE IF NOT EXISTS `exams_exam` (
    `id` CHAR(36) NOT NULL PRIMARY KEY,
    `title` VARCHAR(200) NOT NULL,
    `start_time` DATETIME(6) NOT NULL,
    `end_time` DATETIME(6) NOT NULL,
    `duration_minutes` INT UNSIGNED NOT NULL,
    `total_marks` DECIMAL(6,2) NOT NULL DEFAULT 100.00,
    `passing_marks` DECIMAL(6,2) NOT NULL DEFAULT 40.00,
    `negative_marking` DECIMAL(4,2) NOT NULL DEFAULT 0.00,
    `shuffle_questions` TINYINT(1) NOT NULL DEFAULT 1,
    `shuffle_options` TINYINT(1) NOT NULL DEFAULT 1,
    `attempt_limit` INT UNSIGNED NOT NULL DEFAULT 1,
    `password` VARCHAR(50) NULL,
    `instructions` LONGTEXT NOT NULL,
    `is_published` TINYINT(1) NOT NULL DEFAULT 0,
    `max_violations` INT UNSIGNED NOT NULL DEFAULT 3,
    `created_at` DATETIME(6) NOT NULL,
    `updated_at` DATETIME(6) NOT NULL,
    `created_by_id` CHAR(36) NOT NULL,
    `subject_id` BIGINT NOT NULL,
    FOREIGN KEY (`created_by_id`) REFERENCES `accounts_user` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`subject_id`) REFERENCES `subjects_subject` (`id`) ON DELETE CASCADE,
    CONSTRAINT `chk_passing_marks` CHECK (`passing_marks` <= `total_marks`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 8. Exam Attempts Table
CREATE TABLE IF NOT EXISTS `exams_examattempt` (
    `id` CHAR(36) NOT NULL PRIMARY KEY,
    `start_time` DATETIME(6) NOT NULL,
    `end_time` DATETIME(6) NULL,
    `status` VARCHAR(20) NOT NULL DEFAULT 'IN_PROGRESS',
    `total_score` DECIMAL(6,2) NOT NULL DEFAULT 0.00,
    `percentage` DECIMAL(5,2) NOT NULL DEFAULT 0.00,
    `is_passed` TINYINT(1) NOT NULL DEFAULT 0,
    `violations_count` INT UNSIGNED NOT NULL DEFAULT 0,
    `is_evaluated` TINYINT(1) NOT NULL DEFAULT 0,
    `question_order` JSON NOT NULL,
    `exam_id` CHAR(36) NOT NULL,
    `student_id` CHAR(36) NOT NULL,
    FOREIGN KEY (`exam_id`) REFERENCES `exams_exam` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`student_id`) REFERENCES `accounts_user` (`id`) ON DELETE CASCADE,
    INDEX `idx_attempt_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

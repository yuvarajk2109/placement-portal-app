-- ============================================================
-- Placement Portal Application - Database Schema
-- ============================================================

-- 1. Unified Authentication Table
CREATE TABLE User (
    user_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    email         VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role          VARCHAR(10)  NOT NULL CHECK (role IN ('admin', 'company', 'student')),
    is_active     BOOLEAN      NOT NULL DEFAULT 1,
    is_blacklisted BOOLEAN     NOT NULL DEFAULT 0,
    otp_code      VARCHAR(6),
    otp_expires_at DATETIME,
    is_verified    BOOLEAN     NOT NULL DEFAULT 0,
    created_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 2. Department
CREATE TABLE Department (
    dept_id   INTEGER PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL UNIQUE
);

-- 3. Branch (belongs to Department)
CREATE TABLE Branch (
    branch_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    branch_name VARCHAR(100) NOT NULL,
    dept_id     INTEGER      NOT NULL,
    FOREIGN KEY (dept_id) REFERENCES Department(dept_id),
    UNIQUE (branch_name, dept_id)
);

-- 4. Student Profile (extends User where role='student')
-- Only 3rd and 4th year students can register.
-- Year 3: eligible for 2-month internship drives only.
-- Year 4: eligible for all other drive types.
-- year_of_study is computed from register_no (joining year = first 4 digits).
CREATE TABLE Student (
    register_no   VARCHAR(20)  PRIMARY KEY,
    user_id       INTEGER      NOT NULL UNIQUE,
    first_name    VARCHAR(100) NOT NULL,
    last_name     VARCHAR(100) NOT NULL,
    dob           DATE,
    phone         VARCHAR(15),
    cgpa          REAL         NOT NULL DEFAULT 0.0,
    year_of_study INTEGER      NOT NULL CHECK (year_of_study IN (3, 4)),
    resume_path   VARCHAR(255),
    branch_id     INTEGER      NOT NULL,
    created_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id)   REFERENCES User(user_id),
    FOREIGN KEY (branch_id) REFERENCES Branch(branch_id)
);

-- 4a. Skill (Pre-defined skills)
CREATE TABLE Skill (
    skill_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    skill_name VARCHAR(100) NOT NULL UNIQUE
);

-- 4b. Student_Skill (Many-to-many relationship)
CREATE TABLE Student_Skill (
    register_no VARCHAR(20) NOT NULL,
    skill_id    INTEGER     NOT NULL,
    PRIMARY KEY (register_no, skill_id),
    FOREIGN KEY (register_no) REFERENCES Student(register_no),
    FOREIGN KEY (skill_id)    REFERENCES Skill(skill_id)
);

-- 5. Company Profile (extends User where role='company')
CREATE TABLE Company (
    company_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER      NOT NULL UNIQUE,
    company_name VARCHAR(200) NOT NULL,
    industry     VARCHAR(100),
    website      VARCHAR(255),
    location     VARCHAR(200),
    description  TEXT,
    hr_name      VARCHAR(100),
    hr_email     VARCHAR(255) NOT NULL,
    hr_phone     VARCHAR(15),
    status       VARCHAR(20)  NOT NULL DEFAULT 'pending'
                              CHECK (status IN ('pending', 'approved', 'rejected')),
    created_at   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);

-- 6. Placement Drive (created by Company)
CREATE TABLE Placement_Drive (
    drive_id            INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id          INTEGER      NOT NULL,
    job_title           VARCHAR(200) NOT NULL,
    job_description     TEXT         NOT NULL,
    drive_type          VARCHAR(40)  NOT NULL
                                     CHECK (drive_type IN (
                                         '2m_internship',
                                         '5m_internship', '6m_internship',
                                         '5m_internship_placement', '6m_internship_placement',
                                         '5m_internship_perf_placement', '6m_internship_perf_placement',
                                         'direct_placement'
                                     )),
    cgpa_requirement    REAL         NOT NULL DEFAULT 0.0,
    salary_min          REAL,
    salary_max          REAL,
    location            VARCHAR(200),
    deadline            TIMESTAMP    NOT NULL,
    status              VARCHAR(20)  NOT NULL DEFAULT 'pending'
                                     CHECK (status IN ('pending', 'approved', 'rejected', 'closed')),
    created_at          DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES Company(company_id)
);

-- 7. Drive–Branch Eligibility (M:N)
CREATE TABLE Drive_Branch (
    drive_id  INTEGER NOT NULL,
    branch_id INTEGER NOT NULL,
    PRIMARY KEY (drive_id, branch_id),
    FOREIGN KEY (drive_id)  REFERENCES Placement_Drive(drive_id),
    FOREIGN KEY (branch_id) REFERENCES Branch(branch_id)
);

-- 7a. Drive-Skill (M:N)
CREATE TABLE Drive_Skill (
    drive_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL,
    PRIMARY KEY (drive_id, skill_id),
    FOREIGN KEY (drive_id) REFERENCES Placement_Drive(drive_id),
    FOREIGN KEY (skill_id) REFERENCES Skill(skill_id)
);

-- 8. Interview Rounds (belong to a Drive)
CREATE TABLE Interview (
    interview_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    drive_id        INTEGER      NOT NULL,
    round_number    INTEGER      NOT NULL DEFAULT 1,
    round_title     VARCHAR(100) NOT NULL,      -- e.g., "Technical Round 1", "HR Round"
    interview_date  DATETIME,
    location        VARCHAR(200),               -- or "Online"
    created_at      DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (drive_id) REFERENCES Placement_Drive(drive_id),
    UNIQUE (drive_id, round_number)
);

-- 9. Application (Student applies to a Drive)
CREATE TABLE Application (
    application_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    register_no        VARCHAR(20)  NOT NULL,
    drive_id           INTEGER      NOT NULL,
    applied_date       DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    application_status VARCHAR(20)  NOT NULL DEFAULT 'applied'
                                    CHECK (application_status IN (
                                        'applied', 'shortlisted', 'interview',
                                        'selected', 'rejected', 'withdrawn'
                                    )),
    current_round_id   INTEGER,           -- FK to Interview (which round student is at)
    feedback           TEXT,              -- company feedback
    updated_at         DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (register_no)     REFERENCES Student(register_no),
    FOREIGN KEY (drive_id)        REFERENCES Placement_Drive(drive_id),
    FOREIGN KEY (current_round_id) REFERENCES Interview(interview_id),
    UNIQUE (register_no, drive_id)        -- prevent duplicate applications
);

-- 10. Placement Record (final confirmed placement)
CREATE TABLE Placement (
    placement_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    application_id INTEGER    NOT NULL UNIQUE,
    position      VARCHAR(200) NOT NULL,
    drive_type    VARCHAR(40)  NOT NULL,               -- copied from Placement_Drive at selection time
    salary        REAL,
    joining_date  DATE,
    created_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (application_id) REFERENCES Application(application_id)
);

-- ============================================================
-- Seed: Admin user (created programmatically in seed.py)
-- password_hash is bcrypt of a default password, generated in Python
-- ============================================================
-- INSERT INTO User (email, password_hash, role, is_active, is_verified)
-- VALUES ('admin@placement.edu', '<bcrypt_hash>', 'admin', 1, 1);

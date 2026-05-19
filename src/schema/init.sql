-- ============================================================
-- Hotel Booking & Management System
-- Database Initialization Script
-- Engine: InnoDB | Charset: UTF8MB4
-- ============================================================

DROP DATABASE IF EXISTS hotel_management;
CREATE DATABASE hotel_management
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE hotel_management;

-- ============================================================
-- 1. Guest - stores guest personal information
-- ============================================================
CREATE TABLE Guest (
    Guest_ID            INT             AUTO_INCREMENT,
    First_Name          VARCHAR(50)     NOT NULL,
    Last_Name           VARCHAR(50)     NOT NULL,
    Email               VARCHAR(100)    NOT NULL,
    Phone_Number        VARCHAR(20),
    Identity_Document   VARCHAR(50)     NOT NULL,
    Personal_Prefs      TEXT,
    Registration_Date   DATE            NOT NULL DEFAULT (CURDATE()),

    PRIMARY KEY (Guest_ID),
    UNIQUE KEY uk_guest_email    (Email),
    UNIQUE KEY uk_guest_identity (Identity_Document),
    INDEX idx_guest_name (Last_Name, First_Name)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci
  COMMENT = 'Hotel guests and their personal information';

-- ============================================================
-- 2. Loyalty_Program - one-to-one with Guest
-- ============================================================
CREATE TABLE Loyalty_Program (
    Loyalty_ID      INT             AUTO_INCREMENT,
    Guest_ID        INT             NOT NULL,
    Tier_Level      ENUM('Bronze', 'Silver', 'Gold', 'Platinum')
                                    NOT NULL DEFAULT 'Bronze',
    Available_Points INT            NOT NULL DEFAULT 0,
    Enrollment_Date DATE            NOT NULL DEFAULT (CURDATE()),

    PRIMARY KEY (Loyalty_ID),
    UNIQUE KEY uk_loyalty_guest (Guest_ID),
    INDEX idx_loyalty_tier (Tier_Level),

    CONSTRAINT fk_loyalty_guest
        FOREIGN KEY (Guest_ID) REFERENCES Guest (Guest_ID)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci
  COMMENT = 'Guest loyalty / rewards program membership';

-- ============================================================
-- 3. Room_Type - categories of rooms
-- ============================================================
CREATE TABLE Room_Type (
    Type_ID         INT             AUTO_INCREMENT,
    Category_Name   VARCHAR(50)     NOT NULL,
    Base_Nightly_Rate DECIMAL(10,2) NOT NULL,
    Max_Capacity    INT             NOT NULL,
    Description     TEXT,

    PRIMARY KEY (Type_ID),
    UNIQUE KEY uk_roomtype_category (Category_Name)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci
  COMMENT = 'Room categories with base pricing and capacity';

-- ============================================================
-- 4. Room - individual rooms in the hotel
-- ============================================================
CREATE TABLE Room (
    Room_ID         INT             AUTO_INCREMENT,
    Type_ID         INT             NOT NULL,
    Floor_Level     INT             NOT NULL,
    Current_Status  ENUM('Available', 'Occupied', 'Maintenance', 'Reserved')
                                    NOT NULL DEFAULT 'Available',

    PRIMARY KEY (Room_ID),
    INDEX idx_room_status (Current_Status),
    INDEX idx_room_floor  (Floor_Level),

    CONSTRAINT fk_room_roomtype
        FOREIGN KEY (Type_ID) REFERENCES Room_Type (Type_ID)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci
  COMMENT = 'Physical rooms with current availability status';

-- ============================================================
-- 5. Booking - reservation records
-- ============================================================
CREATE TABLE Booking (
    Booking_ID      INT             AUTO_INCREMENT,
    Guest_ID        INT             NOT NULL,
    Creation_Time   DATETIME        NOT NULL DEFAULT NOW(),
    Total_Guests    INT             NOT NULL DEFAULT 1,
    Overall_Status  ENUM('Confirmed', 'Checked-In', 'Checked-Out', 'Cancelled')
                                    NOT NULL DEFAULT 'Confirmed',
    Special_Requests TEXT,

    PRIMARY KEY (Booking_ID),
    INDEX idx_booking_guest  (Guest_ID),
    INDEX idx_booking_status (Overall_Status),
    INDEX idx_booking_time   (Creation_Time),

    CONSTRAINT fk_booking_guest
        FOREIGN KEY (Guest_ID) REFERENCES Guest (Guest_ID)
        ON UPDATE CASCADE ON DELETE RESTRICT,

    CONSTRAINT chk_booking_guests CHECK (Total_Guests > 0)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci
  COMMENT = 'Booking / reservation header records';

-- ============================================================
-- 6. Booking_Room_Detail - rooms assigned to each booking
-- ============================================================
CREATE TABLE Booking_Room_Detail (
    Detail_ID       INT             AUTO_INCREMENT,
    Booking_ID      INT             NOT NULL,
    Room_ID         INT             NOT NULL,
    CheckIn_Date    DATE            NOT NULL,
    CheckOut_Date   DATE            NOT NULL,
    Final_Agreed_Rate DECIMAL(10,2) NOT NULL,

    PRIMARY KEY (Detail_ID),
    INDEX idx_detail_booking (Booking_ID),
    INDEX idx_detail_room    (Room_ID),
    INDEX idx_detail_dates   (CheckIn_Date, CheckOut_Date),

    CONSTRAINT fk_detail_booking
        FOREIGN KEY (Booking_ID) REFERENCES Booking (Booking_ID)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_detail_room
        FOREIGN KEY (Room_ID) REFERENCES Room (Room_ID)
        ON UPDATE CASCADE ON DELETE RESTRICT,

    CONSTRAINT chk_detail_dates CHECK (CheckOut_Date > CheckIn_Date)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci
  COMMENT = 'Line-level room assignments and dates per booking';

-- ============================================================
-- 7. Payment - financial transactions per booking
-- ============================================================
CREATE TABLE Payment (
    Payment_ID      INT             AUTO_INCREMENT,
    Booking_ID      INT             NOT NULL,
    Amount          DECIMAL(10,2)   NOT NULL,
    Payment_Date    DATETIME        NOT NULL DEFAULT NOW(),
    Payment_Method  ENUM('Credit Card', 'Debit Card', 'Cash',
                         'Bank Transfer', 'Mobile Pay')
                                    NOT NULL,
    Status          ENUM('Completed', 'Pending', 'Refunded', 'Failed')
                                    NOT NULL DEFAULT 'Pending',

    PRIMARY KEY (Payment_ID),
    INDEX idx_payment_booking (Booking_ID),
    INDEX idx_payment_status  (Status),
    INDEX idx_payment_date    (Payment_Date),

    CONSTRAINT fk_payment_booking
        FOREIGN KEY (Booking_ID) REFERENCES Booking (Booking_ID)
        ON UPDATE CASCADE ON DELETE RESTRICT,

    CONSTRAINT chk_payment_amount CHECK (Amount > 0)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci
  COMMENT = 'Payment transactions linked to bookings';

-- ============================================================
-- 8. Dynamic_Pricing_Rule - event-driven price adjustments
-- ============================================================
CREATE TABLE Dynamic_Pricing_Rule (
    Rule_ID         INT             AUTO_INCREMENT,
    Event_Name      VARCHAR(100)    NOT NULL,
    Effective_Start DATE            NOT NULL,
    Effective_End   DATE            NOT NULL,
    Price_Multiplier DECIMAL(4,2)   NOT NULL DEFAULT 1.00,
    Priority        INT             NOT NULL DEFAULT 1,
    Is_Active       BOOLEAN         NOT NULL DEFAULT TRUE,

    PRIMARY KEY (Rule_ID),
    INDEX idx_pricing_dates  (Effective_Start, Effective_End),
    INDEX idx_pricing_active (Is_Active),

    CONSTRAINT chk_pricing_dates      CHECK (Effective_End >= Effective_Start),
    CONSTRAINT chk_pricing_multiplier CHECK (Price_Multiplier > 0)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci
  COMMENT = 'Dynamic pricing rules for seasonal / event-based rate adjustments';

-- ============================================================
-- 9. Department - organizational departments
-- ============================================================
CREATE TABLE Department (
    Dept_ID     INT             AUTO_INCREMENT,
    Dept_Name   VARCHAR(50)     NOT NULL,

    PRIMARY KEY (Dept_ID),
    UNIQUE KEY uk_dept_name (Dept_Name)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci
  COMMENT = 'Hotel departments (Housekeeping, Front Desk, etc.)';

-- ============================================================
-- 10. Staff - hotel employees
-- ============================================================
CREATE TABLE Staff (
    Staff_ID    INT             AUTO_INCREMENT,
    Dept_ID     INT             NOT NULL,
    Full_Name   VARCHAR(100)    NOT NULL,
    Job_Role    VARCHAR(50)     NOT NULL,
    Hire_Date   DATE            NOT NULL DEFAULT (CURDATE()),
    Phone       VARCHAR(20),

    PRIMARY KEY (Staff_ID),
    INDEX idx_staff_dept (Dept_ID),
    INDEX idx_staff_role (Job_Role),

    CONSTRAINT fk_staff_department
        FOREIGN KEY (Dept_ID) REFERENCES Department (Dept_ID)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci
  COMMENT = 'Hotel staff members and their department assignments';

-- ============================================================
-- 11. Task_Log - room-related maintenance / cleaning tasks
-- ============================================================
CREATE TABLE Task_Log (
    Log_ID          INT             AUTO_INCREMENT,
    Staff_ID        INT             NOT NULL,
    Room_ID         INT             NOT NULL,
    Task_Type       ENUM('Cleaning', 'Maintenance', 'Inspection', 'Setup')
                                    NOT NULL,
    Assigned_Time   DATETIME        NOT NULL DEFAULT NOW(),
    Completion_Time DATETIME,
    Duration_Minutes INT,
    Quality_Score   DECIMAL(3,1),

    PRIMARY KEY (Log_ID),
    INDEX idx_task_staff    (Staff_ID),
    INDEX idx_task_room     (Room_ID),
    INDEX idx_task_type     (Task_Type),
    INDEX idx_task_assigned (Assigned_Time),

    CONSTRAINT fk_tasklog_staff
        FOREIGN KEY (Staff_ID) REFERENCES Staff (Staff_ID)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_tasklog_room
        FOREIGN KEY (Room_ID) REFERENCES Room (Room_ID)
        ON UPDATE CASCADE ON DELETE RESTRICT,

    CONSTRAINT chk_task_quality CHECK (Quality_Score BETWEEN 0 AND 10)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci
  COMMENT = 'Task log for room cleaning, maintenance, and inspections';

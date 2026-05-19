-- ============================================================
-- Hotel Booking & Management System
-- Sample Test Data
-- ============================================================

USE hotel_management;

-- ============================================================
-- 1. Department (5 records)
-- ============================================================

-- Core operational departments of the hotel
INSERT INTO Department (Dept_ID, Dept_Name) VALUES
    (1, 'Front Desk'),
    (2, 'Housekeeping'),
    (3, 'Maintenance'),
    (4, 'Food & Beverage'),
    (5, 'Management');

-- ============================================================
-- 2. Staff (8 records)
-- ============================================================

-- Front Desk: receptionist and night auditor
INSERT INTO Staff (Staff_ID, Dept_ID, Full_Name, Job_Role, Hire_Date, Phone) VALUES
    (1, 1, 'Emily Carter',    'Receptionist',        '2023-03-15', '+1-555-0101'),
    (2, 1, 'James Liu',       'Night Auditor',       '2024-01-10', '+1-555-0102');

-- Housekeeping: supervisor and attendant
INSERT INTO Staff (Staff_ID, Dept_ID, Full_Name, Job_Role, Hire_Date, Phone) VALUES
    (3, 2, 'Maria Gonzalez',  'Housekeeping Supervisor', '2022-06-01', '+1-555-0201'),
    (4, 2, 'Aisha Patel',     'Room Attendant',      '2024-08-20', '+1-555-0202');

-- Maintenance: technician
INSERT INTO Staff (Staff_ID, Dept_ID, Full_Name, Job_Role, Hire_Date, Phone) VALUES
    (5, 3, 'Robert Chen',     'Maintenance Technician', '2023-11-05', '+1-555-0301');

-- F&B: chef and waiter
INSERT INTO Staff (Staff_ID, Dept_ID, Full_Name, Job_Role, Hire_Date, Phone) VALUES
    (6, 4, 'Pierre Dupont',   'Executive Chef',      '2021-09-12', '+1-555-0401'),
    (7, 4, 'Sarah Kim',       'Restaurant Server',   '2025-02-01', '+1-555-0402');

-- Management: general manager
INSERT INTO Staff (Staff_ID, Dept_ID, Full_Name, Job_Role, Hire_Date, Phone) VALUES
    (8, 5, 'David Thompson',  'General Manager',     '2020-01-15', '+1-555-0501');

-- ============================================================
-- 3. Room_Type (5 records)
-- ============================================================

-- Five room categories with ascending pricing
INSERT INTO Room_Type (Type_ID, Category_Name, Base_Nightly_Rate, Max_Capacity, Description) VALUES
    (1, 'Standard Single',     80.00,  1, 'Cozy single room with queen bed, work desk, and city view. 22 sqm.'),
    (2, 'Standard Double',    130.00,  2, 'Spacious room with king bed or two doubles, sitting area. 30 sqm.'),
    (3, 'Deluxe Suite',       250.00,  3, 'Luxury suite with separate living area, marble bathroom, and balcony. 55 sqm.'),
    (4, 'Family Room',        200.00,  4, 'Family-friendly room with two queen beds, play corner, and kitchenette. 45 sqm.'),
    (5, 'Presidential Suite', 500.00,  4, 'Top-floor penthouse with panoramic views, private dining, butler service. 120 sqm.');

-- ============================================================
-- 4. Room (12 records)
-- ============================================================

-- Floor 1: ground-level standard rooms
INSERT INTO Room (Room_ID, Type_ID, Floor_Level, Current_Status) VALUES
    (101, 1, 1, 'Available'),       -- Standard Single, ready for booking
    (102, 1, 1, 'Occupied'),        -- Standard Single, currently occupied
    (103, 2, 1, 'Available');       -- Standard Double, ready for booking

-- Floor 2: standard and family rooms
INSERT INTO Room (Room_ID, Type_ID, Floor_Level, Current_Status) VALUES
    (201, 2, 2, 'Occupied'),        -- Standard Double, currently occupied
    (202, 2, 2, 'Reserved'),        -- Standard Double, reserved for upcoming guest
    (203, 4, 2, 'Available');       -- Family Room, ready for booking

-- Floor 3: mix of types
INSERT INTO Room (Room_ID, Type_ID, Floor_Level, Current_Status) VALUES
    (301, 1, 3, 'Maintenance'),     -- Standard Single, under maintenance
    (302, 3, 3, 'Available'),       -- Deluxe Suite, ready for booking
    (303, 3, 3, 'Occupied');        -- Deluxe Suite, currently occupied

-- Floor 4: premium rooms
INSERT INTO Room (Room_ID, Type_ID, Floor_Level, Current_Status) VALUES
    (401, 4, 4, 'Available'),       -- Family Room, ready for booking
    (402, 3, 4, 'Reserved'),        -- Deluxe Suite, reserved
    (403, 5, 4, 'Available');       -- Presidential Suite, ready for booking

-- ============================================================
-- 5. Guest (10 records)
-- ============================================================

-- Regular business traveler
INSERT INTO Guest (Guest_ID, First_Name, Last_Name, Email, Phone_Number, Identity_Document, Personal_Prefs, Registration_Date) VALUES
    (1, 'Michael',  'Anderson',  'michael.anderson@gmail.com',   '+1-212-555-1001', 'US-P4823751',  'Non-smoking, high floor, extra pillows',          '2025-06-10');

-- Frequent guest, loyalty member
INSERT INTO Guest (Guest_ID, First_Name, Last_Name, Email, Phone_Number, Identity_Document, Personal_Prefs, Registration_Date) VALUES
    (2, 'Sophie',   'Williams',  'sophie.williams@outlook.com',  '+44-20-7946-0958', 'GB-P91284567', 'Late checkout preferred, hypoallergenic bedding',  '2024-11-22');

-- Family traveler
INSERT INTO Guest (Guest_ID, First_Name, Last_Name, Email, Phone_Number, Identity_Document, Personal_Prefs, Registration_Date) VALUES
    (3, 'Kenji',    'Tanaka',    'kenji.tanaka@yahoo.co.jp',     '+81-3-5555-2030',  'JP-TK7829014', 'Crib required, Japanese breakfast option',          '2025-01-15');

-- Couple on vacation
INSERT INTO Guest (Guest_ID, First_Name, Last_Name, Email, Phone_Number, Identity_Document, Personal_Prefs, Registration_Date) VALUES
    (4, 'Isabella', 'Rossi',     'isabella.rossi@libero.it',     '+39-06-555-3041',  'IT-YA4521879', 'Quiet room, vegetarian meal options',               '2025-03-08');

-- Corporate executive
INSERT INTO Guest (Guest_ID, First_Name, Last_Name, Email, Phone_Number, Identity_Document, Personal_Prefs, Registration_Date) VALUES
    (5, 'Alexander','Petrov',    'a.petrov@corp-solutions.com',  '+7-495-555-4052',  'RU-7201458390','Suite preferred, airport transfer needed',          '2025-02-20');

-- Young solo traveler
INSERT INTO Guest (Guest_ID, First_Name, Last_Name, Email, Phone_Number, Identity_Document, Personal_Prefs, Registration_Date) VALUES
    (6, 'Emma',     'Johansson', 'emma.johansson@protonmail.com','+46-8-555-5063',   'SE-82014573',  'Gym access, early check-in',                        '2025-07-01');

-- Honeymooners
INSERT INTO Guest (Guest_ID, First_Name, Last_Name, Email, Phone_Number, Identity_Document, Personal_Prefs, Registration_Date) VALUES
    (7, 'Carlos',   'Mendez',    'carlos.mendez@hotmail.com',    '+52-55-5555-6074', 'MX-G12847560', 'Rose petals, champagne on arrival',                 '2025-09-12');

-- Repeat corporate traveler
INSERT INTO Guest (Guest_ID, First_Name, Last_Name, Email, Phone_Number, Identity_Document, Personal_Prefs, Registration_Date) VALUES
    (8, 'Rachel',   'Cohen',     'rachel.cohen@techstartup.io',  '+1-415-555-7085',  'US-P5937284',  'Fast WiFi essential, standing desk if available',   '2025-04-18');

-- Elderly couple
INSERT INTO Guest (Guest_ID, First_Name, Last_Name, Email, Phone_Number, Identity_Document, Personal_Prefs, Registration_Date) VALUES
    (9, 'Hans',     'Mueller',   'hans.mueller@web.de',          '+49-30-555-8096',  'DE-C4FR28197', 'Ground floor preferred, accessibility needs',       '2025-05-30');

-- Tourist with group booking
INSERT INTO Guest (Guest_ID, First_Name, Last_Name, Email, Phone_Number, Identity_Document, Personal_Prefs, Registration_Date) VALUES
    (10,'Priya',    'Sharma',    'priya.sharma@rediffmail.com',  '+91-11-5555-9007', 'IN-K8724510',  'Connecting rooms, vegetarian only',                 '2025-08-25');

-- ============================================================
-- 6. Loyalty_Program (6 records)
-- ============================================================

-- Top-tier loyal guest with many stays
INSERT INTO Loyalty_Program (Loyalty_ID, Guest_ID, Tier_Level, Available_Points, Enrollment_Date) VALUES
    (1, 2, 'Platinum', 28500, '2024-11-22');

-- Gold member, frequent business traveler
INSERT INTO Loyalty_Program (Loyalty_ID, Guest_ID, Tier_Level, Available_Points, Enrollment_Date) VALUES
    (2, 1, 'Gold',     12300, '2025-06-10');

-- Silver member, moderate stays
INSERT INTO Loyalty_Program (Loyalty_ID, Guest_ID, Tier_Level, Available_Points, Enrollment_Date) VALUES
    (3, 5, 'Silver',    6800, '2025-02-20');

-- Bronze member, recently enrolled
INSERT INTO Loyalty_Program (Loyalty_ID, Guest_ID, Tier_Level, Available_Points, Enrollment_Date) VALUES
    (4, 8, 'Bronze',    1500, '2025-04-18');

-- Silver member, repeat corporate guest
INSERT INTO Loyalty_Program (Loyalty_ID, Guest_ID, Tier_Level, Available_Points, Enrollment_Date) VALUES
    (5, 3, 'Silver',    4200, '2025-01-15');

-- Bronze member, new enrollment
INSERT INTO Loyalty_Program (Loyalty_ID, Guest_ID, Tier_Level, Available_Points, Enrollment_Date) VALUES
    (6, 10, 'Bronze',    800, '2025-08-25');

-- ============================================================
-- 7. Dynamic_Pricing_Rule (4 records)
-- ============================================================

-- Christmas / New Year peak season: 80% surcharge
INSERT INTO Dynamic_Pricing_Rule (Rule_ID, Event_Name, Effective_Start, Effective_End, Price_Multiplier, Priority, Is_Active) VALUES
    (1, 'Christmas & New Year Peak',   '2025-12-20', '2026-01-05', 1.80, 10, TRUE);

-- Chinese New Year / Spring Festival: 50% surcharge
INSERT INTO Dynamic_Pricing_Rule (Rule_ID, Event_Name, Effective_Start, Effective_End, Price_Multiplier, Priority, Is_Active) VALUES
    (2, 'Spring Festival',             '2026-01-28', '2026-02-04', 1.50,  8, TRUE);

-- Summer high season: 30% surcharge (June-August)
INSERT INTO Dynamic_Pricing_Rule (Rule_ID, Event_Name, Effective_Start, Effective_End, Price_Multiplier, Priority, Is_Active) VALUES
    (3, 'Summer High Season',          '2026-06-01', '2026-08-31', 1.30,  5, TRUE);

-- Weekday discount: 15% off (ongoing promotion for low-occupancy periods)
INSERT INTO Dynamic_Pricing_Rule (Rule_ID, Event_Name, Effective_Start, Effective_End, Price_Multiplier, Priority, Is_Active) VALUES
    (4, 'Weekday Discount',            '2026-01-06', '2026-05-31', 0.85,  1, TRUE);

-- ============================================================
-- 8. Booking (15 records)
-- ============================================================

-- B1: Christmas stay, checked out (Guest 2 - Platinum member, repeat guest)
INSERT INTO Booking (Booking_ID, Guest_ID, Creation_Time, Total_Guests, Overall_Status, Special_Requests) VALUES
    (1, 2, '2025-12-01 09:30:00', 1, 'Checked-Out', 'Late checkout on departure day');

-- B2: New Year family stay, checked out (Guest 3 - family with kids)
INSERT INTO Booking (Booking_ID, Guest_ID, Creation_Time, Total_Guests, Overall_Status, Special_Requests) VALUES
    (2, 3, '2025-12-10 14:20:00', 4, 'Checked-Out', 'Baby crib in room, extra towels');

-- B3: January business trip, checked out (Guest 1)
INSERT INTO Booking (Booking_ID, Guest_ID, Creation_Time, Total_Guests, Overall_Status, Special_Requests) VALUES
    (3, 1, '2025-12-28 11:00:00', 1, 'Checked-Out', NULL);

-- B4: Spring Festival cancelled booking (Guest 4 - cancelled due to travel change)
INSERT INTO Booking (Booking_ID, Guest_ID, Creation_Time, Total_Guests, Overall_Status, Special_Requests) VALUES
    (4, 4, '2026-01-05 16:45:00', 2, 'Cancelled', 'Honeymoon package requested');

-- B5: February corporate stay, checked out (Guest 5 - executive)
INSERT INTO Booking (Booking_ID, Guest_ID, Creation_Time, Total_Guests, Overall_Status, Special_Requests) VALUES
    (5, 5, '2026-01-20 08:15:00', 1, 'Checked-Out', 'Airport pickup at 14:00');

-- B6: Multi-room group booking, checked out (Guest 10 - tourist group, 2 rooms)
INSERT INTO Booking (Booking_ID, Guest_ID, Creation_Time, Total_Guests, Overall_Status, Special_Requests) VALUES
    (6, 10, '2026-02-01 10:00:00', 4, 'Checked-Out', 'Connecting rooms preferred');

-- B7: March solo trip, checked out (Guest 6)
INSERT INTO Booking (Booking_ID, Guest_ID, Creation_Time, Total_Guests, Overall_Status, Special_Requests) VALUES
    (7, 6, '2026-02-15 19:30:00', 1, 'Checked-Out', 'Gym pass included');

-- B8: Repeat guest second booking, checked out (Guest 2 - Platinum member returns)
INSERT INTO Booking (Booking_ID, Guest_ID, Creation_Time, Total_Guests, Overall_Status, Special_Requests) VALUES
    (8, 2, '2026-02-28 12:00:00', 2, 'Checked-Out', 'Same room as last stay if possible');

-- B9: Cancelled last minute (Guest 7 - honeymoon postponed)
INSERT INTO Booking (Booking_ID, Guest_ID, Creation_Time, Total_Guests, Overall_Status, Special_Requests) VALUES
    (9, 7, '2026-03-01 20:10:00', 2, 'Cancelled', 'Champagne and roses, anniversary celebration');

-- B10: April business trip, checked out (Guest 8 - startup founder)
INSERT INTO Booking (Booking_ID, Guest_ID, Creation_Time, Total_Guests, Overall_Status, Special_Requests) VALUES
    (10, 8, '2026-03-15 07:45:00', 1, 'Checked-Out', 'Need printer access');

-- B11: Elderly couple spring trip, checked out (Guest 9)
INSERT INTO Booking (Booking_ID, Guest_ID, Creation_Time, Total_Guests, Overall_Status, Special_Requests) VALUES
    (11, 9, '2026-03-20 15:00:00', 2, 'Checked-Out', 'Wheelchair accessible room, ground floor');

-- B12: Currently checked in (Guest 1 - third visit this year, multi-room)
INSERT INTO Booking (Booking_ID, Guest_ID, Creation_Time, Total_Guests, Overall_Status, Special_Requests) VALUES
    (12, 1, '2026-05-01 10:30:00', 2, 'Checked-In', 'Meeting room needed for May 14');

-- B13: Upcoming confirmed reservation (Guest 4 - rebooked after cancellation)
INSERT INTO Booking (Booking_ID, Guest_ID, Creation_Time, Total_Guests, Overall_Status, Special_Requests) VALUES
    (13, 4, '2026-05-05 09:00:00', 2, 'Confirmed', 'Anniversary dinner arrangement');

-- B14: Upcoming confirmed reservation (Guest 7)
INSERT INTO Booking (Booking_ID, Guest_ID, Creation_Time, Total_Guests, Overall_Status, Special_Requests) VALUES
    (14, 7, '2026-05-10 11:20:00', 2, 'Confirmed', 'Honeymoon package - flowers and wine');

-- B15: Currently checked in (Guest 5 - second corporate visit)
INSERT INTO Booking (Booking_ID, Guest_ID, Creation_Time, Total_Guests, Overall_Status, Special_Requests) VALUES
    (15, 5, '2026-05-08 13:00:00', 1, 'Checked-In', 'Early breakfast at 6:00 AM');

-- ============================================================
-- 9. Booking_Room_Detail (18 records)
-- ============================================================

-- B1: Christmas Deluxe Suite stay (3 nights at Christmas rate: 250 * 1.8 = 450/night)
INSERT INTO Booking_Room_Detail (Detail_ID, Booking_ID, Room_ID, CheckIn_Date, CheckOut_Date, Final_Agreed_Rate) VALUES
    (1, 1, 303, '2025-12-23', '2025-12-26', 450.00);

-- B2: New Year family stay - Family Room (4 nights at Christmas rate: 200 * 1.8 = 360/night)
INSERT INTO Booking_Room_Detail (Detail_ID, Booking_ID, Room_ID, CheckIn_Date, CheckOut_Date, Final_Agreed_Rate) VALUES
    (2, 2, 203, '2025-12-28', '2026-01-01', 360.00);

-- B3: January business - Standard Single (3 nights, weekday discount: 80 * 0.85 = 68/night)
INSERT INTO Booking_Room_Detail (Detail_ID, Booking_ID, Room_ID, CheckIn_Date, CheckOut_Date, Final_Agreed_Rate) VALUES
    (3, 3, 101, '2026-01-12', '2026-01-15', 68.00);

-- B4: Cancelled Spring Festival booking - Standard Double (would have been 130 * 1.5 = 195/night)
INSERT INTO Booking_Room_Detail (Detail_ID, Booking_ID, Room_ID, CheckIn_Date, CheckOut_Date, Final_Agreed_Rate) VALUES
    (4, 4, 103, '2026-01-29', '2026-02-02', 195.00);

-- B5: February corporate - Deluxe Suite (5 nights, weekday discount: 250 * 0.85 = 212.50/night)
INSERT INTO Booking_Room_Detail (Detail_ID, Booking_ID, Room_ID, CheckIn_Date, CheckOut_Date, Final_Agreed_Rate) VALUES
    (5, 5, 302, '2026-02-03', '2026-02-08', 212.50);

-- B6: Group booking - two rooms: Standard Double + Standard Double (3 nights each, weekday: 130 * 0.85 = 110.50)
INSERT INTO Booking_Room_Detail (Detail_ID, Booking_ID, Room_ID, CheckIn_Date, CheckOut_Date, Final_Agreed_Rate) VALUES
    (6, 6, 103, '2026-02-10', '2026-02-13', 110.50);
INSERT INTO Booking_Room_Detail (Detail_ID, Booking_ID, Room_ID, CheckIn_Date, CheckOut_Date, Final_Agreed_Rate) VALUES
    (7, 6, 201, '2026-02-10', '2026-02-13', 110.50);

-- B7: Solo March trip - Standard Single (4 nights, weekday discount: 80 * 0.85 = 68/night)
INSERT INTO Booking_Room_Detail (Detail_ID, Booking_ID, Room_ID, CheckIn_Date, CheckOut_Date, Final_Agreed_Rate) VALUES
    (8, 7, 102, '2026-03-02', '2026-03-06', 68.00);

-- B8: Repeat guest Deluxe Suite (2 nights, weekday: 250 * 0.85 = 212.50/night)
INSERT INTO Booking_Room_Detail (Detail_ID, Booking_ID, Room_ID, CheckIn_Date, CheckOut_Date, Final_Agreed_Rate) VALUES
    (9, 8, 303, '2026-03-10', '2026-03-12', 212.50);

-- B9: Cancelled honeymoon - Presidential Suite (would have been 500 * 0.85 = 425/night)
INSERT INTO Booking_Room_Detail (Detail_ID, Booking_ID, Room_ID, CheckIn_Date, CheckOut_Date, Final_Agreed_Rate) VALUES
    (10, 9, 403, '2026-03-20', '2026-03-24', 425.00);

-- B10: April business - Standard Single (2 nights, weekday: 80 * 0.85 = 68/night)
INSERT INTO Booking_Room_Detail (Detail_ID, Booking_ID, Room_ID, CheckIn_Date, CheckOut_Date, Final_Agreed_Rate) VALUES
    (11, 10, 101, '2026-04-06', '2026-04-08', 68.00);

-- B11: Elderly couple - Standard Double on ground floor (5 nights, weekday: 130 * 0.85 = 110.50/night)
INSERT INTO Booking_Room_Detail (Detail_ID, Booking_ID, Room_ID, CheckIn_Date, CheckOut_Date, Final_Agreed_Rate) VALUES
    (12, 11, 103, '2026-04-10', '2026-04-15', 110.50);

-- B12: Currently checked in - two rooms: Standard Double + Deluxe Suite (same room 101 reused by different guest)
--      Standard Double (7 nights, weekday: 130 * 0.85 = 110.50/night)
INSERT INTO Booking_Room_Detail (Detail_ID, Booking_ID, Room_ID, CheckIn_Date, CheckOut_Date, Final_Agreed_Rate) VALUES
    (13, 12, 201, '2026-05-12', '2026-05-19', 110.50);
--      Deluxe Suite (7 nights, weekday: 250 * 0.85 = 212.50/night)
INSERT INTO Booking_Room_Detail (Detail_ID, Booking_ID, Room_ID, CheckIn_Date, CheckOut_Date, Final_Agreed_Rate) VALUES
    (14, 12, 303, '2026-05-12', '2026-05-19', 212.50);

-- B13: Upcoming confirmed - Standard Double reserved (3 nights, weekday: 130 * 0.85 = 110.50/night)
INSERT INTO Booking_Room_Detail (Detail_ID, Booking_ID, Room_ID, CheckIn_Date, CheckOut_Date, Final_Agreed_Rate) VALUES
    (15, 13, 202, '2026-05-25', '2026-05-28', 110.50);

-- B14: Upcoming confirmed honeymoon - Presidential Suite (4 nights, base rate: 500/night)
INSERT INTO Booking_Room_Detail (Detail_ID, Booking_ID, Room_ID, CheckIn_Date, CheckOut_Date, Final_Agreed_Rate) VALUES
    (16, 14, 403, '2026-06-01', '2026-06-05', 500.00);

-- B15: Currently checked in - Deluxe Suite (5 nights, weekday: 250 * 0.85 = 212.50/night)
INSERT INTO Booking_Room_Detail (Detail_ID, Booking_ID, Room_ID, CheckIn_Date, CheckOut_Date, Final_Agreed_Rate) VALUES
    (17, 15, 402, '2026-05-14', '2026-05-19', 212.50);

-- B2 additional: Family also booked a Standard Single for the nanny (4 nights, Christmas: 80 * 1.8 = 144/night)
INSERT INTO Booking_Room_Detail (Detail_ID, Booking_ID, Room_ID, CheckIn_Date, CheckOut_Date, Final_Agreed_Rate) VALUES
    (18, 2, 102, '2025-12-28', '2026-01-01', 144.00);

-- ============================================================
-- 10. Payment (12 records)
-- ============================================================

-- B1: Christmas Deluxe Suite - paid in full (3 nights * 450 = 1350)
INSERT INTO Payment (Payment_ID, Booking_ID, Amount, Payment_Date, Payment_Method, Status) VALUES
    (1, 1, 1350.00, '2025-12-23 14:05:00', 'Credit Card', 'Completed');

-- B2: New Year family stay - paid in full (4 nights * 360 + 4 nights * 144 = 1440 + 576 = 2016)
INSERT INTO Payment (Payment_ID, Booking_ID, Amount, Payment_Date, Payment_Method, Status) VALUES
    (2, 2, 2016.00, '2025-12-28 15:30:00', 'Credit Card', 'Completed');

-- B3: January business trip - paid (3 nights * 68 = 204)
INSERT INTO Payment (Payment_ID, Booking_ID, Amount, Payment_Date, Payment_Method, Status) VALUES
    (3, 3, 204.00, '2026-01-12 12:00:00', 'Bank Transfer', 'Completed');

-- B4: Cancelled Spring Festival - deposit paid then refunded (partial deposit of 195)
INSERT INTO Payment (Payment_ID, Booking_ID, Amount, Payment_Date, Payment_Method, Status) VALUES
    (4, 4, 195.00, '2026-01-05 17:00:00', 'Credit Card', 'Refunded');

-- B5: Corporate Deluxe Suite stay - paid (5 nights * 212.50 = 1062.50)
INSERT INTO Payment (Payment_ID, Booking_ID, Amount, Payment_Date, Payment_Method, Status) VALUES
    (5, 5, 1062.50, '2026-02-08 10:00:00', 'Bank Transfer', 'Completed');

-- B6: Group booking two rooms - paid (3 nights * 110.50 * 2 rooms = 663)
INSERT INTO Payment (Payment_ID, Booking_ID, Amount, Payment_Date, Payment_Method, Status) VALUES
    (6, 6, 663.00, '2026-02-10 11:30:00', 'Debit Card', 'Completed');

-- B7: Solo March trip - paid by mobile (4 nights * 68 = 272)
INSERT INTO Payment (Payment_ID, Booking_ID, Amount, Payment_Date, Payment_Method, Status) VALUES
    (7, 7, 272.00, '2026-03-02 16:00:00', 'Mobile Pay', 'Completed');

-- B8: Repeat Platinum guest - paid (2 nights * 212.50 = 425)
INSERT INTO Payment (Payment_ID, Booking_ID, Amount, Payment_Date, Payment_Method, Status) VALUES
    (8, 8, 425.00, '2026-03-12 09:45:00', 'Credit Card', 'Completed');

-- B9: Cancelled honeymoon - deposit refunded (one night deposit: 425)
INSERT INTO Payment (Payment_ID, Booking_ID, Amount, Payment_Date, Payment_Method, Status) VALUES
    (9, 9, 425.00, '2026-03-02 08:00:00', 'Credit Card', 'Refunded');

-- B10: April business - cash payment (2 nights * 68 = 136)
INSERT INTO Payment (Payment_ID, Booking_ID, Amount, Payment_Date, Payment_Method, Status) VALUES
    (10, 10, 136.00, '2026-04-06 14:20:00', 'Cash', 'Completed');

-- B11: Elderly couple spring trip - paid (5 nights * 110.50 = 552.50)
INSERT INTO Payment (Payment_ID, Booking_ID, Amount, Payment_Date, Payment_Method, Status) VALUES
    (11, 11, 552.50, '2026-04-10 16:00:00', 'Debit Card', 'Completed');

-- B12: Currently checked in - deposit pending full settlement (partial: 1 night each room = 110.50 + 212.50 = 323)
INSERT INTO Payment (Payment_ID, Booking_ID, Amount, Payment_Date, Payment_Method, Status) VALUES
    (12, 12, 323.00, '2026-05-12 11:00:00', 'Credit Card', 'Pending');

-- ============================================================
-- 11. Task_Log (15 records)
-- ============================================================

-- Post-checkout deep cleaning for B1 Christmas guest
INSERT INTO Task_Log (Log_ID, Staff_ID, Room_ID, Task_Type, Assigned_Time, Completion_Time, Duration_Minutes, Quality_Score) VALUES
    (1, 3, 303, 'Cleaning', '2025-12-26 11:00:00', '2025-12-26 12:15:00', 75, 9.5);

-- Routine inspection after New Year
INSERT INTO Task_Log (Log_ID, Staff_ID, Room_ID, Task_Type, Assigned_Time, Completion_Time, Duration_Minutes, Quality_Score) VALUES
    (2, 3, 203, 'Inspection', '2026-01-01 14:00:00', '2026-01-01 14:30:00', 30, 8.0);

-- Post-checkout cleaning for B2 family room
INSERT INTO Task_Log (Log_ID, Staff_ID, Room_ID, Task_Type, Assigned_Time, Completion_Time, Duration_Minutes, Quality_Score) VALUES
    (3, 4, 203, 'Cleaning', '2026-01-01 15:00:00', '2026-01-01 16:30:00', 90, 7.5);

-- Maintenance: AC repair in room 301 (reason it is in Maintenance status)
INSERT INTO Task_Log (Log_ID, Staff_ID, Room_ID, Task_Type, Assigned_Time, Completion_Time, Duration_Minutes, Quality_Score) VALUES
    (4, 5, 301, 'Maintenance', '2026-01-10 09:00:00', NULL, NULL, NULL);

-- Post-checkout cleaning for B3 business guest
INSERT INTO Task_Log (Log_ID, Staff_ID, Room_ID, Task_Type, Assigned_Time, Completion_Time, Duration_Minutes, Quality_Score) VALUES
    (5, 4, 101, 'Cleaning', '2026-01-15 12:00:00', '2026-01-15 12:45:00', 45, 8.5);

-- Setup for corporate guest B5 - extra amenities placement
INSERT INTO Task_Log (Log_ID, Staff_ID, Room_ID, Task_Type, Assigned_Time, Completion_Time, Duration_Minutes, Quality_Score) VALUES
    (6, 3, 302, 'Setup', '2026-02-03 10:00:00', '2026-02-03 10:40:00', 40, 9.0);

-- Plumbing repair in room 201
INSERT INTO Task_Log (Log_ID, Staff_ID, Room_ID, Task_Type, Assigned_Time, Completion_Time, Duration_Minutes, Quality_Score) VALUES
    (7, 5, 201, 'Maintenance', '2026-02-12 08:00:00', '2026-02-12 10:30:00', 150, 7.0);

-- Post-checkout cleaning for solo traveler B7
INSERT INTO Task_Log (Log_ID, Staff_ID, Room_ID, Task_Type, Assigned_Time, Completion_Time, Duration_Minutes, Quality_Score) VALUES
    (8, 4, 102, 'Cleaning', '2026-03-06 12:00:00', '2026-03-06 12:40:00', 40, 9.0);

-- Deep cleaning Deluxe Suite after Platinum guest B8
INSERT INTO Task_Log (Log_ID, Staff_ID, Room_ID, Task_Type, Assigned_Time, Completion_Time, Duration_Minutes, Quality_Score) VALUES
    (9, 3, 303, 'Cleaning', '2026-03-12 13:00:00', '2026-03-12 14:30:00', 90, 9.8);

-- Inspection of Presidential Suite before upcoming booking
INSERT INTO Task_Log (Log_ID, Staff_ID, Room_ID, Task_Type, Assigned_Time, Completion_Time, Duration_Minutes, Quality_Score) VALUES
    (10, 3, 403, 'Inspection', '2026-03-25 10:00:00', '2026-03-25 10:45:00', 45, 8.5);

-- Post-checkout cleaning for B10
INSERT INTO Task_Log (Log_ID, Staff_ID, Room_ID, Task_Type, Assigned_Time, Completion_Time, Duration_Minutes, Quality_Score) VALUES
    (11, 4, 101, 'Cleaning', '2026-04-08 11:00:00', '2026-04-08 11:35:00', 35, 8.0);

-- Post-checkout cleaning for elderly couple B11
INSERT INTO Task_Log (Log_ID, Staff_ID, Room_ID, Task_Type, Assigned_Time, Completion_Time, Duration_Minutes, Quality_Score) VALUES
    (12, 4, 103, 'Cleaning', '2026-04-15 13:00:00', '2026-04-15 13:50:00', 50, 8.5);

-- Setup for current guest B12 - multi-room preparation
INSERT INTO Task_Log (Log_ID, Staff_ID, Room_ID, Task_Type, Assigned_Time, Completion_Time, Duration_Minutes, Quality_Score) VALUES
    (13, 3, 201, 'Setup', '2026-05-12 08:00:00', '2026-05-12 08:50:00', 50, 9.0);

-- Light bulb replacement in room 401 - completed quickly
INSERT INTO Task_Log (Log_ID, Staff_ID, Room_ID, Task_Type, Assigned_Time, Completion_Time, Duration_Minutes, Quality_Score) VALUES
    (14, 5, 401, 'Maintenance', '2026-05-13 14:00:00', '2026-05-13 14:20:00', 20, 7.5);

-- Pending inspection for reserved room 402 before guest B15 check-in (not yet completed)
INSERT INTO Task_Log (Log_ID, Staff_ID, Room_ID, Task_Type, Assigned_Time, Completion_Time, Duration_Minutes, Quality_Score) VALUES
    (15, 3, 402, 'Setup', '2026-05-14 07:00:00', '2026-05-14 07:55:00', 55, 9.2);

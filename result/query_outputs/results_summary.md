# Query Result Summary — hotel_management

Database: `hotel_management` · MySQL 8.0.45 · All 12 queries executed against the live instance.


### Q01 — Total spending and booking count per guest

_10 row(s) returned. Top 8 shown:_

|   Guest_ID | Guest_Name       | Email                         |   Total_Bookings |   Total_Spent |
|-----------:|:-----------------|:------------------------------|-----------------:|--------------:|
|          3 | Kenji Tanaka     | kenji.tanaka@yahoo.co.jp      |                1 |        2016   |
|          2 | Sophie Williams  | sophie.williams@outlook.com   |                2 |        1775   |
|          5 | Alexander Petrov | a.petrov@corp-solutions.com   |                2 |        1062.5 |
|         10 | Priya Sharma     | priya.sharma@rediffmail.com   |                1 |         663   |
|          9 | Hans Mueller     | hans.mueller@web.de           |                1 |         552.5 |
|          6 | Emma Johansson   | emma.johansson@protonmail.com |                1 |         272   |
|          1 | Michael Anderson | michael.anderson@gmail.com    |                2 |         204   |
|          8 | Rachel Cohen     | rachel.cohen@techstartup.io   |                1 |         136   |


### Q02 — Occupancy rate by room type (cancelled excluded)

_5 row(s) returned. Top 5 shown:_

|   Type_ID | Category_Name      |   Room_Count |   Total_Booked_Nights |   Occupancy_Rate_Pct |
|----------:|:-------------------|-------------:|----------------------:|---------------------:|
|         3 | Deluxe Suite       |            3 |                    22 |                 2.01 |
|         2 | Standard Double    |            3 |                    21 |                 1.92 |
|         1 | Standard Single    |            3 |                    13 |                 1.19 |
|         5 | Presidential Suite |            1 |                     4 |                 1.1  |
|         4 | Family Room        |            2 |                     4 |                 0.55 |


### Q03 — Dynamic pricing impact — actual vs base nightly rate

_20 row(s) returned. Top 8 shown:_

|   Detail_ID | Category_Name      |   Base_Nightly_Rate |   Actual_Rate | Event_Name                |   Price_Multiplier |   Rule_Suggested_Rate |   Actual_Premium_Pct | Pricing_Impact    |
|------------:|:-------------------|--------------------:|--------------:|:--------------------------|-------------------:|----------------------:|---------------------:|:------------------|
|           1 | Deluxe Suite       |                 250 |         450   | Christmas & New Year Peak |               1.8  |                 450   |                   80 | High Surge        |
|           2 | Family Room        |                 200 |         360   | Christmas & New Year Peak |               1.8  |                 360   |                   80 | High Surge        |
|          18 | Standard Single    |                  80 |         144   | Christmas & New Year Peak |               1.8  |                 144   |                   80 | High Surge        |
|           4 | Standard Double    |                 130 |         195   | Spring Festival           |               1.5  |                 195   |                   50 | Moderate Increase |
|           5 | Deluxe Suite       |                 250 |         212.5 | Spring Festival           |               1.5  |                 375   |                  -15 | Moderate Increase |
|          16 | Presidential Suite |                 500 |         500   | Summer High Season        |               1.3  |                 650   |                    0 | Moderate Increase |
|           3 | Standard Single    |                  80 |          68   | Weekday Discount          |               0.85 |                  68   |                  -15 | Discount          |
|           4 | Standard Double    |                 130 |         195   | Weekday Discount          |               0.85 |                 110.5 |                   50 | Discount          |


### Q04 — Loyalty member spending ranking (window function RANK)

_6 row(s) returned. Top 6 shown:_

|   Loyalty_ID | Guest_Name       | Tier_Level   |   Available_Points |   Total_Spent |   Spending_Rank |
|-------------:|:-----------------|:-------------|-------------------:|--------------:|----------------:|
|            6 | Priya Sharma     | Bronze       |                800 |         663   |               1 |
|            4 | Rachel Cohen     | Bronze       |               1500 |         136   |               2 |
|            5 | Kenji Tanaka     | Silver       |               4200 |        2016   |               1 |
|            3 | Alexander Petrov | Silver       |               6800 |        1062.5 |               2 |
|            2 | Michael Anderson | Gold         |              12300 |         204   |               1 |
|            1 | Sophie Williams  | Platinum     |              28500 |        1775   |               1 |


### Q05 — Available rooms in date range (NOT EXISTS subquery)

_10 row(s) returned. Top 8 shown:_

|   Room_ID | Category_Name   |   Floor_Level |   Base_Nightly_Rate |   Max_Capacity |
|----------:|:----------------|--------------:|--------------------:|---------------:|
|       101 | Standard Single |             1 |                  80 |              1 |
|       102 | Standard Single |             1 |                  80 |              1 |
|       103 | Standard Double |             1 |                 130 |              2 |
|       201 | Standard Double |             2 |                 130 |              2 |
|       202 | Standard Double |             2 |                 130 |              2 |
|       203 | Family Room     |             2 |                 200 |              4 |
|       401 | Family Room     |             4 |                 200 |              4 |
|       302 | Deluxe Suite    |             3 |                 250 |              3 |


### Q06 — Department-level task efficiency

_2 row(s) returned. Top 2 shown:_

|   Dept_ID | Dept_Name    |   Staff_Count |   Total_Tasks |   Avg_Duration_Min |   Avg_Quality_Score |   Completed_Tasks |
|----------:|:-------------|--------------:|--------------:|-------------------:|--------------------:|------------------:|
|         2 | Housekeeping |             2 |            12 |               53.8 |                8.71 |                12 |
|         3 | Maintenance  |             1 |             3 |               85   |                7.25 |                 2 |


### Q07 — Monthly revenue trend with MoM change (LAG)

_5 row(s) returned. Top 5 shown:_

| Revenue_Month   |   Transaction_Count |   Booking_Count |   Total_Revenue |   Avg_Transaction |   Max_Transaction |   MoM_Change |
|:----------------|--------------------:|----------------:|----------------:|------------------:|------------------:|-------------:|
| 2025-12         |                   2 |               2 |          3366   |           1683    |            2016   |        nan   |
| 2026-01         |                   1 |               1 |           204   |            204    |             204   |      -3162   |
| 2026-02         |                   2 |               2 |          1725.5 |            862.75 |            1062.5 |       1521.5 |
| 2026-03         |                   2 |               2 |           697   |            348.5  |             425   |      -1028.5 |
| 2026-04         |                   2 |               2 |           688.5 |            344.25 |             552.5 |         -8.5 |


### Q08 — Cleaning quality ranking (window function ROW_NUMBER)

_1 row(s) returned. Top 1 shown:_

|   Staff_ID | Full_Name   | Job_Role       |   Task_Count |   Avg_Quality |   Avg_Duration |   Rooms_Serviced |   Quality_Rank |
|-----------:|:------------|:---------------|-------------:|--------------:|---------------:|-----------------:|---------------:|
|          4 | Aisha Patel | Room Attendant |            5 |           8.3 |             52 |                4 |              1 |


### Q09 — Revenue dashboard view (6-table JOIN)

_16 row(s) returned. Top 8 shown:_

|   Booking_ID | Guest_Name       | Room_Category   |   Room_ID |   Floor_Level | CheckIn_Date   | CheckOut_Date   |   Stay_Nights |   Nightly_Rate |   Base_Nightly_Rate |   Rate_Variance_Pct |   Paid_Amount | Overall_Status   |
|-------------:|:-----------------|:----------------|----------:|--------------:|:---------------|:----------------|--------------:|---------------:|--------------------:|--------------------:|--------------:|:-----------------|
|            2 | Kenji Tanaka     | Family Room     |       203 |             2 | 2025-12-28     | 2026-01-01      |             4 |          360   |                 200 |                  80 |        2016   | Checked-Out      |
|            2 | Kenji Tanaka     | Standard Single |       102 |             1 | 2025-12-28     | 2026-01-01      |             4 |          144   |                  80 |                  80 |        2016   | Checked-Out      |
|            1 | Sophie Williams  | Deluxe Suite    |       303 |             3 | 2025-12-23     | 2025-12-26      |             3 |          450   |                 250 |                  80 |        1350   | Checked-Out      |
|            5 | Alexander Petrov | Deluxe Suite    |       302 |             3 | 2026-02-03     | 2026-02-08      |             5 |          212.5 |                 250 |                 -15 |        1062.5 | Checked-Out      |
|            6 | Priya Sharma     | Standard Double |       103 |             1 | 2026-02-10     | 2026-02-13      |             3 |          110.5 |                 130 |                 -15 |         663   | Checked-Out      |
|            6 | Priya Sharma     | Standard Double |       201 |             2 | 2026-02-10     | 2026-02-13      |             3 |          110.5 |                 130 |                 -15 |         663   | Checked-Out      |
|           11 | Hans Mueller     | Standard Double |       103 |             1 | 2026-04-10     | 2026-04-15      |             5 |          110.5 |                 130 |                 -15 |         552.5 | Checked-Out      |
|            7 | Emma Johansson   | Standard Single |       102 |             1 | 2026-03-02     | 2026-03-06      |             4 |           68   |                  80 |                 -15 |         272   | Checked-Out      |


### Q10 — Cancellation rate by month with alert level

_5 row(s) returned. Top 5 shown:_

| Month   |   Total_Bookings |   Cancelled_Count |   Confirmed_Count |   Completed_Count |   Cancellation_Rate_Pct | Alert_Level          |
|:--------|-----------------:|------------------:|------------------:|------------------:|------------------------:|:---------------------|
| 2025-12 |                3 |                 0 |                 0 |                 3 |                    0    | NORMAL               |
| 2026-01 |                2 |                 1 |                 0 |                 1 |                   50    | CRITICAL — Above 30% |
| 2026-02 |                3 |                 0 |                 0 |                 3 |                    0    | NORMAL               |
| 2026-03 |                3 |                 1 |                 0 |                 2 |                   33.33 | CRITICAL — Above 30% |
| 2026-05 |                4 |                 0 |                 2 |                 0 |                    0    | NORMAL               |


### Q11 — VIP customer identification via CTE

_1 row(s) returned. Top 1 shown:_

|   Guest_ID | Guest_Name      | Email                       | Tier_Level   |   Booking_Count |   Total_Spent |   Available_Points |   VIP_Score | VIP_Category   |
|-----------:|:----------------|:----------------------------|:-------------|----------------:|--------------:|-------------------:|------------:|:---------------|
|          2 | Sophie Williams | sophie.williams@outlook.com | Platinum     |               2 |          1775 |              28500 |        43.1 | Silver VIP     |


### Q12 — Overlap booking detection (self-join)
**0 rows** returned. This is the expected and desired result: no overlapping bookings exist in the dataset, confirming that the application-layer concurrency guard is correct.

"""
Compute actual query results from the sample data (no MySQL required),
so the LaTeX report can show real numbers instead of placeholders.
Mirrors the logic of tests/test_queries.sql against the same INSERT rows.
"""
import pandas as pd

# ---------- Load mirror of sample_data.sql ----------
guest = pd.DataFrame([
    [1,"Michael","Anderson"], [2,"Sophie","Williams"],   [3,"Kenji","Tanaka"],
    [4,"Isabella","Rossi"],   [5,"Alexander","Petrov"],  [6,"Emma","Johansson"],
    [7,"Carlos","Mendez"],    [8,"Rachel","Cohen"],      [9,"Hans","Mueller"],
    [10,"Priya","Sharma"],
], columns=["gid","fn","ln"])

loyalty = pd.DataFrame([
    [1,2,"Platinum",28500],[2,1,"Gold",12300],[3,5,"Silver",6800],
    [4,8,"Bronze",1500],[5,3,"Silver",4200],[6,10,"Bronze",800],
], columns=["lid","gid","tier","points"])

room_type = pd.DataFrame([
    [1,"Standard Single",80,1],[2,"Standard Double",130,2],
    [3,"Deluxe Suite",250,3],[4,"Family Room",200,4],
    [5,"Presidential Suite",500,4],
], columns=["tid","name","base","cap"])

room = pd.DataFrame([
    [101,1,1,"Available"],[102,1,1,"Occupied"],[103,2,1,"Available"],
    [201,2,2,"Occupied"],[202,2,2,"Reserved"],[203,4,2,"Available"],
    [301,1,3,"Maintenance"],[302,3,3,"Available"],[303,3,3,"Occupied"],
    [401,4,4,"Available"],[402,3,4,"Reserved"],[403,5,4,"Available"],
], columns=["rid","tid","floor","status"])

booking = pd.DataFrame([
    [1,2,"Checked-Out"],[2,3,"Checked-Out"],[3,1,"Checked-Out"],
    [4,4,"Cancelled"], [5,5,"Checked-Out"],[6,10,"Checked-Out"],
    [7,6,"Checked-Out"],[8,2,"Checked-Out"],[9,7,"Cancelled"],
    [10,8,"Checked-Out"],[11,9,"Checked-Out"],[12,1,"Checked-In"],
    [13,4,"Confirmed"],[14,7,"Confirmed"],[15,5,"Checked-In"],
], columns=["bid","gid","status"])

brd = pd.DataFrame([
    [1,1,303,"2025-12-23","2025-12-26",450.00],
    [2,2,203,"2025-12-28","2026-01-01",360.00],
    [3,3,101,"2026-01-12","2026-01-15", 68.00],
    [4,4,103,"2026-01-29","2026-02-02",195.00],
    [5,5,302,"2026-02-03","2026-02-08",212.50],
    [6,6,103,"2026-02-10","2026-02-13",110.50],
    [7,6,201,"2026-02-10","2026-02-13",110.50],
    [8,7,102,"2026-03-02","2026-03-06", 68.00],
    [9,8,303,"2026-03-10","2026-03-12",212.50],
    [10,9,403,"2026-03-20","2026-03-24",425.00],
    [11,10,101,"2026-04-06","2026-04-08", 68.00],
    [12,11,103,"2026-04-10","2026-04-15",110.50],
    [13,12,201,"2026-05-12","2026-05-19",110.50],
    [14,12,303,"2026-05-12","2026-05-19",212.50],
    [15,13,202,"2026-05-25","2026-05-28",110.50],
    [16,14,403,"2026-06-01","2026-06-05",500.00],
    [17,15,402,"2026-05-14","2026-05-19",212.50],
    [18,2,102,"2025-12-28","2026-01-01",144.00],
], columns=["did","bid","rid","ci","co","rate"])
brd["ci"] = pd.to_datetime(brd["ci"]); brd["co"] = pd.to_datetime(brd["co"])
brd["nights"] = (brd["co"] - brd["ci"]).dt.days

payment = pd.DataFrame([
    [1,1,1350.00,"Completed"],[2,2,2016.00,"Completed"],
    [3,3, 204.00,"Completed"],[4,4, 195.00,"Refunded"],
    [5,5,1062.50,"Completed"],[6,6, 663.00,"Completed"],
    [7,7, 272.00,"Completed"],[8,8, 425.00,"Completed"],
    [9,9, 425.00,"Refunded"], [10,10,136.00,"Completed"],
    [11,11,552.50,"Completed"],[12,12,323.00,"Pending"],
], columns=["pid","bid","amount","status"])

task = pd.DataFrame([
    [1,3,303,"Cleaning",75,9.5],[2,3,203,"Inspection",30,8.0],
    [3,4,203,"Cleaning",90,7.5],[4,5,301,"Maintenance",None,None],
    [5,4,101,"Cleaning",45,8.5],[6,3,302,"Setup",40,9.0],
    [7,5,201,"Maintenance",150,7.0],[8,4,102,"Cleaning",40,9.0],
    [9,3,303,"Cleaning",90,9.8],[10,3,403,"Inspection",45,8.5],
    [11,4,101,"Cleaning",35,8.0],[12,4,103,"Cleaning",50,8.5],
    [13,3,201,"Setup",50,9.0],[14,5,401,"Maintenance",20,7.5],
    [15,3,402,"Setup",55,9.2],
], columns=["lid","staff","rid","type","dur","qs"])

# ---------- Q1: Revenue per guest ----------
q1 = (guest.merge(booking, on="gid", how="left")
            .merge(payment.query("status=='Completed'"), on="bid", how="left")
            .groupby(["gid","fn","ln"])
            .agg(Bookings=("bid","nunique"), Spent=("amount","sum"))
            .reset_index()
            .sort_values("Spent", ascending=False)).fillna(0).head(5)
print("Q1 Top-5 by spent:\n", q1.to_string(index=False), "\n")

# ---------- Q2: Occupancy per room type ----------
valid_brd = brd.merge(booking.query("status != 'Cancelled'"), on="bid")
q2 = (room.merge(room_type, on="tid")
           .merge(valid_brd.groupby("rid")["nights"].sum().rename("nights"),
                  on="rid", how="left")
           .groupby(["tid","name"])
           .agg(Rooms=("rid","nunique"), TotalNights=("nights","sum"))
           .reset_index())
q2["OccRate%"] = (q2["TotalNights"] / (q2["Rooms"] * 365) * 100).round(2)
q2 = q2.fillna(0).sort_values("OccRate%", ascending=False)
print("Q2 Occupancy by room type:\n", q2.to_string(index=False), "\n")

# ---------- Q8: Cleaning quality ranking (HAVING >=5 cleaning tasks) ----------
cln = task.query("type=='Cleaning' and qs == qs")
q8 = (cln.groupby("staff").agg(Tasks=("lid","count"),
                                AvgQS=("qs","mean"),
                                AvgDur=("dur","mean")).reset_index())
q8_ge5 = q8.query("Tasks >= 5").sort_values("AvgQS", ascending=False)
print("Q8 Cleaning ranking (HAVING>=5):\n", q8_ge5.to_string(index=False))
print("Q8 (no HAVING filter for context):\n", q8.to_string(index=False), "\n")

# ---------- Q11: VIP scoring ----------
metrics = (guest.merge(booking, on="gid", how="left")
                .merge(payment.query("status=='Completed'"), on="bid", how="left")
                .groupby(["gid","fn","ln"])
                .agg(Bookings=("bid","nunique"), Spent=("amount","sum"))
                .reset_index().fillna(0))
metrics = metrics.merge(loyalty[["gid","tier","points"]], on="gid", how="left")
metrics["tier"] = metrics["tier"].fillna("None")
def vip_score(row):
    s = min(row["Spent"]/10000, 1)*40
    s += min(row["Bookings"]/10, 1)*30
    tier_pt = {"Platinum":30,"Gold":22,"Silver":14,"Bronze":6}.get(row["tier"],0)
    return round(s + tier_pt, 1)
metrics["VIPScore"] = metrics.apply(vip_score, axis=1)
metrics = metrics.sort_values("VIPScore", ascending=False)
print("Q11 VIP scoring (top 5):\n",
      metrics[["gid","fn","ln","tier","Bookings","Spent","VIPScore"]].head().to_string(index=False))

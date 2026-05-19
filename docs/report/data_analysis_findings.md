# Data Analysis Findings — Hotel Booking & Management System

Five managerial insights derived from the populated sample dataset (10 guests, 15 bookings, 18 room-nights, 12 payments, 15 task logs). All figures are computed directly from `src/schema/sample_data.sql`.

## F1 — Loyalty Tier Predicts Spend, But Points Balance Does Not

Booking-level average revenue rises sharply with tier: **Bronze members average only \$399.50 per booking, while Silver members average \$1,380.33 — a 3.5× gap.** Platinum and Gold sit between (\$887.50 and \$1,232.50). However, the Pearson correlation between *available loyalty points* and *total spend* among the six members is only **r = 0.455** — weak to moderate. Points reflect *historical accumulation*, while spend reflects *current booking value*. The implication is that tier upgrades should be triggered by recent rolling revenue, not lifetime point inertia, otherwise Bronze big-spenders (e.g., Guest 10 at \$663 on 800 points) remain under-recognized. *Supporting query:* **Q04, Q11**. *Visualisation:* **fig4 (correlation heat-map)**.

## F2 — A 13.3% Cancellation Rate Concentrates in High-Value Inventory

Two of fifteen bookings (**13.3%**) were cancelled, but they represented disproportionately premium inventory: B4 (Standard Double, Spring Festival, 4 nights at \$195) and B9 (Presidential Suite, 4 nights at \$425). Lost potential revenue totals **\$2,480** — equivalent to **16.7%** of total realised + pending revenue (\$12,336). The cancellations cluster in Jan–Mar event-rate windows, suggesting that surge pricing itself elevates cancellation probability. Q10 flags January 2026 as **CRITICAL (50% monthly cancellation rate)**. Managerially this argues for non-refundable deposits on top-tier rooms during peak rules. *Supporting query:* **Q10, Q03**. *Visualisation:* **fig3 (Sankey: status flow), fig6 (lollipop: pricing impact)**.

## F3 — Weekday Discount Erodes More Revenue Than Christmas Adds

Aggregating actual vs. base rate across all non-cancelled room-nights yields only a **+2.20% net premium** over base. The breakdown is striking: Christmas surcharge added **+\$1,496** across 3 details, while the Weekday Discount subtracted **−\$1,230** across 12 details — nearly offsetting the entire seasonal upside. The 1.8× Christmas multiplier is doing the heavy lifting, but its scope is too narrow to compensate the chronic 0.85× weekday haircut. *Recommendation:* tighten weekday discount eligibility or shorten its 5-month window. *Supporting query:* **Q03, Q07**. *Visualisation:* **fig6 (lollipop chart)**.

## F4 — Housekeeping Outperforms Maintenance by 1.46 Quality Points

Housekeeping logs 12 completed tasks averaging **8.71/10 quality at 53.8 min/task**, while Maintenance logs only 2 completed tasks at **7.25/10 quality and 85.0 min/task** (a third maintenance task is unresolved — the AC repair in room 301 since Jan 10). The 1.46-point gap is not noise: maintenance work is inherently longer-cycle and harder to standardise, yet the unfinished open ticket signals a staffing bottleneck (1 technician for the entire hotel). Hiring a second technician would simultaneously raise quality scores and reduce room downtime. *Supporting query:* **Q06, Q08**. *Visualisation:* **fig5 (raincloud: quality by department)**.

## F5 — 12.37% of Payment Volume is at Risk; Credit Card Dominates Premium Stays

Of the **\$7,624** total payment volume, only **87.63%** is Completed; **8.13%** is Refunded and **4.24%** Pending — i.e., **\$943 (12.37%) at risk** against finalised revenue. Credit Card averages **\$1,263.67 per completed transaction**, 9.3× the Cash average of \$136. Premium bookings concentrate in card payments while cash settles only the smallest stays. This suggests card-acceptance reliability is mission-critical; a single failed terminal in peak season would jeopardise the high-value end of the funnel. *Supporting query:* **Q07, Q09**. *Visualisation:* **fig2 (violin: revenue distribution)**.

---

## Summary Map: Findings → Queries → Figures

| Finding | Headline Number | SQL Query | Figure |
|---|---|---|---|
| F1 Loyalty tier vs. points | Silver ARPU \$1,380 vs Bronze \$400 (3.5×); r=0.455 | Q04, Q11 | fig4 |
| F2 Cancellation concentration | 13.3% rate, \$2,480 lost, Jan = CRITICAL 50% | Q10, Q03 | fig3, fig6 |
| F3 Pricing net premium | +2.20% net; +\$1,496 Christmas vs −\$1,230 weekday | Q03, Q07 | fig6 |
| F4 Department quality gap | Housekeeping 8.71 vs Maintenance 7.25 (Δ1.46) | Q06, Q08 | fig5 |
| F5 Revenue at risk | 12.37% Pending+Refunded; CC ARPU 9.3× Cash | Q07, Q09 | fig2 |

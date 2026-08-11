# Set Piece Statistics

## Overview

This section analyzes the effectiveness of attacking set pieces throughout the season. It focuses on corner kicks and penalty kicks, measuring both the frequency of these situations and their contribution to goal scoring.

---

## Business Question

**How effective were attacking set pieces during the season in terms of corner kicks and penalty kicks?**

---

## Data Sources

The analysis was performed using the following database tables:

- `Events`
- `PassEvents`
- `PassTypes`
- `ShotEvents`
- `ShotTypes`
- `ShotOutcomes`
- `PlayPatterns`

---

## Metrics

The following key performance indicators (KPIs) are reported:

- Total Corner Kicks
- Goals from Corners
- Corner Conversion Rate
- Total Penalties Awarded
- Penalty Goals
- Penalty Conversion Rate

---

## Results

| Metric | Value |
|---------------------------------|------:|
| Total Corner Kicks | 3,841 |
| Goals from Corners | 136 |
| Corner Conversion Rate | 3.54% |
| Total Penalties Awarded | 97 |
| Penalty Goals | 69 |
| Penalty Conversion Rate | 71.13% |

---

## Methodology

The set-piece statistics were calculated using the StatsBomb event model.

- **Corner Kicks** were identified from `PassEvents` where the corresponding `PassType` was classified as **Corner**.
- **Goals from Corners** were identified as shot events with a **Goal** outcome that originated from the **From Corner** play pattern.
- **Corner Conversion Rate** was calculated as:

```
Goals from Corners
------------------ × 100
Total Corner Kicks
```

- **Penalties Awarded** were identified from `ShotEvents` where the `ShotType` was **Penalty**.
- **Penalty Goals** represent penalties that resulted in a goal.
- **Penalty Conversion Rate** was calculated as:

```
Penalty Goals
------------- × 100
Total Penalties Awarded
```

---

## Insight

A total of **3,841 corner kicks** were taken during the season, producing **136 goals**, resulting in a **corner conversion rate of 3.54%**. Although corner kicks occurred frequently, only a small proportion directly resulted in goals, reflecting the inherent difficulty of converting these opportunities.

In comparison, **97 penalties** were awarded, of which **69** were successfully converted, yielding a **penalty conversion rate of 71.13%**. This substantially higher success rate demonstrates that penalty kicks remain one of the most effective goal-scoring opportunities in football.

---

## Notes

- Corner kicks are identified using the `PassType` lookup table rather than play patterns, as a corner is recorded as a specialized pass event.
- Goals from corners are determined using the `PlayPattern` associated with the corresponding shot event.
- Penalty statistics are derived directly from the `ShotType` associated with each shot event.
- Conversion rates are rounded to two decimal places for reporting consistency.
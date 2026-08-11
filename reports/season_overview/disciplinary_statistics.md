# Disciplinary Statistics

## Overview

This section examines the disciplinary characteristics of the season by analyzing fouls committed, bookings, dismissals, and the frequency with which disciplinary actions were issued. These metrics provide insight into the physical intensity of the competition and the overall officiating profile of the season.

---

## Business Question

**What were the overall disciplinary characteristics of the season in terms of fouls committed, bookings, dismissals, and referee decisions?**

---

## Data Sources

The analysis was performed using the following database tables:

- `FoulCommittedEvents`
- `BadBehaviourEvents`
- `Cards`

---

## Metrics

The following key performance indicators (KPIs) are reported:

- Total Fouls Committed
- Total Yellow Cards
- Total Second Yellow Cards
- Total Straight Red Cards
- Yellow Cards per Foul
- Straight Red Cards per Foul

---

## Results

| Metric | Value |
|---------------------------------|------:|
| Total Fouls Committed | 4,088 |
| Total Yellow Cards | 2,084 |
| Total Second Yellow Cards | 73 |
| Total Straight Red Cards | 36 |
| Yellow Cards per Foul | 41.46% |
| Straight Red Cards per Foul | 0.66% |

---

## Methodology

The disciplinary statistics were derived using the StatsBomb event model.

- **Total Fouls Committed** were obtained from the `FoulCommittedEvents` table.
- **Yellow Cards**, **Second Yellow Cards**, and **Straight Red Cards** were aggregated from both the `FoulCommittedEvents` and `BadBehaviourEvents` tables, as disciplinary actions are recorded in both event types.
- **Yellow Cards per Foul** represents the percentage of fouls that resulted in either a yellow card or a second-yellow caution.
- **Straight Red Cards per Foul** represents the percentage of fouls that resulted in an immediate dismissal.

---

## Insight

A total of **4,088 fouls** were committed during the season, resulting in **2,084 yellow cards**, **73 second-yellow dismissals**, and **36 straight red cards**.

Approximately **41.46%** of fouls resulted in a booking, while only **0.66%** led directly to a straight red card. These figures indicate that referees most frequently managed player discipline through cautions rather than immediate dismissals, with straight red cards remaining relatively uncommon throughout the competition.

---

## Notes

- Card statistics are aggregated from both `FoulCommittedEvents` and `BadBehaviourEvents` to ensure complete disciplinary coverage.
- A second-yellow dismissal is reported separately from a straight red card because they represent distinct disciplinary events under the Laws of the Game.
- The "Yellow Cards per Foul" metric includes both standard yellow cards and second-yellow cautions, as both represent cautions issued by the referee.
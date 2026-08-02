# Match Intensity

## Overview

This section evaluates the overall intensity of the season by measuring the average number of fouls committed, yellow cards issued, and corner kicks awarded per match. Together, these metrics provide an indication of the physical nature of the competition, the level of disciplinary intervention by referees, and the frequency of attacking opportunities.

---

## Business Question

**How physically demanding and active was the season based on the average number of fouls committed, yellow cards issued, and corner kicks awarded per match?**

---

## Data Sources

The analysis was performed using the following database tables:

- `Matches`
- `FoulCommittedEvents`
- `BadBehaviourEvents`
- `Cards`
- `Events`
- `PassEvents`
- `PassTypes`

---

## Metrics

The following key performance indicators (KPIs) are reported:

- Fouls Committed per Match
- Yellow Cards per Match
- Corner Kicks per Match

---

## KPI Definitions

### Fouls Committed per Match

**Formula**

```
Total Fouls Committed
---------------------
Total Matches
```

Measures the average number of fouls committed during a match.

---

### Yellow Cards per Match

**Formula**

```
Total Yellow Cards
------------------
Total Matches
```

Measures the average number of yellow cards issued per match. Yellow cards are aggregated from both `FoulCommittedEvents` and `BadBehaviourEvents` to ensure complete disciplinary coverage.

---

### Corner Kicks per Match

**Formula**

```
Total Corner Kicks
------------------
Total Matches
```

Measures the average number of corner kicks awarded in a match.

---

## Results

| Metric | Value |
|--------------------------------|------:|
| Fouls Committed per Match | 10.76 |
| Yellow Cards per Match | 5.48 |
| Corner Kicks per Match | 10.11 |

---

## Methodology

- Total fouls were obtained from the `FoulCommittedEvents` table.
- Yellow cards were aggregated from both `FoulCommittedEvents` and `BadBehaviourEvents`, as disciplinary actions are recorded in multiple event categories within the StatsBomb event model.
- Corner kicks were identified using `PassEvents` where the associated `PassType` was classified as **Corner**.
- Match averages were calculated by dividing each event count by the total number of matches played during the season.
- All values are rounded to two decimal places.

---

## Insight

The season averaged **10.76 fouls**, **5.48 yellow cards**, and **10.11 corner kicks** per match.

These figures indicate a physically competitive league in which referees frequently intervened with disciplinary action while teams consistently generated attacking opportunities through corner kicks. The combination of a high foul frequency and regular attacking set pieces suggests an active and competitive style of play throughout the season.

---

## Notes

- All averages are calculated using the total number of matches played during the season.
- Yellow card statistics include cautions recorded during both foul-related incidents and bad behaviour events.
- Match intensity metrics are intended to provide a high-level overview of the physical and attacking characteristics of the competition.
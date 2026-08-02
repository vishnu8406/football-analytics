# Goal Statistics

## Overview

This section presents a high-level summary of the goal-scoring characteristics of the season. It analyzes goal distribution, scoring patterns, and goal origins to provide an overall understanding of offensive performance throughout the competition.

---

## Business Question

**What are the overall goal-scoring characteristics of the season?**

---

## Data Sources

The analysis was performed using the following database tables:

- `Matches`
- `Events`
- `ShotEvents`
- `ShotOutcomes`
- `EventTypes`
- `PlayPatterns`

---

## Metrics

The following key performance indicators (KPIs) are reported:

- Home Goals
- Away Goals
- Total Goals
- Own Goals
- Open-Play Goals
- Dead-Ball Goals
- Average Goals per Match

---

## Results

| Metric | Value |
|---------------------------|------:|
| Home Goals | 615 |
| Away Goals | 428 |
| Total Goals | 1043 |
| Own Goals | 29 |
| Open-Play Goals | 412 |
| Dead-Ball Goals* | 602 |
| Average Goals per Match | 2.74 |

---

## Methodology

Goals were categorized using the StatsBomb event model.

- **Open-Play Goals** include goals scored during:
  - Regular Play
  - Counter Attacks

- **Dead-Ball Goals** include goals originating from:
  - Free Kicks
  - Corners
  - Throw Ins
  - Goal Kicks
  - Goalkeeper Restarts
  - Kick Offs
  - Other restart situations

- **Own Goals** are stored separately as dedicated event types and are not associated with shot events.

---

## Insight

A total of **1,043 goals** were scored during the season, averaging **2.74 goals per match**, indicating a relatively high-scoring competition. Home teams contributed **615 goals (59.0%)**, while away teams scored **428 goals (41.0%)**, suggesting a noticeable home-scoring advantage throughout the season.

Among all goals, **412** originated from open play, whereas **602** resulted from dead-ball or restart situations. Additionally, the season recorded **29 own goals**, representing approximately **2.8%** of all goals scored.

---

## Validation

The total number of goals recorded in the `Matches` table (**1,043**) is consistent with the combined total of:

- Shot-based Goals: **1,014**
- Own Goals: **29**

**Validation Check**

```
Shot-Based Goals + Own Goals = Total Goals

1,014 + 29 = 1,043 ✅
```

This validation confirms that the event-level data is internally consistent with the official match score records.

---

## Notes

- Goal statistics are aggregated across the selected season.
- Open-play and dead-ball goals are derived exclusively from shot events.
- Own goals are represented separately in the StatsBomb event model and therefore are excluded from both the open-play and dead-ball goal categories.
- Goal classifications follow the methodology adopted for this project and are documented to ensure transparency and reproducibility.
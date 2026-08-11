# Defensive Performance

## Overview

This section evaluates the defensive strength of every team throughout the season by measuring goals conceded, defensive consistency, clean sheets, and goalkeeper shot-stopping performance.

Unlike the attacking analysis, this module focuses on preventing goals rather than scoring them.

---

## Business Question

**Which teams defended most effectively throughout the season?**

---

## Data Sources

The analysis uses the following database tables:

- Teams
- Matches
- Events
- GoalKeeperEvents
- GoalKeeperTypes

---

## Metrics

The following defensive KPIs are reported:

- Goals Conceded
- Goals Conceded per Match
- Clean Sheets
- Goalkeeper Saves

---

## KPI Definitions

### Goals Conceded

The total number of goals conceded by each team throughout the season.

---

### Goals Conceded per Match

**Formula**

```
Goals Conceded
---------------
Matches Played
```

Measures the average number of goals conceded in each match.

---

### Clean Sheets

The total number of matches in which the team conceded zero goals.

---

### Goalkeeper Saves

The total number of goalkeeper saves recorded throughout the season, including penalty saves where applicable.

---

## Results

The query returns one row per team with the following defensive statistics.

| Team | Goals Conceded | GA/Match | Clean Sheets | Goalkeeper Saves |
|------|---------------:|----------:|-------------:|-----------------:|

---

## Methodology

- Goals conceded were derived from official match results.
- Clean sheets were identified by counting matches in which the opposing team scored zero goals.
- Goalkeeper saves were calculated using goalkeeper event records, including successful penalty saves.
- Teams were ranked by defensive effectiveness, beginning with goals conceded.

---

## Key Insights

- **Atlético Madrid** recorded the league's strongest defensive performance, conceding only **17 goals** while keeping **24 clean sheets**, highlighting exceptional defensive consistency.
- **Barcelona**, **Villarreal**, and **Real Madrid** also demonstrated strong defensive performances by maintaining fewer than one goal conceded per match.
- Teams with the highest goalkeeper save totals generally faced significantly more defensive pressure, indicating that a high number of saves does not necessarily imply a stronger defense.
- Clean sheets provide an additional measure of defensive reliability by identifying teams capable of consistently preventing opponents from scoring.

---

## Notes

- Goalkeeper saves include successful penalty saves.
- Goals conceded are derived from official match scores.
- This analysis focuses on overall team defensive performance rather than individual goalkeeper evaluation.
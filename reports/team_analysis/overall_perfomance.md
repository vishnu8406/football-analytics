# Overall Performance

## Overview

This section evaluates the overall performance of every team during the season by constructing the league table using match outcomes and goal statistics. It summarizes each team's consistency, attacking and defensive output, and overall success based on the standard football points system.

---

## Business Question

**Which teams performed best throughout the season based on league results, goal statistics, and points accumulated?**

---

## Data Sources

The analysis was performed using the following database tables:

- `Teams`
- `Matches`

---

## Metrics

The following key performance indicators (KPIs) are reported:

- Matches Played
- Wins
- Draws
- Losses
- Goals Scored (GF)
- Goals Conceded (GA)
- Goal Difference (GD)
- Total Points
- Win Percentage
- Points per Match (PPM)

---

## KPI Definitions

### Matches Played

The total number of league matches played by each team.

---

### Wins

The total number of matches won by each team, including both home and away victories.

---

### Draws

The total number of matches that finished level.

---

### Losses

The total number of matches lost, including both home and away defeats.

---

### Goals Scored (GF)

The total number of goals scored by the team throughout the season.

---

### Goals Conceded (GA)

The total number of goals conceded by the team throughout the season.

---

### Goal Difference (GD)

**Formula**

```
Goals Scored − Goals Conceded
```

Measures a team's overall scoring dominance across the season.

---

### Points

**Formula**

```
(3 × Wins) + Draws
```

Calculated according to the standard football league scoring system.

---

### Win Percentage

**Formula**

```
Wins
----- × 100
Matches Played
```

Measures the proportion of matches won during the season.

---

### Points per Match (PPM)

**Formula**

```
Points
------
Matches Played
```

Measures the average number of points earned per match, enabling fair comparisons between teams even when the number of matches differs.

---

## Results

The query returns one row for every team, producing a complete league table ranked by:

1. Total Points
2. Goal Difference
3. Goals Scored

The output includes the following columns:

| Team | MP | W | D | L | GF | GA | GD | Pts | Win % | PPM |
|------|---:|---:|---:|---:|---:|---:|---:|---:|------:|----:|

---

## Methodology

- Every match was associated with both participating teams by matching each team's identifier against the home and away team fields.
- Home and away statistics were combined using conditional aggregation (`CASE WHEN`) to calculate season totals.
- Goals scored and conceded were derived separately depending on whether the team played at home or away.
- League points were calculated using the standard football scoring system of three points for a win and one point for a draw.
- Teams were ranked by total points, followed by goal difference and goals scored.

---

## Insight

The league table provides a comprehensive view of team performance throughout the season by combining match results with offensive and defensive statistics.

The highest-ranked teams consistently combined a high win percentage with strong goal-scoring ability and positive goal differences, while lower-ranked teams generally accumulated fewer points due to a combination of fewer victories, lower scoring output, and higher numbers of goals conceded.

Points per Match (PPM) complements the traditional league table by normalizing performance relative to matches played, making it particularly useful when comparing teams across incomplete seasons or different competitions.

---

## Notes

- League rankings follow the standard football hierarchy:
  1. Points
  2. Goal Difference
  3. Goals Scored
- Win Percentage and Points per Match are derived metrics intended to provide additional context beyond the traditional league table.
- This analysis serves as the foundation for subsequent Team Analysis modules, including Attacking Performance, Defensive Performance, Possession & Passing, and Discipline.
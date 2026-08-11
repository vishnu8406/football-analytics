# Attacking Performance

## Overview

This section evaluates the attacking performance of every team during the season by analyzing goal scoring, shot creation, shooting accuracy, and finishing efficiency. Rather than relying solely on total goals, it measures how effectively teams converted scoring opportunities into goals and identifies the primary sources of those goals.

---

## Business Question

**Which teams demonstrated the strongest attacking performance throughout the season based on shooting efficiency and goal production?**

---

## Data Sources

The analysis was performed using the following database tables:

- Teams
- Matches
- Events
- ShotEvents
- ShotOutcomes
- PlayPatterns
- ShotTypes

---

## Metrics

The following key performance indicators (KPIs) are reported:

- Goals Scored
- Goals per Match
- Total Shots
- Shots on Target
- Shot Accuracy
- Shot Conversion Rate
- Open Play Goals
- Set Piece Goals
- Penalty Goals

---

## KPI Definitions

### Goals Scored

The total number of successful shot events that resulted in a goal.

> **Note:** Goals awarded through opponent own goals are excluded because they are recorded as separate event types rather than successful shot events.

---

### Goals per Match

**Formula**

```
Goals Scored
-------------
Matches Played
```

Measures the average attacking output per match.

---

### Total Shots

The total number of shot attempts taken during the season.

---

### Shots on Target

The total number of shots that required a save or resulted in a goal, based on the StatsBomb shot outcome definitions used in this project.

---

### Shot Accuracy

**Formula**

```
Shots on Target
----------------
Total Shots
```

Measures how frequently a team's shots were directed towards the goal.

---

### Shot Conversion Rate

**Formula**

```
Goals Scored
-------------
Total Shots
```

Measures the percentage of total shots that resulted in goals.

---

### Open Play Goals

Goals scored during regular attacking play, including counterattacks.

---

### Set Piece Goals

Goals scored from dead-ball situations, including corners, free kicks, throw-ins, goal kicks, kick-offs, and other non-open-play situations.

---

### Penalty Goals

Goals scored directly from penalty kicks.

---

## Results

The query returns one row for every team with the following attacking statistics.

| Team | Goals | G/Match | Shots | On Target | Accuracy | Conversion | Open Play | Set Piece | Penalties |
|------|------:|---------:|------:|----------:|----------:|-----------:|----------:|----------:|----------:|

---

## Methodology

- Shot events were linked to the corresponding team through the Events table.
- Goals were identified using successful Shot Outcome events.
- Goals per Match was calculated by dividing total goals by the number of distinct matches played.
- Shots on Target were classified according to the StatsBomb shot outcome definitions adopted for this project.
- Shot Accuracy and Shot Conversion Rate were calculated using total shots as the denominator.
- Open-play and set-piece goals were classified using the Play Pattern associated with each shot event.
- Penalty goals were identified using the Shot Type associated with each shot.

---

## Key Insights

- **Barcelona** finished as the league's most productive attack, scoring **109** non-own goals at an average of **2.87 goals per match** while maintaining a strong **18% shot conversion rate**.
- **Real Madrid** generated the highest shot volume (**717 shots**) and the highest number of shots on target (**287**), highlighting an aggressive attacking approach throughout the season.
- Most teams scored the vast majority of their goals from **open play**, indicating that sustained attacking play contributed more to goal production than dead-ball situations.
- Penalty goals represented a relatively small proportion of total goals for every team, reinforcing that open-play finishing remained the primary source of attacking success.
- Shot accuracy varied considerably across teams, demonstrating that creating a high number of shooting opportunities alone did not necessarily translate into efficient finishing.

---

## Notes

- Goals reported in this analysis exclude opponent own goals because StatsBomb records own goals as separate event types rather than successful shot events.
- Consequently, the total goals reported here may differ slightly from the official Goals For (GF) values presented in the Overall Performance analysis.
- This module focuses exclusively on attacking efficiency and chance conversion rather than overall league performance.
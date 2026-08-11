# Set Piece Effectiveness

## Overview

Set pieces provide valuable scoring opportunities and often determine the outcome of closely contested football matches. Teams that consistently convert corners, penalties, and direct free kicks into goals gain a significant competitive advantage over the course of a season.

This analysis evaluates each team's effectiveness from attacking set-piece situations by measuring both the number of opportunities created and the efficiency with which they were converted into goals.

---

## Business Question

**Which teams were most effective at converting attacking set-piece opportunities into goals throughout the season?**

---

## Data Sources

The analysis uses:

- Teams
- Events
- PassEvents
- PassTypes
- ShotEvents
- ShotTypes
- ShotOutcomes
- PlayPatterns

---

## Metrics

- Total Corners
- Corner Goals
- Corner Conversion Percentage
- Total Penalties
- Penalty Goals
- Penalty Conversion Percentage
- Direct Free Kick Goals

---

# KPI Definitions

## Total Corners

The total number of corner kicks taken throughout the season.

---

## Corner Goals

Goals scored from possessions beginning with a corner kick.

---

## Corner Conversion Percentage

**Formula**

```
Corner Goals
--------------
Total Corners
×100
```

Measures the efficiency of converting corner kicks into goals.

---

## Total Penalties

The total number of penalty kicks taken.

---

## Penalty Goals

Successful penalty kicks converted into goals.

---

## Penalty Conversion Percentage

**Formula**

```
Penalty Goals
---------------
Total Penalties
×100
```

Measures the success rate of penalty takers.

---

## Direct Free Kick Goals

Goals scored directly from free-kick attempts.

---

# Results

The query returns one row for every team containing attacking set-piece statistics.

| Team | Corners | Corner Goals | Corner Conversion % | Penalties | Penalty Goals | Penalty Conversion % | Free Kick Goals |
|------|---------:|-------------:|--------------------:|----------:|--------------:|---------------------:|-----------------:|

---

# Methodology

- Corner kicks were identified using the `PassTypes` table.
- Corner goals were identified using the `PlayPatterns` table (`From Corner`) together with successful shot outcomes.
- Penalties were identified using the `ShotTypes` table.
- Penalty goals were determined using successful penalty shot outcomes.
- Direct free-kick goals were identified using free-kick shot types with a goal outcome.

---

# Key Insights

### Real Madrid were the league's most dangerous team from corners

Real Madrid converted **14 goals from 257 corners**, achieving a **5.45% corner conversion rate**, the highest number of corner goals in the league.

---

### Barcelona combined quality with efficiency

Barcelona scored **11 corner goals** while converting **57.89%** of their penalties and leading the league with **5 direct free-kick goals**. Their ability to score from multiple types of set pieces highlights their diverse attacking threat.

---

### Athletic Club demonstrated excellent corner efficiency

Athletic Club scored **11 goals from 208 corners**, producing a **5.29% conversion rate**, making them one of the league's strongest teams from corner situations despite taking fewer corners than Real Madrid.

---

### Sevilla generated numerous corner opportunities but converted few

Sevilla took **252 corners**, the second-highest total in the league, yet scored only **4 corner goals**, resulting in a league-low **1.59% conversion rate** among teams with high corner volumes. This suggests that while Sevilla frequently created set-piece opportunities, they struggled to capitalize on them.

---

### Penalty conversion remained consistently high across the league

Most teams converted between **70% and 100%** of their penalties, demonstrating the generally high probability of scoring from the penalty spot.

Several teams—including Villarreal, Granada, Levante UD, Real Sociedad, RC Deportivo La Coruña, and Sporting Gijón—converted every penalty they took, although these perfect records were based on relatively small sample sizes.

---

### Direct free-kick goals were uncommon

Only a handful of teams scored more than two direct free-kick goals during the season, confirming that direct free kicks remain one of the most difficult methods of scoring in football.

---

# Tactical Interpretation

The analysis demonstrates that set-piece success depends on both opportunity and efficiency.

Some teams, such as Real Madrid and Barcelona, combined a high volume of attacking set pieces with strong conversion rates, maximizing their scoring potential.

Others, such as Sevilla, generated many opportunities but failed to convert them consistently, highlighting potential weaknesses in delivery, movement, or finishing during set-piece situations.

Evaluating both volume and efficiency provides a more complete understanding of a team's attacking effectiveness than considering either metric alone.

---

# Notes

- Corner kicks are identified using recorded corner pass events.
- Corner goals are defined as goals scored from possessions beginning with a corner kick.
- Penalty statistics include all recorded penalty shots.
- Direct free-kick goals include only goals scored directly from free-kick shot attempts.
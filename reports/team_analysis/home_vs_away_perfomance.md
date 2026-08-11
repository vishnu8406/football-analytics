# Home vs Away Performance

## Overview

Home advantage is one of the most influential factors in football. Teams often perform differently depending on whether they play in front of their home supporters or away from home. This analysis compares each team's performance across both venues to evaluate consistency, home advantage, and away resilience.

---

## Business Question

**How did each team's performance differ between home and away matches throughout the season?**

---

## Data Sources

The analysis uses the following database tables:

- Teams
- Matches

---

## Metrics

The following Key Performance Indicators (KPIs) are reported:

- Home Wins
- Home Losses
- Home Draws
- Away Wins
- Away Losses
- Away Draws
- Home Goals Scored
- Away Goals Scored
- Home Goals Conceded
- Away Goals Conceded
- Home Points
- Away Points
- Home Win Percentage
- Away Win Percentage

---

# KPI Definitions

## Home Wins

The total number of matches won while playing at home.

---

## Away Wins

The total number of matches won while playing away.

---

## Home Points

Calculated using the standard league points system:

```
3 × Home Wins + Home Draws
```

---

## Away Points

Calculated using:

```
3 × Away Wins + Away Draws
```

---

## Home Win Percentage

**Formula**

```
Home Wins
-------------------
Home Matches
×100
```

---

## Away Win Percentage

**Formula**

```
Away Wins
-------------------
Away Matches
×100
```

---

## Results

The query returns one row for every team with the following statistics.

| Team | Home Wins | Away Wins | Home Points | Away Points | Home Win % | Away Win % |
|------|----------:|----------:|------------:|------------:|-----------:|-----------:|

---

# Methodology

- Match outcomes were determined using the official match scores.
- Home and away performances were analysed separately for every team.
- Goals scored and conceded were calculated independently for home and away fixtures.
- League points were calculated using the standard football scoring system (3 points for a win, 1 point for a draw).
- Win percentages were calculated relative to the number of home and away matches played.

---

# Key Insights

### Barcelona and Real Madrid were equally dominant at home

Both **Barcelona** and **Real Madrid** won **16 of their 19 home matches**, achieving an outstanding **84.21% home win rate**. Their exceptional home performances formed the foundation of their title challenge.

---

### Barcelona remained the league's strongest away side

Barcelona recorded **13 away victories** and accumulated **42 away points**, producing an impressive **68.42% away win rate**. Their ability to maintain elite performance levels away from home demonstrates remarkable consistency throughout the season.

---

### Atlético Madrid displayed exceptional defensive consistency both home and away

Atlético Madrid collected **48 home points** and **40 away points**, while conceding only **7 home goals** and **11 away goals**. Their balanced record reflects a disciplined tactical approach that remained effective regardless of venue.

---

### Sevilla relied heavily on home advantage

Sevilla produced one of the league's strongest home records, winning **14 home matches** and collecting **43 home points**. However, they failed to register a single away victory, finishing with **9 away points** and an **away win percentage of 0%**. This represents the most pronounced home-away contrast among all teams in the league.

---

### Home advantage was evident across the league

Most teams earned significantly more points at home than away. Higher home win percentages and stronger goal differences suggest that familiar surroundings, crowd support, and reduced travel demands contributed positively to team performance throughout the season.

---

### Strong teams maintained consistency regardless of venue

Barcelona, Real Madrid, and Atlético Madrid all recorded high win percentages both at home and away. Their ability to consistently secure results in different environments distinguishes them from many mid-table teams that depended heavily on home fixtures.

---

### Several teams struggled away from home

Teams such as **Rayo Vallecano**, **Levante UD**, **Espanyol**, and **Getafe** recorded away win percentages below **16%**, indicating considerable difficulty in translating home performances into positive away results.

---

# Tactical Interpretation

The analysis highlights that home advantage remained an important factor throughout the season. While nearly every team performed better at home, the league's strongest clubs demonstrated an ability to sustain high performance levels regardless of venue.

In contrast, several mid-table and lower-table teams relied heavily on home fixtures to accumulate points, suggesting that tactical confidence, defensive organization, and attacking effectiveness declined when playing away.

These findings complement the Overall Performance analysis by providing additional context on where teams accumulated points and how venue influenced seasonal success.

---

# Notes

- League points follow the standard football scoring system (3 points for a win and 1 point for a draw).
- Win percentages are calculated separately for home and away matches.
- Goals scored and conceded are based on official match results.
- This analysis focuses on team-level venue performance across the full league season.
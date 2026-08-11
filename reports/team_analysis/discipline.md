# Discipline Performance

## Overview

Discipline plays an important role in football performance. Teams that consistently commit fouls or receive cards risk conceding dangerous set pieces, playing with fewer players following dismissals, and accumulating suspensions over the course of a season.

This analysis evaluates each team's disciplinary record by measuring fouls committed, cards received, and disciplinary averages per match.

---

## Business Question

**Which teams displayed the highest and lowest levels of discipline throughout the season?**

---

## Data Sources

The analysis uses:

- Teams
- Matches
- Events
- FoulCommittedEvents
- BadBehaviourEvents
- Cards

---

## Metrics

- Total Fouls
- Yellow Cards
- Straight Red Cards
- Second Yellow Cards
- Total Cards
- Fouls per Match
- Yellow Cards per Match
- Red Cards per Match
- Second Yellow Cards per Match

---

# KPI Definitions

## Total Fouls

The total number of fouls committed throughout the season.

---

## Yellow Cards

Total cautions received.

---

## Straight Red Cards

Players sent off directly without a previous caution.

---

## Second Yellow Cards

Players dismissed after receiving a second yellow card.

---

## Total Cards

The combined total of:

- Yellow Cards
- Straight Red Cards
- Second Yellow Cards

---

## Fouls per Match

Formula

```
Total Fouls
------------
Matches Played
```

---

## Yellow Cards per Match

Formula

```
Yellow Cards
--------------
Matches Played
```

---

## Red Cards per Match

Formula

```
Straight Red Cards
-------------------
Matches Played
```

---

## Results

One row is returned for every team containing disciplinary statistics.

---

# Methodology

- Fouls were obtained from the `FoulCommittedEvents` table.
- Card information was collected by combining `FoulCommittedEvents` and `BadBehaviourEvents`.
- Cards were classified as Yellow, Second Yellow, or Straight Red using the `Cards` lookup table.
- Per-match metrics were calculated by dividing season totals by matches played.

---

# Key Insights

### Granada committed the most fouls

Granada recorded **237 fouls**, averaging **6.24 fouls per match**, making them one of the league's most aggressive teams.

---

### Getafe and Eibar also ranked among the league's most physical sides

Getafe (**252 fouls**) and Eibar (**248 fouls**) consistently ranked near the top for fouls committed, reflecting a more combative defensive approach.

---

### Barcelona were the league's most disciplined team

Barcelona committed only **136 fouls**, averaging **3.58 fouls per match**, while also receiving the fewest yellow cards (**67**). Their high-possession style reduced the need for defensive interventions.

---

### Yellow cards closely followed foul frequency

Teams committing more fouls generally accumulated more yellow cards, demonstrating a strong relationship between aggressive defensive play and disciplinary sanctions.

---

### Straight red cards remained relatively rare

Most teams received between **0 and 2** straight red cards during the season, highlighting that direct dismissals were uncommon compared with yellow card offences.

---

### Second yellow dismissals were uncommon

Second yellow red cards occurred infrequently across the league, with most teams recording between **2 and 5** dismissals.

---

### Rayo Vallecano recorded the highest number of straight red cards

Rayo Vallecano received **6 straight red cards**, considerably more than any other team, indicating a tendency toward more severe disciplinary incidents.

---

# Tactical Interpretation

Possession-oriented teams such as Barcelona and Real Madrid generally committed fewer fouls and accumulated fewer cards, reflecting longer periods of ball control and reduced defensive pressure.

Conversely, teams defending for longer periods often committed more fouls as they attempted to disrupt opposition attacks, leading to higher yellow card totals.

Disciplinary performance therefore provides additional context for understanding defensive styles alongside the Defensive Performance analysis.

---

# Notes

- Card statistics combine records from both `FoulCommittedEvents` and `BadBehaviourEvents`.
- Straight red cards and second yellow dismissals are reported separately.
- Per-match metrics are calculated over the full league season.
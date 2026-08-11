# Passing Performance

## Overview

Passing is one of the most important indicators of a team's playing philosophy and ability to control a football match. While attacking metrics measure the end product, passing metrics reveal how teams build attacks, retain possession, and progress the ball across the pitch.

This analysis evaluates the passing performance of every team by measuring passing volume, passing efficiency, pass height distribution, and pass length distribution.

---

## Business Question

**Which teams demonstrated the strongest passing performance throughout the season based on passing volume, completion rate, and passing style?**

---

## Data Sources

The analysis uses the following database tables:

- Teams
- Matches
- Events
- PassEvents
- PassOutcomes
- PassHeights

---

## Metrics

The following Key Performance Indicators (KPIs) are reported:

- Total Passes
- Successful Passes
- Pass Accuracy
- High Passes
- Low Passes
- Ground Passes
- Average Pass Length
- Short Passes (0–15 m)
- Medium Passes (15–30 m)
- Long Passes (>30 m)

---

# KPI Definitions

## Total Passes

The total number of passes attempted during the season.

---

## Successful Passes

The total number of completed passes.

A pass is considered successful when:

```
pass_outcome_id IS NULL
```

according to the StatsBomb event model.

---

## Pass Accuracy

**Formula**

```
Successful Passes
------------------
Total Passes
×100
```

Measures the proportion of attempted passes that successfully reached a teammate.

---

## High Passes

The number of aerial or lofted passes attempted.

---

## Low Passes

The number of passes played with a slight elevation above the ground.

---

## Ground Passes

The number of passes played directly along the ground.

---

## Average Pass Length

**Formula**

```
Average(pass_length)
```

Measures the average distance travelled by every pass.

Higher values generally indicate a more direct playing style, whereas lower values indicate shorter passing sequences.

---

## Short Passes (0–15 m)

Passes with a length between **0 and 15 metres**.

---

## Medium Passes (15–30 m)

Passes with a length between **15 and 30 metres**.

---

## Long Passes (>30 m)

Passes exceeding **30 metres**.

---

# Results

The query returns one row for every team with the following passing statistics.

| Team | Total Passes | Successful Passes | Pass Accuracy | High | Low | Ground | Avg Length | 0–15 m | 15–30 m | >30 m |
|------|-------------:|------------------:|--------------:|------:|----:|--------:|-----------:|--------:|---------:|-------:|

---

# Methodology

- Every pass event was linked to the corresponding team through the Events table.
- Total passes were calculated using all records in the PassEvents table.
- Successful passes were identified using the absence of a pass outcome (`pass_outcome_id IS NULL`).
- Pass accuracy was calculated as the ratio of successful passes to total attempted passes.
- Pass height was classified using the PassHeights lookup table.
- Pass length was analysed using the recorded pass distance and categorized into short (0–15 m), medium (15–30 m), and long (>30 m) passes.

---

# Key Insights

### Barcelona dominated passing volume

Barcelona completed **25,707 passes**, the highest total in the league, while also recording the highest number of successful passes (**22,132**) and the highest pass accuracy (**86.09%**).

This reflects a possession-oriented playing style built around sustained ball retention, patient build-up play, and precise passing combinations.

---

### Real Madrid combined volume with efficiency

Real Madrid attempted **23,279 passes** with an impressive **84.62%** completion rate.

Although they attempted fewer passes than Barcelona, their passing efficiency remained among the league's highest, highlighting a balance between controlled possession and vertical attacking play.

---

### Possession-oriented teams attempted significantly more passes

Barcelona, Real Madrid, Las Palmas, and Celta Vigo all exceeded **20,000 passes**, suggesting a tactical emphasis on maintaining possession and progressing attacks through structured passing sequences rather than direct long-ball football.

---

### Direct-playing teams preferred longer passes

Teams such as **Eibar (23.95 m)**, **Granada (23.52 m)**, **Sporting Gijón (23.29 m)**, and **Levante UD (23.06 m)** recorded the longest average pass lengths.

These teams relied more heavily on direct progression, frequently bypassing midfield with longer forward passes.

---

### Passing efficiency varied considerably across teams

Pass accuracy ranged from **86.09% (Barcelona)** to **67.20% (Eibar)**.

This difference illustrates contrasting tactical philosophies, with possession-oriented teams prioritizing ball retention, while more direct teams accepted a higher level of passing risk in exchange for quicker progression.

---

### Ground passing remained the dominant method of distribution

Across every team, ground passes represented the largest proportion of total passes.

This highlights that modern football predominantly relies on controlled ground-based ball circulation, with high and low passes serving more specialized tactical purposes.

---

### Pass length distribution reveals tactical identity

- Teams with a large proportion of **short passes (0–15 m)** generally favoured possession-based football and patient build-up play.
- Teams producing more **long passes (>30 m)** tended to adopt a direct style focused on rapid territorial progression and attacking transitions.
- Medium-distance passes formed the core of ball progression for most teams, balancing possession with forward movement.

---

# Tactical Interpretation

The passing metrics reveal clear stylistic differences between teams rather than simply identifying which team passed the ball most often.

Possession-oriented teams generally exhibit:

- High passing volume
- High pass accuracy
- Shorter average pass lengths
- Greater reliance on ground passes

Conversely, direct teams typically demonstrate:

- Lower passing accuracy
- Longer average pass lengths
- Higher proportions of aerial passes
- Greater use of long-range distribution to advance play quickly.

These stylistic differences complement the attacking and defensive analyses, helping explain how teams generated scoring opportunities and controlled matches throughout the season.

---

# Notes

- Successful passes are defined according to the StatsBomb event model (`pass_outcome_id IS NULL`).
- Pass height categories follow the official StatsBomb classifications.
- Pass length categories (0–15 m, 15–30 m, >30 m) were defined specifically for this project to distinguish short, medium, and long passing tendencies.
- This analysis focuses on team-level passing performance rather than individual player contributions.
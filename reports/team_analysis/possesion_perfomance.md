# Possession Performance

## Overview

Possession reflects a team's ability to control the tempo and rhythm of a football match. However, possession is more than simply keeping the ball. Effective possession involves sustaining possession sequences, progressing the ball through multiple actions, and creating attacking opportunities while limiting the opponent's control.

This analysis estimates possession performance using the StatsBomb event model by combining possession duration, possession frequency, and possession quality metrics.

---

## Business Question

**Which teams controlled possession most effectively throughout the season?**

---

## Data Sources

The analysis uses the following database tables:

- Teams
- Matches
- Events
- PassEvents

---

## Metrics

The following Key Performance Indicators (KPIs) are reported:

- Average Possession Percentage
- Total Possessions
- Average Possession Duration
- Events per Possession
- Passes per Possession

---

# KPI Definitions

## Average Possession Percentage

Estimated as:

```
Team Possession Time
--------------------------
Total Match Possession Time
×100
```

where possession time is calculated by summing the duration of all events occurring while a team is in possession.

---

## Total Possessions

The total number of unique possession sequences initiated by a team throughout the season.

Each possession is uniquely identified using the combination:

```
(match_id, possession)
```

---

## Average Possession Duration

**Formula**

```
Total Possession Time
----------------------
Total Possessions
```

Represents the average length of time each possession sequence lasts.

---

## Events per Possession

**Formula**

```
Total Events
----------------
Total Possessions
```

Measures the average number of recorded actions completed before possession changes.

---

## Passes per Possession

**Formula**

```
Total Passes
----------------
Total Possessions
```

Indicates how frequently a team circulates the ball within each possession sequence.

---

# Results

The query returns one row for every team containing the following possession statistics.

| Team | Avg Possession (%) | Possessions | Avg Duration (s) | Events / Possession | Passes / Possession |
|------|-------------------:|------------:|-----------------:|--------------------:|--------------------:|

---

# Methodology

- Each possession sequence was identified using the `(match_id, possession)` combination.
- Event durations were aggregated to estimate possession time.
- Team possession percentages were calculated separately for every match before averaging across the season.
- Possession frequency, possession duration, event count, and passing activity were aggregated at the team level.

---

# Key Insights

### Barcelona dominated possession in every aspect

Barcelona recorded the highest estimated average possession (**66.89%**) while also producing the longest average possession sequences (**23.98 seconds**), the highest number of events per possession (**25.73**), and the most passes per possession (**7.27**).

These figures reflect an exceptional ability to sustain possession through extended passing sequences and patient build-up play.

---

### Real Madrid combined control with quicker progression

Real Madrid averaged **57.19%** possession with an average possession duration of **18.73 seconds** and **6.22 passes per possession**.

Compared with Barcelona, Real Madrid maintained possession for shorter periods while progressing attacks more directly, illustrating a balance between possession control and vertical attacking football.

---

### Las Palmas and Celta Vigo embraced possession-based football

Both Las Palmas (**55.54%**) and Celta Vigo (**55.25%**) ranked among the league leaders in possession.

Their high possession percentages, combined with relatively long possession durations and over five passes per possession, indicate a clear emphasis on patient ball circulation and controlled build-up.

---

### Possession frequency does not necessarily indicate control

Rayo Vallecano recorded the highest number of possession sequences (**4,222**) but averaged only **14.32 seconds** per possession.

This suggests that although they regained possession frequently, many possessions were relatively short, indicating a faster and more direct style of play rather than prolonged ball retention.

---

### Longer possessions generated more actions

Barcelona averaged **25.73 events** during every possession sequence, considerably higher than most teams in the league.

In contrast, teams such as Eibar (**14.73**) and Sporting Gijón (**15.14**) completed far fewer actions before losing possession, highlighting notable differences in ball retention and build-up quality.

---

### Passing intensity closely followed possession quality

The relationship between possession duration and passes per possession is clearly visible across the league.

Teams with longer possession sequences generally completed more passes within each possession, while teams with shorter possessions relied on quicker progression and fewer passes before either losing possession or attempting to attack.

---

### Atlético Madrid demonstrated efficient possession without dominance

Atlético Madrid averaged **47.52%** possession, placing them in the lower half of the league.

However, they still averaged **18.48 events** and **5.21 passes** per possession, suggesting that although they controlled the ball less frequently, they made effective use of their possessions through structured build-up and disciplined play.

---

# Tactical Interpretation

The possession metrics reveal distinct tactical identities across the league.

Possession-oriented teams generally exhibit:

- Higher possession percentages
- Longer possession sequences
- Greater numbers of actions within each possession
- More passes before losing possession

Conversely, direct teams typically demonstrate:

- Lower possession percentages
- Shorter possession sequences
- Fewer events per possession
- Quicker transitions toward attacking opportunities

These differences complement the Passing Performance analysis and provide additional context for understanding how teams controlled matches and constructed attacks.

---

# Notes

- Possession statistics are estimated using the duration of events recorded while a team is in possession.
- Each possession sequence is uniquely identified by the `(match_id, possession)` combination.
- Since official possession percentages are not included in the StatsBomb Open Data dataset, the reported values represent analytical estimates rather than official match statistics.
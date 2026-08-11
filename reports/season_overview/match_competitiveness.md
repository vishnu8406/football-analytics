# Match Competitiveness

## Overview

This section evaluates the competitive nature of the season by analyzing match outcomes, draw frequency, goalless matches, and the prevalence of high-scoring games. These metrics provide insight into the overall entertainment value and competitive balance of the competition.

---

## Business Question

**How competitive and entertaining was the season based on match outcomes and scoring patterns?**

---

## Data Sources

The analysis was performed using the following database table:

- `Matches`

---

## Metrics

The following key performance indicators (KPIs) are reported:

- Total Matches
- Home Wins
- Away Wins
- Draws
- Draw Percentage
- Goalless Draws
- High-Scoring Matches (>3 Goals)

---

## Results

| Metric | Value |
|------------------------------|------:|
| Total Matches | 380 |
| Home Wins | 183 |
| Away Wins | 105 |
| Draws | 92 |
| Draw Percentage | 24.21% |
| Goalless Draws | 25 |
| High-Scoring Matches (>3 Goals) | 110 |

---

## Methodology

The following definitions were used for this analysis:

- **Home Win:** Home team's score is greater than the away team's score.
- **Away Win:** Away team's score is greater than the home team's score.
- **Draw:** Both teams finish with the same score.
- **Goalless Draw:** A match ending 0–0.
- **High-Scoring Match:** A match with more than three total goals.

---

## Insight

The season consisted of **380 matches**, with **183 home victories**, **105 away victories**, and **92 draws**, resulting in a **draw rate of 24.21%**.

Home teams won significantly more matches than away teams, indicating a noticeable **home advantage** throughout the season. Home victories accounted for nearly half of all matches, while away teams secured considerably fewer wins.

Only **25 matches (6.58%)** ended in a goalless draw, suggesting that scoreless games were relatively uncommon. In contrast, **110 matches (28.95%)** produced more than three goals, highlighting a substantial number of high-scoring encounters.

Overall, the combination of a low number of goalless draws and a high proportion of high-scoring matches suggests that the season was generally **competitive, open, and entertaining for spectators**.

---

## Notes

- Match outcomes were derived directly from the final scores recorded in the `Matches` table.
- A high-scoring match is defined as any match with more than three total goals.
- Percentages are calculated using the total number of matches (380) as the denominator.
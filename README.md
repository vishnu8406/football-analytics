# ⚽ Football Analytics Dashboard

A professional football analytics platform built using **Python, SQLite, Streamlit, Pandas, and StatsBomb Open Data**.

This project transforms raw football event data into interactive visualizations and analytics dashboards, enabling match, player, team, and possession-level analysis.

---

## 🚀 Features

### 📊 Match Analysis
- Match summary
- Event timeline
- Team lineups
- Cards and substitutions
- Goalkeeper actions

### 🎯 Shot Analysis
- Interactive shot maps
- Real football pitch visualization
- Shot outcomes
- xG (Expected Goals)
- Team shot comparison

### 🔥 Player Analysis
- Player heatmaps
- Touch location analysis
- Player activity visualization

### 🕸 Pass Network Analysis
- Team passing network
- Passing connections between players
- Pass volume visualization

### ⚽ xG Analysis
- Team xG comparison
- Match xG breakdown
- Shot quality assessment

### 🔄 Possession Explorer
- Full possession visualization
- Event-by-event sequence analysis
- Passes, carries, dribbles and shots
- Possession outcomes
- Attacking direction normalization

---

## 🛠 Tech Stack

### Programming
- Python

### Data Analysis
- Pandas
- NumPy

### Database
- SQLite

### Visualization
- Matplotlib
- mplsoccer

### Dashboard
- Streamlit

### Data Source
- StatsBomb Open Data

---

## 📂 Project Structure

```text
football-analytics/

├── dashboard/
│   ├── Home.py
│   └── pages/
│       ├── 1_match_analysis.py
│       ├── 2_player_heatmap.py
│       ├── 3_xg_analysis.py
│       ├── 4_pass_network.py
│       └── 11_possession_explorer.py
│
├── scripts/
│   ├── database/
│   ├── preprocessing/
│   └── analytics/
│
├── reports/
│   └── csv/
│
├── data/
│   ├── database/
│   └── raw/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 📈 Dashboard Pages

| Page | Description |
|--------|-------------|
| Match Analysis | Match statistics, lineups, timeline |
| Player Heatmap | Player positional activity |
| xG Analysis | Expected goals comparison |
| Pass Network | Team passing structures |
| Possession Explorer | Event sequence visualization |

---

## 📊 Analytics Pipeline

```text
StatsBomb Open Data
            │
            ▼
      JSON Files
            │
            ▼
      SQLite Database
            │
            ▼
    Data Processing Scripts
            │
            ▼
      Analytics CSV Layer
            │
            ▼
    Streamlit Dashboard
            │
            ▼
      Football Insights
```

---

## ⚽ Data Source

This project uses the official StatsBomb Open Data repository.

StatsBomb provides detailed football event data including:

- Matches
- Events
- Lineups
- Shots
- Passes
- Possessions
- Player actions

Repository:

https://github.com/statsbomb/open-data

---

## 📸 Screenshots

### Home Page

_Add screenshot here_

### Match Analysis

_Add screenshot here_

### Shot Map

_Add screenshot here_

### Pass Network

_Add screenshot here_

### Possession Explorer

_Add screenshot here_

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/football-analytics.git

cd football-analytics
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the dashboard:

```bash
streamlit run dashboard/Home.py
```

---

## 🌐 Deployment

The dashboard can be deployed using:

- Streamlit Community Cloud
- Render
- Railway

Recommended:

Streamlit Community Cloud

---

## 🎯 Project Objectives

The goal of this project is to demonstrate:

- Data Engineering
- Database Design
- ETL Pipelines
- Data Analysis
- Sports Analytics
- Dashboard Development
- Data Visualization

through a complete end-to-end football analytics workflow.

---

## 🔮 Future Enhancements

### Version 2

- Team Dashboard
- Goal Build-Up Analysis
- Progressive Pass Analysis
- Final Third Entries
- Turnover Analysis
- Passing Lanes
- Player Comparison Dashboard
- Team Comparison Dashboard
- Season Analytics

---

## 👨‍💻 Author

**Vishnu / S. Maiyarasu**

Electrical & Electronics Engineering  
Data Analytics Enthusiast  
Python Developer  
Football Analytics Explorer

---

## ⭐ Acknowledgements

- StatsBomb Open Data
- Streamlit
- mplsoccer
- Pandas Community
- Python Open Source Ecosystem

---

If you found this project useful, consider giving it a ⭐ on GitHub.

## 📄 License

This project is licensed under the MIT License.# football-analysis

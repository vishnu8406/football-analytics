import streamlit as st
import pandas as pd
import sqlite3

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="La Liga 2015/16 Analytics Platform",
    page_icon="⚽",
    layout="wide"
)

# ==================================================
# DATABASE CONNECTION
# ==================================================
def load_data():

    matches = pd.read_csv(
        "https://huggingface.co/datasets/Maiyarasu/football_analytics/resolve/main/csv/match_analysis/match_summary.csv"
    )

    sequence = pd.read_csv(
        "https://huggingface.co/datasets/Maiyarasu/football_analytics/resolve/main/csv/event_sequence/sequence_events.csv"
    )

    return matches, sequence

matches, sequence = load_data()
total_matches = matches["match_id"].nunique()

total_events = len(sequence)

total_players = sequence["player_name"].nunique()

total_teams = sequence["team_name"].nunique()
# ==================================================
# HERO
# ==================================================

st.markdown("""
<div style='text-align:center;padding-top:20px;'>

<h1>⚽ La Liga 2015/16 Football Analytics Platform</h1>

<h3>
Interactive Football Analytics Dashboard Powered by StatsBomb Open Data
</h3>

<p style='font-size:18px'>
Explore player performance, team statistics, passing networks,
expected goals, possession sequences and match analytics
from the complete La Liga 2015/16 season.
</p>

</div>
""", unsafe_allow_html=True)

# ==================================================
# DATASET NOTICE
# ==================================================

st.warning("""
📌 DATASET SCOPE

This platform currently analyzes only the Spanish La Liga 2015/16 season.

All statistics, visualizations and dashboards are generated from
StatsBomb Open Data.

Future versions will support additional leagues and seasons.
""")

# ==================================================
# METRICS
# ==================================================

st.markdown("---")
st.header("📊 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Matches",
        f"{total_matches:,}"
    )

with col2:
    st.metric(
        "Events",
        f"{total_events:,}"
    )

with col3:
    st.metric(
        "Players",
        f"{total_players:,}"
    )

with col4:
    st.metric(
        "Teams",
        f"{total_teams:,}"
    )

# ==================================================
# QUICK NAVIGATION
# ==================================================

st.markdown("---")
st.header("🚀 Analytics Modules")

col1, col2, col3 = st.columns(3)

with col1:

    st.info("""
### ⚽ Team Analysis

Analyze team-level performance,
attacking metrics,
defensive metrics
""")

    st.page_link(
        "pages/1_team_analysis.py",
        label="Open Team Analysis",
        icon="⚽"
    )

    st.markdown("")

    st.info("""
### 📊 Team Comparison

Compare two teams
across multiple
performance metrics
""")

    st.page_link(
        "pages/4_team_comparison.py",
        label="Open Team Comparison",
        icon="📊"
    )

with col2:

    st.info("""
### 👤 Player Analysis

Player statistics,
performance metrics,
season insights
""")

    st.page_link(
        "pages/2_player_analysis.py",
        label="Open Player Analysis",
        icon="👤"
    )

    st.markdown("")

    st.info("""
### ⚖️ Player Comparison

Compare players
across attacking
and defensive metrics
""")

    st.page_link(
        "pages/3_player_comparison.py",
        label="Open Player Comparison",
        icon="⚖️"
    )

    st.markdown("")

    st.info("""
### 📡 Player Radar

Advanced player
radar visualizations
""")

    st.page_link(
        "pages/5_player_radar.py",
        label="Open Player Radar",
        icon="📡"
    )

with col3:

    st.info("""
### 📅 Match Analysis

Match timeline,
lineups,
cards and goals
""")

    st.page_link(
        "pages/6_match_analysis.py",
        label="Open Match Analysis",
        icon="📅"
    )

    st.markdown("")

    st.info("""
### 🔥 Player Heatmap

Visualize player
touch locations and
activity zones
""")

    st.page_link(
        "pages/7_player_heatmap.py",
        label="Open Player Heatmap",
        icon="🔥"
    )

# ==================================================
# ADVANCED ANALYTICS
# ==================================================

st.markdown("---")
st.header("🎯 Advanced Analytics")

col1, col2 = st.columns(2)

with col1:

    st.info("""
### 🎯 xG Analysis

Expected Goals Analysis

- Team xG
- Match xG
- Shot Quality
- Finishing Analysis
""")

    st.page_link(
        "pages/8_xG_analysis.py",
        label="Open xG Analysis",
        icon="🎯"
    )

with col2:

    st.info("""
### 🕸 Pass Network

Passing Structures

- Team Networks
- Player Connections
- Passing Patterns
""")

    st.page_link(
        "pages/9_pass_network.py",
        label="Open Pass Network",
        icon="🕸"
    )

# ==================================================
# POSSESSION ANALYTICS
# ==================================================

st.markdown("---")
st.header("🔄 Possession Analytics")

st.info("""
### Possession Explorer

Visualize complete possession sequences
event-by-event on a football pitch.

Features:

- Passes
- Carries
- Dribbles
- Shots
- Goal Sequences
- Possession Outcomes
""")

st.page_link(
    "pages/10_possession_explorer.py",
    label="Open Possession Explorer",
    icon="🔄"
)

# ==================================================
# ABOUT
# ==================================================

st.markdown("---")
st.header("📖 About The Project")

st.write("""
This project was developed as an end-to-end football analytics platform.

Raw StatsBomb JSON data was transformed into a fully normalized
SQLite database and used to create advanced football analytics
dashboards.

The project demonstrates:

- Data Engineering
- Database Design
- ETL Pipelines
- SQL Analytics
- Data Visualization
- Sports Analytics
- Dashboard Development
""")

# ==================================================
# TECH STACK
# ==================================================

st.markdown("---")
st.header("🛠 Technology Stack")

col1, col2, col3 = st.columns(3)

with col1:

    st.success("""
### Data Engineering

- Python
- Pandas
- NumPy
- SQLite
""")

with col2:

    st.success("""
### Visualization

- Streamlit
- Matplotlib
- mplsoccer
""")

with col3:

    st.success("""
### Data Source

- StatsBomb Open Data
- Match Data
- Event Data
- Lineup Data
""")

# ==================================================
# ROADMAP
# ==================================================

st.markdown("---")
st.header("🛣 Future Roadmap")

roadmap = pd.DataFrame(
    {
        "Feature": [
            "Team Dashboard",
            "Goal Build-Up Analysis",
            "Progressive Pass Analysis",
            "Final Third Entries",
            "Player Similarity Models",
            "Season Analytics",
            "Machine Learning Models"
        ],
        "Status": [
            "Planned",
            "Planned",
            "Planned",
            "Planned",
            "Planned",
            "Planned",
            "Planned"
        ]
    }
)

st.dataframe(
    roadmap,
    width="stretch",
    hide_index=True
)

# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.caption(
    "⚽ La Liga 2015/16 Football Analytics Platform | Version 1.0 | Powered by StatsBomb Open Data"
)

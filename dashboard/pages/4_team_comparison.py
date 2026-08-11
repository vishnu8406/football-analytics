import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Team Comparison",
    layout="wide"
)

st.title("⚔️ Team Comparison")

# ----------------------------------
# Load Data
# ----------------------------------

@st.cache_data
def load_team_performance():
    return pd.read_csv(
        "https://huggingface.co/datasets/Maiyarasu/football_analytics/resolve/main/csv/team_analysis/overall_performance.csv"
    )

df = load_team_performance()

# ----------------------------------
# Team Selection
# ----------------------------------

col1, col2 = st.columns(2)

with col1:
    team1 = st.selectbox(
        "Select Team 1",
        sorted(df["team_name"].unique())
    )

with col2:
    team2 = st.selectbox(
        "Select Team 2",
        sorted(df["team_name"].unique()),
        index=1
    )

# ----------------------------------
# Team Data
# ----------------------------------

t1 = df[df["team_name"] == team1].iloc[0]
t2 = df[df["team_name"] == team2].iloc[0]

# ----------------------------------
# Comparison Table
# ----------------------------------

comparison = pd.DataFrame({
    "Metric": [
        "Points",
        "Wins",
        "Draws",
        "Losses",
        "Goals For",
        "Goals Against",
        "Goal Difference",
        "Win %",
        "Points / Match"
    ],
    team1: [
        t1["points"],
        t1["total_wins"],
        t1["total_draws"],
        t1["total_losses"],
        t1["goals_for"],
        t1["goals_against"],
        t1["goal_difference"],
        t1["win_percentage"],
        t1["points_per_match"]
    ],
    team2: [
        t2["points"],
        t2["total_wins"],
        t2["total_draws"],
        t2["total_losses"],
        t2["goals_for"],
        t2["goals_against"],
        t2["goal_difference"],
        t2["win_percentage"],
        t2["points_per_match"]
    ]
})

st.subheader("Comparison Table")
st.dataframe(comparison, use_container_width=True)

# ----------------------------------
# Grouped Bar Chart
# ----------------------------------

chart_df = pd.DataFrame({
    "Metric": [
        "Points",
        "Wins",
        "Goals For",
        "Goal Difference"
    ] * 2,

    "Value": [
        t1["points"],
        t1["total_wins"],
        t1["goals_for"],
        t1["goal_difference"],

        t2["points"],
        t2["total_wins"],
        t2["goals_for"],
        t2["goal_difference"]
    ],

    "Team": [
        team1,
        team1,
        team1,
        team1,

        team2,
        team2,
        team2,
        team2
    ]
})

fig = px.bar(
    chart_df,
    x="Metric",
    y="Value",
    color="Team",
    barmode="group",
    title="Team Performance Comparison"
)

st.plotly_chart(fig, use_container_width=True)

import plotly.graph_objects as go

metrics = [
    "points",
    "goals_for",
    "goal_difference",
    "win_percentage",
    "points_per_match"
]

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=[t1[m] for m in metrics],
    theta=metrics,
    fill="toself",
    name=team1
))

fig.add_trace(go.Scatterpolar(
    r=[t2[m] for m in metrics],
    theta=metrics,
    fill="toself",
    name=team2
))

st.plotly_chart(fig)
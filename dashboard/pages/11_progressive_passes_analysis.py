import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import load_parquet

st.set_page_config(
    page_title="Progressive Pass Analysis",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Progressive Pass Analysis")

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------

@st.cache_data
def load_data():

    player_df = load_parquet(
        "progressive_passes/player_progressive_passes.parquet"
    )

    team_df = load_parquet(
        "progressive_passes/team_progressive_passes.parquet"
    )

    event_df = load_parquet(
        "progressive_passes/progressive_passes.parquet"
    )

    return player_df, team_df, event_df


player_df, team_df, event_df = load_data()

# ---------------------------------------------------
# Top Players
# ---------------------------------------------------

st.subheader("🏆 Top Progressive Pass Players")

top_players = (
    player_df
    .sort_values(
        "progressive_passes",
        ascending=False
    )
    .head(20)
)

fig = px.bar(
    top_players,
    x="player_name",
    y="progressive_passes",
    color="team_name",
    title="Top 20 Players by Progressive Passes"
)

fig.update_layout(
    xaxis_title="Player",
    yaxis_title="Progressive Passes"
)

st.plotly_chart(
    fig,
    width="stretch"
)

# ---------------------------------------------------
# Team Ranking
# ---------------------------------------------------

st.subheader("⚽ Team Progressive Passing Ranking")

fig = px.bar(
    team_df.sort_values(
        "progressive_passes",
        ascending=False
    ),
    x="team_name",
    y="progressive_passes",
    color="success_rate",
    title="Progressive Passes by Team"
)

st.plotly_chart(
    fig,
    width="stretch"
)

# ---------------------------------------------------
# Player Selector
# ---------------------------------------------------

st.markdown("---")

selected_player = st.selectbox(
    "Select Player",
    sorted(player_df["player_name"].unique())
)

player_row = player_df[
    player_df["player_name"] == selected_player
].iloc[0]

# ---------------------------------------------------
# KPI Cards
# ---------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Progressive Passes",
    int(player_row["progressive_passes"])
)

col2.metric(
    "Successful",
    int(player_row["successful_progressive_passes"])
)

col3.metric(
    "Success %",
    f"{player_row['success_rate']:.1f}%"
)

col4.metric(
    "Avg Distance",
    f"{player_row['avg_progress_distance']:.1f} m"
)

# ---------------------------------------------------
# Progress Distance Distribution
# ---------------------------------------------------

st.markdown("---")
st.subheader("📈 Progress Distance Distribution")

player_events = event_df.merge(
    player_df[["player_name"]],
    left_on="player_name",
    right_on="player_name"
)

player_events = player_events[
    player_events["player_name"] == selected_player
]

fig = px.histogram(
    player_events,
    x="progress_distance",
    nbins=30,
    title="Progress Distance Distribution"
)

st.plotly_chart(
    fig,
    width="stretch"
)

# ---------------------------------------------------
# Team Comparison
# ---------------------------------------------------

st.markdown("---")
st.subheader("⚔️ Team Comparison")

team1 = st.selectbox(
    "Team 1",
    sorted(team_df["team_name"].unique())
)

team2 = st.selectbox(
    "Team 2",
    sorted(team_df["team_name"].unique()),
    index=1
)

comparison = team_df[
    team_df["team_name"].isin(
        [team1, team2]
    )
]

metrics = [
    "progressive_passes",
    "successful_progressive_passes",
    "avg_progress_distance"
]

fig = go.Figure()

for metric in metrics:

    fig.add_trace(
        go.Bar(
            name=metric.replace("_", " ").title(),
            x=comparison["team_name"],
            y=comparison[metric]
        )
    )

fig.update_layout(
    barmode="group",
    title="Team Progressive Passing Comparison"
)

st.plotly_chart(
    fig,
    width="stretch"
)

# ---------------------------------------------------
# Raw Data
# ---------------------------------------------------

st.markdown("---")
st.subheader("📋 Player Progressive Passing Table")

st.dataframe(
    player_df.sort_values(
        "progressive_passes",
        ascending=False
    ),
    width="stretch"
)
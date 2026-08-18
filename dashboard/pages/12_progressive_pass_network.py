import streamlit as st
import pandas as pd

from mplsoccer import Pitch
import matplotlib.pyplot as plt

from utils.data_loader import load_parquet

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="Progressive Pass Network",
    page_icon="🕸️",
    layout="wide"
)

st.title("🕸️ Progressive Pass Network")

# --------------------------------------------------
# Load Data
# --------------------------------------------------

@st.cache_data
def load_data():

    return load_parquet(
        "progressive_passes/progressive_pass_network.parquet"
    )

df = load_data()

# --------------------------------------------------
# Team Selector
# --------------------------------------------------

teams = sorted(df["team_name"].unique())

selected_team = st.selectbox(
    "Select Team",
    teams
)

team_df = df[
    df["team_name"] == selected_team
].copy()

# --------------------------------------------------
# Filters
# --------------------------------------------------

st.sidebar.header("Filters")

min_passes = st.sidebar.slider(
    "Minimum Progressive Passes",
    min_value=1,
    max_value=int(team_df["progressive_pass_count"].max()),
    value=5
)

team_df = team_df[
    team_df["progressive_pass_count"] >= min_passes
]

if team_df.empty:
    st.warning("No data available for selected filter.")
    st.stop()

# --------------------------------------------------
# Build Node Positions
# --------------------------------------------------

node_df = (
    team_df.groupby("passer")
    .agg(
        avg_x=("avg_x", "mean"),
        avg_y=("avg_y", "mean"),
        total_passes=("progressive_pass_count", "sum")
    )
    .reset_index()
)

# --------------------------------------------------
# Draw Network
# --------------------------------------------------

pitch = Pitch(
    pitch_type="statsbomb",
    pitch_color="#0E1117",
    line_color="white"
)

fig, ax = pitch.draw(
    figsize=(14, 10)
)

# --------------------------------------------------
# Draw Pass Links
# --------------------------------------------------

max_passes = team_df["progressive_pass_count"].max()

for _, row in team_df.iterrows():

    line_width = (
        row["progressive_pass_count"]
        / max_passes
    ) * 10

    pitch.lines(
        row["avg_x"],
        row["avg_y"],
        row["receiver_x"],
        row["receiver_y"],
        lw=line_width,
        alpha=0.7,
        ax=ax
    )

# --------------------------------------------------
# Draw Players
# --------------------------------------------------

pitch.scatter(
    node_df["avg_x"],
    node_df["avg_y"],
    s=node_df["total_passes"] * 3,
    ax=ax
)

# --------------------------------------------------
# Player Labels
# --------------------------------------------------

for _, row in node_df.iterrows():

    ax.text(
        row["avg_x"],
        row["avg_y"],
        row["passer"],
        color="white",
        fontsize=8,
        ha="center",
        va="center"
    )

# --------------------------------------------------
# Title
# --------------------------------------------------

ax.set_title(
    f"{selected_team} Progressive Pass Network",
    fontsize=18,
    color="white"
)

st.pyplot(fig)

# --------------------------------------------------
# Network Metrics
# --------------------------------------------------

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Players",
    node_df.shape[0]
)

col2.metric(
    "Connections",
    team_df.shape[0]
)

col3.metric(
    "Progressive Passes",
    int(
        team_df["progressive_pass_count"].sum()
    )
)

col4.metric(
    "Average Success Rate",
    f"{team_df['success_rate'].mean():.1f}%"
)

# --------------------------------------------------
# Strongest Connections
# --------------------------------------------------

st.markdown("---")
st.subheader("🔥 Strongest Progressive Connections")

top_links = (
    team_df.sort_values(
        "progressive_pass_count",
        ascending=False
    )
    .head(20)
)

st.dataframe(
    top_links[
        [
            "passer",
            "receiver",
            "progressive_pass_count",
            "success_rate",
            "avg_progress_distance"
        ]
    ],
    width="stretch"
)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from mplsoccer import Pitch
from utils.data_loader import load_parquet
# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Pass Network",
    page_icon="🔗",
    layout="wide"
)

st.title("🔗 Pass Network Analysis")

# ==================================================
# LOAD DATA
# ==================================================



passes = load_parquet("pass_network.parquet")

matches = load_parquet(
    "match_analysis/match_summary.parquet"
)

# ==================================================
# MATCH SELECTOR
# ==================================================

matches["match_label"] = (
    matches["home_team"]
    + " vs "
    + matches["away_team"]
    + " | "
    + matches["match_date"].astype(str)
)

selected_match = st.selectbox(
    "Select Match",
    matches["match_label"]
)

match_row = matches[
    matches["match_label"] == selected_match
].iloc[0]

match_id = match_row["match_id"]

# ==================================================
# FILTER MATCH
# ==================================================

match_passes = passes[
    passes["match_id"] == match_id
]

if match_passes.empty:

    st.warning("No pass data available.")
    st.stop()

# ==================================================
# TEAM SELECTOR
# ==================================================

teams = sorted(
    match_passes["team_name"].unique()
)

selected_team = st.selectbox(
    "Select Team",
    teams
)

team_passes = match_passes[
    match_passes["team_name"] == selected_team
]

if team_passes.empty:

    st.warning("No passes for selected team.")
    st.stop()

# ==================================================
# KPI SECTION
# ==================================================

total_passes = len(team_passes)

unique_connections = len(
    team_passes.groupby(
        ["passer", "receiver"]
    )
)

most_involved = pd.concat([
    team_passes["passer"],
    team_passes["receiver"]
]).value_counts()

most_involved_player = most_involved.index[0]

avg_pass_length = round(
    team_passes["pass_length"].mean(),
    2
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Passes",
    total_passes
)

c2.metric(
    "Connections",
    unique_connections
)

c3.metric(
    "Most Involved",
    most_involved_player
)

c4.metric(
    "Avg Pass Length",
    avg_pass_length
)

# ==================================================
# PLAYER POSITIONS
# ==================================================

player_positions = (
    team_passes
    .groupby("passer")
    .agg({
        "location_x": "mean",
        "location_y": "mean"
    })
    .reset_index()
)

# ==================================================
# PASS COUNTS
# ==================================================

connections = (
    team_passes
    .groupby(
        ["passer", "receiver"]
    )
    .size()
    .reset_index(name="pass_count")
)

# Keep only strong links

connections = connections[
    connections["pass_count"] >= 3
]

# ==================================================
# DRAW PITCH
# ==================================================

pitch = Pitch(
    pitch_type="statsbomb",
    pitch_color="white",
    line_color="black"
)

fig, ax = pitch.draw(
    figsize=(14, 10)
)

# ==================================================
# DRAW CONNECTIONS
# ==================================================

for _, row in connections.iterrows():

    passer = row["passer"]
    receiver = row["receiver"]

    count = row["pass_count"]

    p1 = player_positions[
        player_positions["passer"] == passer
    ]

    p2 = player_positions[
        player_positions["passer"] == receiver
    ]

    if p1.empty or p2.empty:
        continue

    x1 = p1.iloc[0]["location_x"]
    y1 = p1.iloc[0]["location_y"]

    x2 = p2.iloc[0]["location_x"]
    y2 = p2.iloc[0]["location_y"]

    pitch.lines(
        x1,
        y1,
        x2,
        y2,
        lw=max(count / 2, 1),
        alpha=0.6,
        ax=ax
    )

# ==================================================
# DRAW PLAYERS
# ==================================================

pitch.scatter(
    player_positions["location_x"],
    player_positions["location_y"],
    s=800,
    edgecolors="black",
    linewidth=2,
    ax=ax
)

# ==================================================
# PLAYER LABELS
# ==================================================

for _, row in player_positions.iterrows():

    ax.text(
        row["location_x"],
        row["location_y"],
        row["passer"],
        ha="center",
        va="center",
        fontsize=8,
        fontweight="bold"
    )

# ==================================================
# TITLE
# ==================================================

ax.set_title(
    f"Pass Network - Team {selected_team}",
    fontsize=18,
    pad=20
)

st.pyplot(fig)

# ==================================================
# TOP CONNECTIONS
# ==================================================

st.markdown("---")
st.subheader("🔥 Top Pass Connections")

top_connections = connections.sort_values(
    "pass_count",
    ascending=False
).head(15)

st.dataframe(
    top_connections,
    width="stretch"
)

# ==================================================
# PLAYER INVOLVEMENT
# ==================================================

st.markdown("---")
st.subheader("📊 Player Involvement")

involvement = pd.concat([
    team_passes["passer"],
    team_passes["receiver"]
]).value_counts()

involvement = involvement.reset_index()

involvement.columns = [
    "player",
    "touches_in_network"
]

st.bar_chart(
    involvement.set_index("player")
)
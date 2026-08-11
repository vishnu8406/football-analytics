import streamlit as st
import pandas as pd

from mplsoccer import Pitch
import matplotlib.pyplot as plt

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Player Heatmap",
    page_icon="🔥",
    layout="wide"
)

st.title("🔥 Player Heatmap")

# ==================================================
# LOAD DATA
# ==================================================

heatmap = pd.read_csv(
    "reports/csv/player_heatmap.csv"
)
match_summary = pd.read_csv(
    "reports/csv/match_analysis/match_summary.csv"
)
# ==================================================
# PLAYER SELECTOR
# ==================================================

player = st.selectbox(
    "Select Player",
    sorted(
        heatmap["player_name"].unique()
    )
)

player_df = heatmap[
    heatmap["player_name"] == player
]

# ==================================================
# MATCH FILTER
# ==================================================

matches = sorted(
    player_df["match_id"].unique()
)

# Matchs played by selected player

player_matches = player_df["match_id"].unique()

match_options = match_summary[
    match_summary["match_id"].isin(player_matches)
].copy()

match_options["match_label"] = (
    match_options["home_team"]
    + " vs "
    + match_options["away_team"]
    + " | "
    + match_options["match_date"].astype(str)
)

match_dict = dict(
    zip(
        match_options["match_label"],
        match_options["match_id"]
    )
)

selected_match = st.selectbox(
    "Select Match",
    ["All Matches"] + list(match_dict.keys())
)

if selected_match != "All Matches":

    selected_match_id = match_dict[selected_match]

    player_df = player_df[
        player_df["match_id"] == selected_match_id
    ]

# ==================================================
# NO DATA CHECK
# ==================================================

if len(player_df) == 0:

    st.warning("No location data available.")
    st.stop()

# ==================================================
# KPI SECTION
# ==================================================

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Events",
    len(player_df)
)

col2.metric(
    "Matches",
    player_df["match_id"].nunique()
)

col3.metric(
    "Average X Position",
    round(
        player_df["location_x"].mean(),
        1
    )
)

# ==================================================
# AVERAGE POSITION
# ==================================================

avg_x = player_df["location_x"].mean()
avg_y = player_df["location_y"].mean()

# ==================================================
# DRAW PITCH
# ==================================================

pitch = Pitch(
    pitch_type="statsbomb",
    pitch_color="white",
    line_color="black"
)

fig, ax = pitch.draw(
    figsize=(12, 8)
)

# ==================================================
# HEATMAP
# ==================================================

pitch.kdeplot(
    player_df["location_x"],
    player_df["location_y"],
    fill=True,
    levels=100,
    thresh=0.05,
    alpha=0.8,
    ax=ax
)

# ==================================================
# EVENT LOCATIONS
# ==================================================

pitch.scatter(
    player_df["location_x"],
    player_df["location_y"],
    s=20,
    alpha=0.4,
    ax=ax
)

# ==================================================
# AVERAGE POSITION MARKER
# ==================================================

pitch.scatter(
    avg_x,
    avg_y,
    s=500,
    color="red",
    edgecolors="black",
    linewidth=2,
    ax=ax
)

ax.text(
    avg_x,
    avg_y,
    "AVG",
    color="white",
    fontsize=10,
    fontweight="bold",
    ha="center",
    va="center"
)

# ==================================================
# TITLE
# ==================================================

ax.set_title(
    f"{player} Heatmap",
    fontsize=18,
    pad=20
)

st.pyplot(fig)

# ==================================================
# RAW DATA
# ==================================================

with st.expander("View Event Data"):

    st.dataframe(
        player_df,
        use_container_width=True
    )
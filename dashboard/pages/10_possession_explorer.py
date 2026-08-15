import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from mplsoccer import Pitch
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch
from utils.data_loader import load_parquet

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Possession Explorer",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ Possession Explorer")

# =====================================================
# LOAD DATA
# =====================================================



sequence = load_parquet(
    "event_sequence/sequence_events.parquet"
)

matches = load_parquet(
    "match_analysis/match_summary.parquet"
)
# =====================================================
# MATCH SELECTOR
# =====================================================

matches["match_label"] = (
    matches["home_team"]
    + " vs "
    + matches["away_team"]
    + " | "
    + matches["match_date"].astype(str)
)

selected_label = st.selectbox(
    "Select Match",
    matches["match_label"]
)

match = matches[
    matches["match_label"] == selected_label
].iloc[0]

match_id = match["match_id"]

home_team = match["home_team"]
away_team = match["away_team"]

# =====================================================
# MATCH DATA
# =====================================================

match_sequence = sequence[
    sequence["match_id"] == match_id
].copy()

# =====================================================
# POSSESSION SELECTOR
# =====================================================

possession_summary = (
    match_sequence.groupby("possession")
    .agg(
        possession_owner=("possession_owner", "first"),
        possession_outcome=("possession_outcome", "first"),
        start_minute=("minute", "min"),
        end_minute=("minute", "max"),
        events=("event_id", "count")
    )
    .reset_index()
)

possession_summary["label"] = (
    possession_summary["possession"].astype(str)
    + " | "
    + possession_summary["possession_owner"]
    + " | "
    + possession_summary["possession_outcome"]
)

selected_possession = st.selectbox(
    "Select Possession",
    possession_summary["label"]
)

possession_id = int(
    selected_possession.split("|")[0].strip()
)

possession_df = match_sequence[
    match_sequence["possession"] == possession_id
].copy()

# =====================================================
# POSSESSION INFO
# =====================================================

owner = possession_df[
    "possession_owner"
].iloc[0]

outcome = possession_df[
    "possession_outcome"
].iloc[0]

start_minute = possession_df[
    "minute"
].min()

end_minute = possession_df[
    "minute"
].max()

event_count = len(possession_df)

# =====================================================
# SUMMARY CARDS
# =====================================================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Owner",
    owner
)

c2.metric(
    "Outcome",
    outcome
)

c3.metric(
    "Events",
    event_count
)

c4.metric(
    "Minutes",
    f"{start_minute}-{end_minute}"
)

# =====================================================
# OPTIONS
# =====================================================

st.markdown("---")

c1, c2, c3 = st.columns(3)

show_numbers = c1.checkbox(
    "Show Event Numbers",
    value=True
)

show_names = c2.checkbox(
    "Show Player Names",
    value=False
)

normalize_direction = c3.checkbox(
    "Normalize Direction",
    value=True
)

# =====================================================
# NORMALIZE ATTACKING DIRECTION
# =====================================================

if normalize_direction:

    if owner == away_team:

        possession_df["location_x"] = (
            120 - possession_df["location_x"]
        )

        possession_df["location_y"] = (
            80 - possession_df["location_y"]
        )

        possession_df["end_location_x"] = (
            120 - possession_df["end_location_x"]
        )

        possession_df["end_location_y"] = (
            80 - possession_df["end_location_y"]
        )

# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3 = st.tabs(
    [
        "Pitch View",
        "Timeline",
        "Raw Events"
    ]
)

# =====================================================
# PITCH TAB
# =====================================================

with tab1:

    pitch = Pitch(
        pitch_type="statsbomb",
        pitch_color="white",
        line_color="black"
    )

    fig, ax = pitch.draw(
        figsize=(14, 9)
    )

    # ============================================
    # DRAW EVENTS
    # ============================================

    for idx, row in possession_df.iterrows():

        event = str(
            row["event_type_name"]
        )

        detail = str(
            row["event_detail"]
        )

        x = row["location_x"]
        y = row["location_y"]

        end_x = row["end_location_x"]
        end_y = row["end_location_y"]

        # ----------------------------------------
        # PASS
        # ----------------------------------------

        if event == "Pass":

            if pd.isna(end_x):
                continue

            length = row["pass_length"]

            height = str(
                row["pass_height_name"]
            )

            color = "royalblue"
            linewidth = 2
            linestyle = "-"

            curve = 0

            if length > 30:

                color = "navy"
                linewidth = 3
                curve = 0.25

            if length > 45:

                curve = 0.40

            if height == "High Pass":

                linestyle = "--"

            arrow = FancyArrowPatch(
                (x, y),
                (end_x, end_y),
                arrowstyle="->",
                mutation_scale=12,
                linewidth=linewidth,
                color=color,
                linestyle=linestyle,
                connectionstyle=f"arc3,rad={curve}"
            )

            ax.add_patch(arrow)

        # ----------------------------------------
        # CARRY
        # ----------------------------------------

        elif event == "Carry":

            if pd.isna(end_x):
                continue

            ax.arrow(
                x,
                y,
                end_x - x,
                end_y - y,
                color="orange",
                width=0.15,
                alpha=0.8,
                length_includes_head=True
            )

        # ----------------------------------------
        # DRIBBLE
        # ----------------------------------------

        elif event == "Dribble":

            pitch.scatter(
                x,
                y,
                color="purple",
                s=120,
                marker="D",
                ax=ax
            )

        # ----------------------------------------
        # BALL RECOVERY
        # ----------------------------------------

        elif event == "Ball Recovery":

            pitch.scatter(
                x,
                y,
                color="green",
                s=150,
                marker="o",
                ax=ax
            )

        # ----------------------------------------
        # INTERCEPTION
        # ----------------------------------------

        elif event == "Interception":

            pitch.scatter(
                x,
                y,
                color="black",
                s=150,
                marker="X",
                ax=ax
            )
        # ----------------------------------------
        # CLEARANCE
        # ----------------------------------------

        elif event == "Clearance":

            pitch.scatter(
                x,
                y,
                color="brown",
                s=180,
                marker="^",
                ax=ax
            )

        # ----------------------------------------
        # GOALKEEPER EVENTS
        # ----------------------------------------

        elif event == "Goal Keeper":

            pitch.scatter(
                x,
                y,
                color="cyan",
                s=180,
                marker="s",
                ax=ax
            )

        # ----------------------------------------
        # SHOTS
        # ----------------------------------------

        elif event == "Shot":

            if "Goal" in detail:

                color = "green"
                marker = "*"
                size = 400

            elif "Saved" in detail:

                color = "red"
                marker = "o"
                size = 220

            elif "Post" in detail:

                color = "orange"
                marker = "P"
                size = 260

            elif "Blocked" in detail:

                color = "darkred"
                marker = "X"
                size = 220

            else:

                color = "gray"
                marker = "o"
                size = 180

            pitch.scatter(
                x,
                y,
                color=color,
                s=size,
                marker=marker,
                edgecolors="black",
                linewidths=1,
                ax=ax
            )

            if not pd.isna(end_x):

                ax.arrow(
                    x,
                    y,
                    end_x - x,
                    end_y - y,
                    color=color,
                    width=0.12,
                    alpha=0.8,
                    length_includes_head=True
                )

        # ----------------------------------------
        # PRESSURE
        # ----------------------------------------

        elif event == "Pressure":

            pitch.scatter(
                x,
                y,
                color="magenta",
                s=80,
                marker="+",
                ax=ax
            )

        # ----------------------------------------
        # BLOCK
        # ----------------------------------------

        elif event == "Block":

            pitch.scatter(
                x,
                y,
                color="darkred",
                s=120,
                marker="X",
                ax=ax
            )

        # ----------------------------------------
        # MISCONTROL
        # ----------------------------------------

        elif event == "Miscontrol":

            pitch.scatter(
                x,
                y,
                color="red",
                s=120,
                marker="v",
                ax=ax
            )

        # ----------------------------------------
        # DISPOSSESSED
        # ----------------------------------------

        elif event == "Dispossessed":

            pitch.scatter(
                x,
                y,
                color="red",
                s=120,
                marker="D",
                ax=ax
            )

        # ----------------------------------------
        # EVENT NUMBERING
        # ----------------------------------------

        if show_numbers:

            ax.text(
                x,
                y,
                str(
                    possession_df.index.get_loc(idx) + 1
                ),
                fontsize=8,
                fontweight="bold",
                color="black",
                ha="center",
                va="center"
            )

        # ----------------------------------------
        # PLAYER LABELS
        # ----------------------------------------

        if show_names:

            if pd.notna(
                row["player_name"]
            ):

                ax.text(
                    x + 1,
                    y + 1,
                    row["player_name"],
                    fontsize=7
                )

    # ============================================
    # TITLE
    # ============================================

    ax.set_title(
        f"{owner} Possession #{possession_id}\nOutcome: {outcome}",
        fontsize=16,
        fontweight="bold"
    )

    # ============================================
    # LEGEND
    # ============================================

    legend_elements = [

        Line2D(
            [0],
            [0],
            color="royalblue",
            lw=2,
            label="Pass"
        ),

        Line2D(
            [0],
            [0],
            color="navy",
            lw=3,
            label="Long Pass"
        ),

        Line2D(
            [0],
            [0],
            color="orange",
            lw=3,
            label="Carry"
        ),

        Line2D(
            [0],
            [0],
            marker="D",
            color="w",
            markerfacecolor="purple",
            markersize=10,
            label="Dribble"
        ),

        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor="green",
            markersize=10,
            label="Recovery"
        ),

        Line2D(
            [0],
            [0],
            marker="X",
            color="w",
            markerfacecolor="black",
            markersize=10,
            label="Interception"
        ),

        Line2D(
            [0],
            [0],
            marker="^",
            color="w",
            markerfacecolor="brown",
            markersize=10,
            label="Clearance"
        ),

        Line2D(
            [0],
            [0],
            marker="s",
            color="w",
            markerfacecolor="cyan",
            markersize=10,
            label="Goalkeeper"
        ),

        Line2D(
            [0],
            [0],
            marker="*",
            color="w",
            markerfacecolor="green",
            markersize=12,
            label="Goal"
        ),

        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor="red",
            markersize=10,
            label="Saved Shot"
        ),

        Line2D(
            [0],
            [0],
            marker="P",
            color="w",
            markerfacecolor="orange",
            markersize=10,
            label="Hit Post"
        )

    ]

    ax.legend(
        handles=legend_elements,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.05),
        ncol=4
    )

    st.pyplot(fig)

# =====================================================
# TIMELINE TAB
# =====================================================

with tab2:

    st.subheader(
        "📅 Event Timeline"
    )

    timeline = possession_df[
        [
            "minute",
            "second",
            "team_name",
            "player_name",
            "event_type_name",
            "event_detail"
        ]
    ].copy()

    timeline["time"] = (
        timeline["minute"].astype(str)
        + "' "
        + timeline["second"].astype(str)
        + '"'
    )

    timeline = timeline[
        [
            "time",
            "team_name",
            "player_name",
            "event_type_name",
            "event_detail"
        ]
    ]

    st.dataframe(
        timeline,
        width="stretch",
        hide_index=True
    )

# =====================================================
# RAW EVENTS TAB
# =====================================================

with tab3:

    st.subheader(
        "📄 Raw Event Data"
    )

    st.dataframe(
        possession_df,
        width="stretch",
        hide_index=True
    )
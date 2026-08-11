import streamlit as st
import pandas as pd
import plotly.express as px
from mplsoccer import Pitch
# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Match Analysis",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ Match Analysis Dashboard")

# ==================================================
# LOAD DATA
# ==================================================

matches = pd.read_csv(
    "reports/csv/match_analysis/match_summary.csv"
)

lineups = pd.read_csv(
    "reports/csv/match_analysis/match_lineups.csv"
)

events = pd.read_csv(
    "reports/csv/match_analysis/match_events.csv"
)

shots = pd.read_csv(
    "reports/csv/match_analysis/match_shots.csv"
)

subs = pd.read_csv(
    "reports/csv/match_analysis/substitutions.csv"
)

cards = pd.read_csv(
    "reports/csv/match_analysis/cards.csv"
)

goalkeepers = pd.read_csv(
    "reports/csv/match_analysis/goalkeeper_events.csv"
)
formation = pd.read_csv(
    "reports/csv/match_analysis/player_position.csv"
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

match = matches[
    matches["match_label"] == selected_match
].iloc[0]

match_id = match["match_id"]

# ==================================================
# FILTER DATA
# ==================================================

match_lineups = lineups[
    lineups["match_id"] == match_id
]

match_events = events[
    events["match_id"] == match_id
]

match_shots = shots[
    shots["match_id"] == match_id
]

match_subs = subs[
    subs["match_id"] == match_id
]

match_cards = cards[
    cards["match_id"] == match_id
]

match_gk = goalkeepers[
    goalkeepers["match_id"] == match_id
]

# ==================================================
# MATCH HEADER
# ==================================================

st.markdown("---")

col1, col2, col3 = st.columns([3, 2, 3])

with col1:
    st.subheader(match["home_team"])

with col2:
    st.metric(
        "Score",
        f'{match["home_score"]} - {match["away_score"]}'
    )

with col3:
    st.subheader(match["away_team"])

st.write(
    f"Week {match['match_week']} | {match['match_date']} | Kickoff {match['kick_off']}"
)

# ==================================================
# LINEUPS
# ==================================================
position_map = {

    "Goalkeeper": (50, 5),

    "Right Back": (80, 20),
    "Right Center Back": (65, 20),
    "Center Back": (50, 20),
    "Left Center Back": (35, 20),
    "Left Back": (20, 20),

    "Right Wing Back": (85, 30),
    "Left Wing Back": (15, 30),

    "Right Defensive Midfield": (70, 40),
    "Center Defensive Midfield": (50, 40),
    "Left Defensive Midfield": (30, 40),

    "Right Midfield": (80, 55),
    "Right Center Midfield": (65, 55),
    "Center Midfield": (50, 55),
    "Left Center Midfield": (35, 55),
    "Left Midfield": (20, 55),

    "Right Attacking Midfield": (70, 70),
    "Center Attacking Midfield": (50, 70),
    "Left Attacking Midfield": (30, 70),

    "Right Wing": (85, 85),
    "Left Wing": (15, 85),

    "Right Center Forward": (65, 92),
    "Center Forward": (50, 92),
    "Left Center Forward": (35, 92)
}

import plotly.graph_objects as go


def draw_formation(match_id, team_name):

    team_data = formation[
        (formation["match_id"] == match_id)
        &
        (formation["team_name"] == team_name)
    ]

    fig = go.Figure()

    # Pitch outline

    fig.add_shape(
        type="rect",
        x0=0,
        y0=0,
        x1=100,
        y1=100,
        line=dict(width=2)
    )

    # Halfway line

    fig.add_shape(
        type="line",
        x0=0,
        y0=50,
        x1=100,
        y1=50
    )

    # Center circle

    fig.add_shape(
        type="circle",
        x0=40,
        y0=40,
        x1=60,
        y1=60
    )

    # Players

    for _, row in team_data.iterrows():

        pos = row["position_name"]

        if pos not in position_map:
            continue

        x, y = position_map[pos]

        fig.add_trace(
            go.Scatter(
                x=[x],
                y=[y],
                mode="markers+text",
                text=[
                    f"{row['jersey_number']}<br>{row['player_name']}"
                ],
                textposition="bottom center",
                marker=dict(
                    size=22
                ),
                hovertemplate=
                "<b>%{text}</b><extra></extra>"
            )
        )

    fig.update_layout(
        title=f"{team_name} Starting XI",
        height=700,
        showlegend=False,
        xaxis=dict(
            visible=False,
            range=[0, 100]
        ),
        yaxis=dict(
            visible=False,
            range=[0, 100]
        ),
        margin=dict(
            l=10,
            r=10,
            t=50,
            b=10
        )
    )

    return fig
st.markdown("---")
st.subheader("📋 Lineups")

home_team = match["home_team"]
away_team = match["away_team"]
st.markdown("---")
st.subheader("📋 Team Formations")

col1, col2 = st.columns(2)

with col1:

    st.plotly_chart(
        draw_formation(
            match_id,
            home_team
        ),
        use_container_width=True
    )

with col2:

    st.plotly_chart(
        draw_formation(
            match_id,
            away_team
        ),
        use_container_width=True
    )
# ==================================================
# SHOT MAP
# ==================================================

from mplsoccer import Pitch

st.markdown("---")
st.subheader("🎯 Team Shot Map")

shots["match_id"] = pd.to_numeric(
    shots["match_id"],
    errors="coerce"
)

match_shots = shots[
    shots["match_id"] == match_id
].copy()

if match_shots.empty:

    st.warning("No shot data available for this match.")

else:

    match_shots["location_x"] = pd.to_numeric(
        match_shots["location_x"],
        errors="coerce"
    )

    match_shots["location_y"] = pd.to_numeric(
        match_shots["location_y"],
        errors="coerce"
    )

    match_shots["statsbomb_xg"] = pd.to_numeric(
        match_shots["statsbomb_xg"],
        errors="coerce"
    )

    match_shots = match_shots.dropna(
        subset=[
            "location_x",
            "location_y"
        ]
    )

    # ---------------------------------
    # Split Home and Away Teams
    # ---------------------------------

    home_shots = match_shots[
        match_shots["team_name"] == match["home_team"]
    ].copy()

    away_shots = match_shots[
        match_shots["team_name"] == match["away_team"]
    ].copy()

    # ---------------------------------
    # Flip Away Team Coordinates
    # ---------------------------------

    away_shots["location_x"] = (
        120 - away_shots["location_x"]
    )

    away_shots["location_y"] = (
        80 - away_shots["location_y"]
    )

    # ---------------------------------
    # Draw Pitch
    # ---------------------------------

    pitch = Pitch(
        pitch_type="statsbomb",
        pitch_color="white",
        line_color="black"
    )

    fig, ax = pitch.draw(
        figsize=(12, 8)
    )

    # ---------------------------------
    # Home Team Shots
        # ---------------------------------
    # ---------------------------------
    # Outcome Symbols
    # ---------------------------------

    outcome_symbols = {
        "Goal": "*",
        "Saved": "o",
        "Post": "^",
        "Off T": "X",
        "Blocked": "s"
    }

    # ---------------------------------
    # HOME TEAM
    # ---------------------------------

    for outcome in home_shots["shot_outcome_name"].unique():

        temp = home_shots[
            home_shots["shot_outcome_name"] == outcome
        ]

        pitch.scatter(
            temp["location_x"],
            temp["location_y"],
            s=(temp["statsbomb_xg"] * 2500) + 100,
            color="blue",
            marker=outcome_symbols.get(outcome, "o"),
            edgecolors="black",
            linewidth=1,
            alpha=0.8,
            label=f"Home - {outcome}",
            ax=ax
        )

    # ---------------------------------
    # AWAY TEAM
    # ---------------------------------

    for outcome in away_shots["shot_outcome_name"].unique():

        temp = away_shots[
            away_shots["shot_outcome_name"] == outcome
        ]

        pitch.scatter(
            temp["location_x"],
            temp["location_y"],
            s=(temp["statsbomb_xg"] * 2500) + 100,
            color="red",
            marker=outcome_symbols.get(outcome, "o"),
            edgecolors="black",
            linewidth=1,
            alpha=0.8,
            label=f"Away - {outcome}",
            ax=ax
        )
    # ---------------------------------
    # Labels
    # ---------------------------------

    ax.legend(
        loc="upper left",
        fontsize=11
    )

    ax.set_title(
        f"{match['home_team']} {match['home_score']} - {match['away_score']} {match['away_team']}",
        fontsize=16,
        fontweight="bold"
    )

    st.pyplot(fig)

    # ---------------------------------
    # Match Shot Stats
    # ---------------------------------

    st.markdown("### 📊 Shot Summary")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Home Team Shots",
            len(home_shots)
        )

        st.metric(
            "Home Team xG",
            round(
                home_shots["statsbomb_xg"].sum(),
                2
            )
        )

    with col2:

        st.metric(
            "Away Team Shots",
            len(away_shots)
        )

        st.metric(
            "Away Team xG",
            round(
                away_shots["statsbomb_xg"].sum(),
                2
            )
        )
# ==================================================
# SHOT OUTCOMES
# ==================================================

st.markdown("---")
st.subheader("⚽ Shot Outcomes")

shot_summary = (
    match_shots
    .groupby(
        ["team_name", "shot_outcome_name"]
    )
    .size()
    .reset_index(name="count")
)

fig = px.bar(
    shot_summary,
    x="shot_outcome_name",
    y="count",
    color="team_name",
    barmode="group"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==================================================
# XG SUMMARY
# ==================================================

st.markdown("---")
st.subheader("📈 xG Summary")

xg_summary = (
    match_shots
    .groupby("team_name")["statsbomb_xg"]
    .sum()
    .reset_index()
)

fig = px.bar(
    xg_summary,
    x="team_name",
    y="statsbomb_xg",
    title="Total xG"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==================================================
# SUBSTITUTIONS
# ==================================================

st.markdown("---")
st.subheader("🔄 Substitutions")

if not match_subs.empty:

    st.dataframe(
        match_subs.sort_values(
            "minute"
        ),
        use_container_width=True
    )

# ==================================================
# CARDS
# ==================================================

st.markdown("---")
st.subheader("🟨 Cards")

if not match_cards.empty:

    st.dataframe(
        match_cards.sort_values(
            "minute"
        ),
        use_container_width=True
    )

# ==================================================
# GOALKEEPER EVENTS
# ==================================================

st.markdown("---")
st.subheader("🧤 Goalkeeper Events")

if not match_gk.empty:

    st.dataframe(
        match_gk.sort_values(
            "minute"
        ),
        use_container_width=True
    )
#new
# ==================================================
# MATCH TIMELINE
# ==================================================

st.markdown("---")
st.subheader("📅 Match Timeline")

# -----------------------------------
# Build Timeline Dataset
# -----------------------------------

timeline = []

# Goals
for _, row in match_shots.iterrows():

    if row["shot_outcome_name"] == "Goal":

        timeline.append({
            "minute": int(row["minute"]),
            "team": row["team_name"],
            "icon": "⚽",
            "text": f"{row['player_name']} scored"
        })

# Cards
for _, row in match_cards.iterrows():

    if row["card_name"] == "Yellow Card":
        icon = "🟨"

    elif row["card_name"] == "Red Card":
        icon = "🟥"

    elif row["card_name"] == "Second Yellow":
        icon = "🟨🟥"

    else:
        icon = "🟨"

    timeline.append({
        "minute": int(row["minute"]),
        "team": row["team_name"],
        "icon": icon,
        "text": f"{row['card_name']} for {row['player_name']}"
    })

# Substitutions
for _, row in match_subs.iterrows():

    timeline.append({
        "minute": int(row["minute"]),
        "team": row["team_name"],
        "icon": "🔄",
        "text": f"{row['player_on']} in, {row['player_off']} out"
    })

# -----------------------------------
# Create DataFrame
# -----------------------------------

timeline = pd.DataFrame(timeline)

if timeline.empty:

    st.info("No timeline data available.")

else:

    timeline = timeline.sort_values(
        "minute",
        ascending=False
    )

    home_team = match["home_team"]
    away_team = match["away_team"]

    # -----------------------------------
    # CSS
    # -----------------------------------

    st.markdown("""
    <style>

    .timeline-row{
        display:flex;
        justify-content:space-between;
        align-items:center;
        padding-top:8px;
        padding-bottom:8px;
    }

    .timeline-left{
        width:42%;
        text-align:right;
        padding-right:15px;
        font-size:16px;
    }

    .timeline-minute{
        width:16%;
        text-align:center;
        font-weight:bold;
        font-size:18px;
    }

    .timeline-right{
        width:42%;
        text-align:left;
        padding-left:15px;
        font-size:16px;
    }

    </style>
    """, unsafe_allow_html=True)

    # -----------------------------------
    # Render Events
    # -----------------------------------

    col1, col2, col3 = st.columns([4,1,4])
     
    with col2:
        st.markdown(
            "<center><h4>🏁 FT</h4></center>",
            unsafe_allow_html=True
        )

    for _, row in timeline.iterrows():

        col1, col2, col3 = st.columns([4, 1, 4])

        event_text = f"{row['icon']} {row['text']}"

        with col1:

            if row["team"] == home_team:
                st.markdown(event_text)

        with col2:

            st.markdown(
                f"<center><b>{row['minute']}'</b></center>",
                unsafe_allow_html=True
            )

        with col3:

            if row["team"] == away_team:
                st.markdown(event_text)

        st.divider()

    # -----------------------------------
    # Full Time
    # -----------------------------------

    col1, col2, col3 = st.columns([4,1,4])

    with col2:
        st.markdown(
            "<center><h4>🏁 Kick Off</h4></center>",
            unsafe_allow_html=True
        )

# ==================================================
# RAW EVENTS
# ==================================================

st.markdown("---")
st.subheader("📜 All Match Events")

st.dataframe(
    match_events.sort_values(
        ["minute", "second"]
    ),
    use_container_width=True
)
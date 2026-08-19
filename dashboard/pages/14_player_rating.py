import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.data_loader import load_parquet

st.set_page_config(
    page_title="Match Ratings Dashboard",
    layout="wide"
)

st.title("⭐ Match Ratings Dashboard")

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_ratings():
    return load_parquet(
        "match_analysis/match_player_ratings.parquet"
    )


@st.cache_data
def load_formation():
    return load_parquet(
        "match_analysis/player_position.parquet"
    )


@st.cache_data
def load_lineups():
    return load_parquet(
        "match_analysis/match_lineups.parquet"
    )


ratings = load_ratings()
formation = load_formation()
lineups = load_lineups()

# =====================================================
# PREPARE FORMATION DATA
# =====================================================

# =====================================================
# PREPARE FORMATION DATA
# =====================================================

# player_position.parquet already contains:
# match_id, team_name, player_name, jersey_number, position_name

formation = formation.drop_duplicates(
    subset=[
        "match_id",
        "team_name",
        "player_name"
    ]
).copy()

# Add ratings

formation = formation.merge(
    ratings[
        [
            "match_id",
            "player_name",
            "team_name",
            "rating",
            "goals",
            "assists"
        ]
    ],
    on=[
        "match_id",
        "player_name",
        "team_name"
    ],
    how="left"
)

# Fill missing values

formation["rating"] = formation["rating"].fillna(6.3)
formation["goals"] = formation["goals"].fillna(0)
formation["assists"] = formation["assists"].fillna(0)

# =====================================================
# POSITION MAP
# =====================================================

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

# =====================================================
# MATCH SELECTION
# =====================================================

matches = sorted(
    ratings["match_name"].unique()
)

selected_match = st.selectbox(
    "Select Match",
    matches
)

match_df = ratings[
    ratings["match_name"] == selected_match
].copy()

match_id = match_df["match_id"].iloc[0]

home_team = match_df["home_team"].iloc[0]
away_team = match_df["away_team"].iloc[0]

# =====================================================
# PLAYER OF THE MATCH
# =====================================================

motm = match_df.loc[
    match_df["rating"].idxmax()
]

st.subheader("⭐ Player of the Match")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Player",
    motm["player_name"]
)

c2.metric(
    "Rating",
    round(motm["rating"], 2)
)

c3.metric(
    "Goals",
    int(motm["goals"])
)

c4.metric(
    "Assists",
    int(motm["assists"])
)

st.markdown("---")

# =====================================================
# FORMATION FUNCTION
# =====================================================

def draw_formation(match_id, team_name):

    team_data = formation[
        (formation["match_id"] == match_id)
        &
        (formation["team_name"] == team_name)
    ]

    fig = go.Figure()

    # Pitch

    fig.add_shape(
        type="rect",
        x0=0,
        y0=0,
        x1=100,
        y1=100,
        line=dict(width=2)
    )

    fig.add_shape(
        type="line",
        x0=0,
        y0=50,
        x1=100,
        y1=50
    )

    fig.add_shape(
        type="circle",
        x0=40,
        y0=40,
        x1=60,
        y1=60
    )

    for _, row in team_data.iterrows():

        pos = row["position_name"]

        if pos not in position_map:
            continue

        x, y = position_map[pos]

        rating = row["rating"]

        if pd.isna(rating):
            rating = 6.0

        if rating >= 8:
            color = "#2ecc71"
        elif rating >= 7:
            color = "#3498db"
        elif rating >= 6:
            color = "#f1c40f"
        else:
            color = "#e74c3c"

        fig.add_trace(
            go.Scatter(
                x=[x],
                y=[y],
                mode="markers+text",
                text=[
                    (
                        f"#{row['jersey_number']}"
                        f"<br>{row['player_name']}"
                        f"<br>⭐ {rating:.1f}"
                    )
                ],
                textposition="bottom center",
                marker=dict(
                    size=30,
                    color=color,
                    line=dict(
                        color="white",
                        width=2
                    )
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


# =====================================================
# TEAM FORMATIONS
# =====================================================

st.subheader("📋 Team Formations")

col1, col2 = st.columns(2)

with col1:

    st.plotly_chart(
        draw_formation(
            match_id,
            home_team
        ),
        width ='stretch'
    )

with col2:

    st.plotly_chart(
        draw_formation(
            match_id,
            away_team
        ),
        width ='stretch'
    )

st.markdown("---")


# =====================================================
# PLAYER OF THE MATCH STATS
# =====================================================

st.subheader("⭐ Player of the Match Statistics")

motm_stats = motm[
    [
        "goals",
        "assists",
        "shots",
        "total_xg",
        "pass_accuracy",
        "interceptions",
        "recoveries",
        "blocks",
        "clearances",
        "goalkeeper_actions",
        "yellow_cards",
        "red_cards",
        "rating"
    ]
]

st.dataframe(
    motm_stats.to_frame().T,
    width ='stretch'
)

st.markdown("---")


# =====================================================
# TEAM SELECTOR
# =====================================================

teams = sorted(
    match_df["team_name"].unique()
)

selected_team = st.selectbox(
    "Select Team",
    teams
)

team_df = match_df[
    match_df["team_name"] == selected_team
].copy()

st.markdown("---")


# =====================================================
# SUBSTITUTES
# =====================================================

st.subheader("🔄 Substitutes")

subs = team_df[
    team_df["minutes_played"] < 45
]

if len(subs) > 0:

    st.dataframe(
        subs[
            [
                "player_name",
                "minutes_played",
                "goals",
                "assists",
                "shots",
                "pass_accuracy",
                "rating"
            ]
        ]
        .sort_values(
            "rating",
            ascending=False
        ),
        width ='stretch'
    )

else:

    st.info(
        "No substitutes found."
    )

st.markdown("---")


# =====================================================
# TEAM SUMMARY
# =====================================================

st.subheader("📊 Team Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Goals",
    int(team_df["goals"].sum())
)

c2.metric(
    "Assists",
    int(team_df["assists"].sum())
)

c3.metric(
    "Avg Rating",
    round(team_df["rating"].mean(), 2)
)

c4.metric(
    "Players",
    len(team_df)
)

st.markdown("---")


# =====================================================
# FULL PLAYER RATINGS
# =====================================================

st.subheader("📋 Full Player Ratings")

ratings_table = team_df[
    [
        "player_name",
        "minutes_played",
        "goals",
        "assists",
        "shots",
        "total_xg",
        "pass_accuracy",
        "interceptions",
        "recoveries",
        "blocks",
        "clearances",
        "yellow_cards",
        "red_cards",
        "rating"
    ]
]

st.dataframe(
    ratings_table.sort_values(
        "rating",
        ascending=False
    ),
    width ='stretch'
)

st.markdown("---")


# =====================================================
# TOP 5 PLAYERS IN MATCH
# =====================================================

st.subheader("🏆 Top 5 Rated Players")

top_players = (
    match_df
    .sort_values(
        "rating",
        ascending=False
    )
    .head(5)
)

st.dataframe(
    top_players[
        [
            "player_name",
            "team_name",
            "goals",
            "assists",
            "pass_accuracy",
            "rating"
        ]
    ],
    width ='stretch'
)
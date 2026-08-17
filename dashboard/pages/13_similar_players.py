import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

from utils.data_loader import load_parquet

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="Player Similarity",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Player Similarity Model")

# --------------------------------------------------
# Load Data
# --------------------------------------------------

@st.cache_data
def load_data():

    return load_parquet(
        "parquet/player_comparison_dataset.parquet"
    )

df = load_data()

# --------------------------------------------------
# Features
# --------------------------------------------------

FEATURES = [
    "goals",
    "assists",
    "shots",
    "pass_accuracy",
    "key_passes",
    "defensive_actions_per_match",
    "cards_per_match",
    "total_xg",
    "finishing_efficiency"
]

# --------------------------------------------------
# Prepare Model
# --------------------------------------------------

X = df[FEATURES].fillna(0)

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

model = NearestNeighbors(
    n_neighbors=11,
    metric="cosine"
)

model.fit(X_scaled)

# --------------------------------------------------
# Player Selector
# --------------------------------------------------

selected_player = st.selectbox(
    "Select Player",
    sorted(df["player_name"].unique())
)

# --------------------------------------------------
# Find Similar Players
# --------------------------------------------------

player_idx = df[
    df["player_name"] == selected_player
].index[0]

distances, indices = model.kneighbors(
    [X_scaled[player_idx]]
)

similar_players = df.iloc[
    indices[0]
].copy()

similar_players["similarity_score"] = (
    1 - distances[0]
) * 100

similar_players = similar_players.iloc[1:]

# --------------------------------------------------
# Top Similar Players
# --------------------------------------------------

st.subheader(
    f"Players Similar To {selected_player}"
)

display_df = similar_players[
    [
        "player_name",
        "similarity_score"
    ]
].copy()

display_df["similarity_score"] = (
    display_df["similarity_score"]
    .round(2)
)

st.dataframe(
    display_df,
    width="stretch"
)

# --------------------------------------------------
# Best Match
# --------------------------------------------------

best_match = similar_players.iloc[0]

st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Selected Player",
        selected_player
    )

with col2:

    st.metric(
        "Most Similar Player",
        best_match["player_name"]
    )

# --------------------------------------------------
# Feature Comparison
# --------------------------------------------------

st.markdown("---")
st.subheader("📊 Statistical Comparison")

player_stats = df[
    df["player_name"] == selected_player
]

compare_stats = df[
    df["player_name"] == best_match["player_name"]
]

comparison = pd.DataFrame({
    "Metric": FEATURES,
    selected_player: player_stats[
        FEATURES
    ].values[0],
    best_match["player_name"]: compare_stats[
        FEATURES
    ].values[0]
})

st.dataframe(
    comparison,
    width="stretch"
)

# --------------------------------------------------
# Radar Chart
# --------------------------------------------------

st.markdown("---")
st.subheader("🎯 Radar Comparison")

radar_features = FEATURES

player_values = player_stats[
    radar_features
].values.flatten()

similar_values = compare_stats[
    radar_features
].values.flatten()

fig = go.Figure()

fig.add_trace(
    go.Scatterpolar(
        r=player_values,
        theta=radar_features,
        fill="toself",
        name=selected_player
    )
)

fig.add_trace(
    go.Scatterpolar(
        r=similar_values,
        theta=radar_features,
        fill="toself",
        name=best_match["player_name"]
    )
)

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True
        )
    ),
    showlegend=True,
    height=700
)

st.plotly_chart(
    fig,
    width="stretch"
)

# --------------------------------------------------
# Similarity Distribution
# --------------------------------------------------

st.markdown("---")
st.subheader("📈 Similarity Scores")

fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=similar_players["player_name"],
        y=similar_players["similarity_score"]
    )
)

fig.update_layout(
    xaxis_title="Player",
    yaxis_title="Similarity %",
    height=500
)

st.plotly_chart(
    fig,
    width="stretch"
)
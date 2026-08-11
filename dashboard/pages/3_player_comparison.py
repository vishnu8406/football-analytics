from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

BASE_DIR = Path(__file__).resolve().parents[2]

@st.cache_data
def load_player_master():
    return pd.read_csv(
        "https://huggingface.co/datasets/Maiyarasu/football_analytics/resolve/main/csv/player_master.csv"
    )

df = load_player_master()

st.title("⚔️ Player Comparison")

players = sorted(df["player_name"].dropna().unique())

col1, col2 = st.columns(2)

with col1:
    player1 = st.selectbox(
        "Select Player 1",
        players,
        index=0
    )

with col2:
    player2 = st.selectbox(
        "Select Player 2",
        players,
        index=1
    )

p1 = df[df["player_name"] == player1].iloc[0]
p2 = df[df["player_name"] == player2].iloc[0]

metrics = [
    "goals",
    "assists",
    "pass_accuracy",
    "key_passes",
    "total_xg",
    "total_defensive_actions"
]

comparison_df = pd.DataFrame({
    "Metric": metrics,
    player1: [p1[m] for m in metrics],
    player2: [p2[m] for m in metrics]
})

st.subheader("Statistical Comparison")

st.dataframe(
    comparison_df,
    use_container_width=True
)

fig = go.Figure()

fig.add_trace(
    go.Bar(
        name=player1,
        x=metrics,
        y=[p1[m] for m in metrics]
    )
)

fig.add_trace(
    go.Bar(
        name=player2,
        x=metrics,
        y=[p2[m] for m in metrics]
    )
)

fig.update_layout(
    barmode="group",
    title="Player Comparison",
    xaxis_title="Metrics",
    yaxis_title="Value"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

radar_metrics = [
    "goals",
    "assists",
    "pass_accuracy",
    "key_passes",
    "total_xg",
    "total_defensive_actions"
]

fig = go.Figure()

fig.add_trace(
    go.Scatterpolar(
        r=[p1[m] for m in radar_metrics],
        theta=radar_metrics,
        fill="toself",
        name=player1
    )
)

fig.add_trace(
    go.Scatterpolar(
        r=[p2[m] for m in radar_metrics],
        theta=radar_metrics,
        fill="toself",
        name=player2
    )
)

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True
        )
    ),
    title="Radar Comparison"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
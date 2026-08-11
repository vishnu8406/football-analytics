import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="Player Radar Analysis",
    page_icon="📡",
    layout="wide"
)

st.title("📡 Player Radar Dashboard")

# --------------------------------------------------
# Load Data
# --------------------------------------------------

@st.cache_data
def load_player_radar():
    return pd.read_csv(
        "https://huggingface.co/datasets/Maiyarasu/football_analytics/resolve/main/csv/player_radar_dataset.csv"
    )

radar = load_player_radar()

# --------------------------------------------------
# Player Selection
# --------------------------------------------------

player = st.selectbox(
    "Select Player",
    sorted(radar["player_name"].unique())
)

player_data = radar[
    radar["player_name"] == player
].iloc[0]

# --------------------------------------------------
# Radar Metrics
# --------------------------------------------------

metrics = [
    "goals",
    "assists",
    "pass_accuracy",
    "key_passes_per_match",
    "defensive_actions_per_match",
    "finishing_efficiency"
]

labels = [
    "Goals",
    "Assists",
    "Pass Accuracy",
    "Key Passes",
    "Def Actions",
    "Finishing"
]

# --------------------------------------------------
# Calculate Percentiles
# --------------------------------------------------

values = []

for metric in metrics:

    percentile = (
        radar[metric]
        .rank(pct=True)
        .loc[player_data.name]
        * 100
    )

    values.append(round(percentile, 2))

# Close radar shape

values.append(values[0])
labels.append(labels[0])

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Goals",
        int(player_data["goals"])
    )

with col2:
    st.metric(
        "Assists",
        int(player_data["assists"])
    )

with col3:
    st.metric(
        "Pass Accuracy %",
        round(player_data["pass_accuracy"], 2)
    )

with col4:
    st.metric(
        "Finishing Efficiency %",
        round(player_data["finishing_efficiency"], 2)
    )

# --------------------------------------------------
# Radar Chart
# --------------------------------------------------

st.markdown("---")
st.subheader("Player Performance Radar")

fig = go.Figure()

fig.add_trace(
    go.Scatterpolar(
        r=values,
        theta=labels,
        fill="toself",
        name=player
    )
)

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 100]
        )
    ),
    showlegend=False,
    height=700
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# Percentile Rankings
# --------------------------------------------------

st.markdown("---")
st.subheader("Percentile Rankings")

percentile_df = pd.DataFrame({
    "Metric": [
        "Goals",
        "Assists",
        "Pass Accuracy",
        "Key Passes / Match",
        "Defensive Actions / Match",
        "Finishing Efficiency"
    ],
    "Percentile": values[:-1]
})

st.dataframe(
    percentile_df,
    use_container_width=True
)

# --------------------------------------------------
# Raw Statistics
# --------------------------------------------------

st.markdown("---")
st.subheader("Player Statistics")

stats = pd.DataFrame({
    "Statistic": [
        "Goals",
        "Assists",
        "Shots",
        "Pass Accuracy",
        "Key Passes",
        "Long Passes",
        "Tackles Won",
        "Interceptions",
        "Recoveries",
        "Clearances",
        "Blocks",
        "xG",
        "Goals - xG",
        "Finishing Efficiency"
    ],
    "Value": [
        player_data["goals"],
        player_data["assists"],
        player_data["shots"],
        round(player_data["pass_accuracy"], 2),
        player_data["key_passes"],
        player_data["long_passes"],
        player_data["tackles_won"],
        player_data["interceptions"],
        player_data["recoveries"],
        player_data["clearances"],
        player_data["blocks"],
        round(player_data["total_xg"], 2),
        round(player_data["goals_minus_xg"], 2),
        round(player_data["finishing_efficiency"], 2)
    ]
})

st.dataframe(
    stats,
    use_container_width=True
)

# --------------------------------------------------
# Top Radar Players
# --------------------------------------------------

st.markdown("---")
st.subheader("Top Players by Finishing Efficiency")

top_players = radar.sort_values(
    "finishing_efficiency",
    ascending=False
).head(15)

st.dataframe(
    top_players[
        [
            "player_name",
            "goals",
            "assists",
            "total_xg",
            "finishing_efficiency"
        ]
    ],
    use_container_width=True
)
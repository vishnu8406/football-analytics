import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="Player Analysis",
    page_icon="👤",
    layout="wide"
)

st.title("👤 Player Analysis Dashboard")

# --------------------------------------------------
# Load Data
# --------------------------------------------------


@st.cache_data
def load_player_data():

    attacking = pd.read_csv(
        "https://huggingface.co/datasets/Maiyarasu/football_analytics/resolve/main/csv/player_attacking.csv"
    )

    passing = pd.read_csv(
        "https://huggingface.co/datasets/Maiyarasu/football_analytics/resolve/main/csv/player_passes.csv"
    )

    creative = pd.read_csv(
        "https://huggingface.co/datasets/Maiyarasu/football_analytics/resolve/main/csv/player_creative.csv"
    )

    defensive = pd.read_csv(
        "https://huggingface.co/datasets/Maiyarasu/football_analytics/resolve/main/csv/player_defensive.csv"
    )

    discipline = pd.read_csv(
        "https://huggingface.co/datasets/Maiyarasu/football_analytics/resolve/main/csv/player_discipline.csv"
    )

    xg = pd.read_csv(
        "https://huggingface.co/datasets/Maiyarasu/football_analytics/resolve/main/csv/player_xG.csv"
    )

    heatmap = pd.read_csv(
        "https://huggingface.co/datasets/Maiyarasu/football_analytics/resolve/main/csv/player_heatmap.csv"
    )

    return (
        attacking,
        passing,
        creative,
        defensive,
        discipline,
        xg,
        heatmap
    )


(
    attacking,
    passing,
    creative,
    defensive,
    discipline,
    xg,
    heatmap
) = load_player_data()
# --------------------------------------------------
# Master Dataset
# --------------------------------------------------

players = attacking.copy()


players = players.merge(
    passing[
        [
            "player_name",
            "passes_per_match",
            "key_passes",
            "long_passes"
        ]
    ],
    on="player_name",
    how="left"
)

players = players.merge(
    creative[
        [
            "player_name",
            "key_passes_per_match",
            "assists_per_match",
            "assist_conversion_percentage"
        ]
    ],
    on="player_name",
    how="left"
)

players = players.merge(
    defensive[
        [
            "player_name",
            "tackles_won",
            "interceptions",
            "recoveries",
            "clearances",
            "blocks",
            "total_defensive_actions"
        ]
    ],
    on="player_name",
    how="left"
)

players = players.merge(
    discipline[
        [
            "player_name",
            "total_fouls",
            "yellow_cards",
            "red_cards",
            "total_cards"
        ]
    ],
    on="player_name",
    how="left"
)

players = players.merge(
    xg[
        [
            "player_name",
            "total_xg",
            "goals_minus_xg",
            "finishing_efficiency"
        ]
    ],
    on="player_name",
    how="left"
)

# --------------------------------------------------
# Player Selector
# --------------------------------------------------

player = st.selectbox(
    "Select Player",
    sorted(players["player_name"].unique())
)

player_data = players[
    players["player_name"] == player
].iloc[0]
player_data = player_data.fillna(0)
# --------------------------------------------------
# KPI Section
# --------------------------------------------------

st.subheader(player)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Goals",
    int(player_data["goals"])
)

col2.metric(
    "Assists",
    int(player_data["assists"])
)

col3.metric(
    "Pass Accuracy %",
    round(player_data["pass_accuracy"], 2)
)

col4.metric(
    "xG",
    round(player_data["total_xg"], 2)
)

# --------------------------------------------------
# Second KPI Row
# --------------------------------------------------

col5, col6, col7, col8 = st.columns(4)

col5.metric(
    "Shots",
    int(player_data["shots"])
)

col6.metric(
    "Key Passes",
    int(player_data["key_passes"])
)

col7.metric(
    "Defensive Actions",
    int(player_data["total_defensive_actions"])
)

col8.metric(
    "Cards",
    int(player_data["total_cards"])
)

# --------------------------------------------------
# Attacking Analysis
# --------------------------------------------------

st.markdown("---")
st.subheader("⚽ Attacking Analysis")

attacking_df = pd.DataFrame({
    "Metric": ["Goals", "Assists", "Shots"],
    "Value": [
        player_data["goals"],
        player_data["assists"],
        player_data["shots"]
    ]
})

fig = px.bar(
    attacking_df,
    x="Metric",
    y="Value",
    title="Attacking Statistics"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Passing Analysis
# --------------------------------------------------

st.markdown("---")
st.subheader("🎯 Passing Analysis")

passing_df = pd.DataFrame({
    "Metric": [
        "Pass Accuracy",
        "Key Passes",
        "Long Passes"
    ],
    "Value": [
        player_data["pass_accuracy"],
        player_data["key_passes"],
        player_data["long_passes"]
    ]
})

fig = px.bar(
    passing_df,
    x="Metric",
    y="Value",
    title="Passing Statistics"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Creativity Analysis
# --------------------------------------------------

st.markdown("---")
st.subheader("🧠 Creativity Analysis")

creative_df = pd.DataFrame({
    "Metric": [
        "Key Passes",
        "Assists",
        "Assist Conversion %"
    ],
    "Value": [
        player_data["key_passes"],
        player_data["assists"],
        player_data["assist_conversion_percentage"]
    ]
})

fig = px.bar(
    creative_df,
    x="Metric",
    y="Value",
    title="Creativity Statistics"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Defensive Analysis
# --------------------------------------------------

st.markdown("---")
st.subheader("🛡️ Defensive Analysis")

defensive_df = pd.DataFrame({
    "Metric": [
        "Tackles",
        "Interceptions",
        "Recoveries",
        "Clearances",
        "Blocks"
    ],
    "Value": [
        player_data["tackles_won"],
        player_data["interceptions"],
        player_data["recoveries"],
        player_data["clearances"],
        player_data["blocks"]
    ]
})

fig = px.bar(
    defensive_df,
    x="Metric",
    y="Value",
    title="Defensive Statistics"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Discipline Analysis
# --------------------------------------------------

st.markdown("---")
st.subheader("🟨 Discipline Analysis")

discipline_df = pd.DataFrame({
    "Metric": [
        "Fouls",
        "Yellow Cards",
        "Red Cards"
    ],
    "Value": [
        player_data["total_fouls"],
        player_data["yellow_cards"],
        player_data["red_cards"]
    ]
})

fig = px.bar(
    discipline_df,
    x="Metric",
    y="Value",
    title="Disciplinary Record"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# xG Analysis
# --------------------------------------------------

st.markdown("---")
st.subheader("📈 xG Analysis")

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Goals - xG",
        round(player_data["goals_minus_xg"], 2)
    )

    st.metric(
        "Finishing Efficiency %",
        round(player_data["finishing_efficiency"], 2)
    )

with col2:

    fig = px.scatter(
        xg,
        x="total_xg",
        y="goals",
        hover_name="player_name",
        title="Goals vs xG"
    )

    fig.add_vline(
        x=player_data["total_xg"]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# Top Players Table
# --------------------------------------------------

st.markdown("---")
st.subheader("🏅 Top Goal Scorers")

top_goals = players.sort_values(
    "goals",
    ascending=False
).head(15)

st.dataframe(
    top_goals[
        [
            "player_name",
            "goals",
            "assists",
            "total_xg"
        ]
    ],
    use_container_width=True
)
st.markdown("---")
st.subheader("🔥 Player Position Heatmap")

player_heat = heatmap[
    heatmap["player_name"] == player
]

if len(player_heat) > 0:

    fig = go.Figure()

    fig.add_trace(
        go.Histogram2dContour(
            x=player_heat["location_x"],
            y=player_heat["location_y"],
            colorscale="Hot",
            reversescale=False,
            showscale=True
        )
    )

    fig.update_layout(
        title=f"{player} Activity Zones",
        xaxis=dict(
            range=[0,120],
            showgrid=False
        ),
        yaxis=dict(
            range=[0,80],
            showgrid=False
        ),
        height=600
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:
    st.warning("No heatmap data available.")
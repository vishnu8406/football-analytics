import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="xG Analysis",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Expected Goals (xG) Analysis")

# =====================================
# LOAD DATA
# =====================================

@st.cache_data
def load_xg():
    return pd.read_csv(
        "https://huggingface.co/datasets/Maiyarasu/football_analytics/resolve/main/csv/player_xG.csv"
    )

xg = load_xg()

xg = xg[xg["total_shots"] >= 10]
# =====================================
# KPI SECTION
# =====================================

total_goals = xg["goals"].sum()
total_xg = xg["total_xg"].sum()

overperformers = (
    xg["goals_minus_xg"] > 0
).sum()

underperformers = (
    xg["goals_minus_xg"] < 0
).sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Goals",
    int(total_goals)
)

col2.metric(
    "Total xG",
    round(total_xg, 2)
)

col3.metric(
    "Overperformers",
    int(overperformers)
)

col4.metric(
    "Underperformers",
    int(underperformers)
)

# =====================================
# GOALS VS XG
# =====================================

st.markdown("---")
st.subheader("⚽ Goals vs xG")

fig = px.scatter(
    xg,
    x="total_xg",
    y="goals",
    hover_name="player_name",
    size="goals",
    title="Goals vs Expected Goals"
)

fig.add_shape(
    type="line",
    x0=0,
    y0=0,
    x1=xg["total_xg"].max(),
    y1=xg["total_xg"].max(),
    line=dict(
        dash="dash"
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================
# TOP XG PLAYERS
# =====================================

st.markdown("---")
st.subheader("🎯 Top xG Players")

top_xg = xg.sort_values(
    "total_xg",
    ascending=False
).head(15)

fig = px.bar(
    top_xg,
    x="player_name",
    y="total_xg",
    title="Top Players by xG"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================
# BEST FINISHERS
# =====================================

st.markdown("---")
st.subheader("🔥 Best Finishers")

best_finishers = xg.sort_values(
    "goals_minus_xg",
    ascending=False
).head(15)

fig = px.bar(
    best_finishers,
    x="player_name",
    y="goals_minus_xg",
    title="Goals - xG"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================
# WORST FINISHERS
# =====================================

st.markdown("---")
st.subheader("❄️ Underperformers")

worst_finishers = xg.sort_values(
    "goals_minus_xg"
).head(15)

fig = px.bar(
    worst_finishers,
    x="player_name",
    y="goals_minus_xg",
    title="Players Below Expected Goals"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================
# FINISHING EFFICIENCY
# =====================================

st.markdown("---")
st.subheader("🏹 Finishing Efficiency")

efficiency = xg.sort_values(
    "finishing_efficiency",
    ascending=False
).head(15)

fig = px.bar(
    efficiency,
    x="player_name",
    y="finishing_efficiency",
    title="Finishing Efficiency (%)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================
# PLAYER EXPLORER
# =====================================

st.markdown("---")
st.subheader("🔍 Player Explorer")

player = st.selectbox(
    "Select Player",
    sorted(
        xg["player_name"].unique()
    )
)

player_data = xg[
    xg["player_name"] == player
].iloc[0]

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Goals",
    int(player_data["goals"])
)

c2.metric(
    "xG",
    round(player_data["total_xg"], 2)
)

c3.metric(
    "Goals - xG",
    round(player_data["goals_minus_xg"], 2)
)

c4.metric(
    "Efficiency %",
    round(
        player_data["finishing_efficiency"],
        2
    )
)

st.dataframe(
    player_data.to_frame().T,
    use_container_width=True
)
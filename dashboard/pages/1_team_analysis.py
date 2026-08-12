import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------
# Page Config
# -----------------------------------

st.set_page_config(
    page_title="Team Analysis",
    page_icon="🏆",
    layout="wide"
)

st.title("🏆 Team Performance Analysis")

# -----------------------------------
# Load Data
# -----------------------------------

@st.cache_data
def load_team_performance():
    return pd.read_csv(
        "https://huggingface.co/datasets/Maiyarasu/football_analytics/resolve/main/csv/team_analysis/overall_performance.csv"
    )

df = load_team_performance()

# -----------------------------------
# Team Selector
# -----------------------------------

team = st.selectbox(
    "Select Team",
    sorted(df["team_name"].unique())
)

team_data = df[df["team_name"] == team].iloc[0]

# -----------------------------------
# KPI Section
# -----------------------------------

st.subheader(f"{team} Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Points",
    int(team_data["points"])
)

col2.metric(
    "Matches",
    int(team_data["matches_played"])
)

col3.metric(
    "Win %",
    f"{team_data['win_percentage']:.2f}%"
)

col4.metric(
    "PPM",
    f"{team_data['points_per_match']:.2f}"
)

# -----------------------------------
# Second KPI Row
# -----------------------------------

col5, col6, col7, col8 = st.columns(4)

col5.metric(
    "Wins",
    int(team_data["total_wins"])
)

col6.metric(
    "Draws",
    int(team_data["total_draws"])
)

col7.metric(
    "Losses",
    int(team_data["total_losses"])
)

col8.metric(
    "Goal Difference",
    int(team_data["goal_difference"])
)

# -----------------------------------
# Goals Analysis
# -----------------------------------

st.markdown("---")
st.subheader("⚽ Goals Analysis")

col1, col2 = st.columns(2)

with col1:

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=["Goals For", "Goals Against"],
            y=[
                team_data["goals_for"],
                team_data["goals_against"]
            ]
        )
    )

    fig.update_layout(
        title="Goals Scored vs Conceded"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

# -----------------------------------
# Result Distribution
# -----------------------------------

with col2:

    result_df = pd.DataFrame({
        "Result": ["Wins", "Draws", "Losses"],
        "Count": [
            team_data["total_wins"],
            team_data["total_draws"],
            team_data["total_losses"]
        ]
    })

    fig = px.pie(
        result_df,
        names="Result",
        values="Count",
        title="Match Results Distribution"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

# -----------------------------------
# League Table
# -----------------------------------

st.markdown("---")
st.subheader("📊 League Standings")

league_table = (
    df.sort_values(
        "points",
        ascending=False
    )
    .reset_index(drop=True)
)

league_table.index += 1

st.dataframe(
    league_table,
    width="stretch"
)

# -----------------------------------
# Top Teams By Points
# -----------------------------------

st.markdown("---")
st.subheader("🏅 Top Teams By Points")

top_points = df.sort_values(
    "points",
    ascending=False
)

fig = px.bar(
    top_points,
    x="team_name",
    y="points",
    title="Points Comparison"
)

st.plotly_chart(
    fig,
    width="stretch"
)

# -----------------------------------
# Goal Difference Ranking
# -----------------------------------

st.markdown("---")
st.subheader("📈 Goal Difference Ranking")

goal_diff = df.sort_values(
    "goal_difference",
    ascending=False
)

fig = px.bar(
    goal_diff,
    x="team_name",
    y="goal_difference",
    title="Goal Difference"
)

st.plotly_chart(
    fig,
    width="stretch"
)

# -----------------------------------
# Team Comparison
# -----------------------------------

st.markdown("---")
st.subheader("⚔️ Team Comparison")

team2 = st.selectbox(
    "Compare With",
    sorted(df["team_name"].unique()),
    index=1
)

compare_df = df[
    df["team_name"].isin([team, team2])
]

comparison_metrics = [
    "points",
    "goals_for",
    "goals_against",
    "goal_difference"
]

fig = go.Figure()

for metric in comparison_metrics:

    fig.add_trace(
        go.Bar(
            name=metric.replace("_", " ").title(),
            x=compare_df["team_name"],
            y=compare_df[metric]
        )
    )

fig.update_layout(
    barmode="group",
    title="Team Comparison"
)

st.plotly_chart(
    fig,
    width="stretch"
)
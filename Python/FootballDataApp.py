import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Jalkapallo tilastoja", page_icon="⚽️", layout="wide")

st.title(":soccer: Football data from 1872-2024")

fl = st.file_uploader(":file_folder: Upload a file", type=(["csv","txt","xlsx","xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(fl, encoding="UTF-8")
else:
    os.chdir(r"C:\rojekti\Data")
    df = pd.read_csv("results.csv", encoding="UTF-8")

#Päivämäärän valinta
col1, col2 = st.columns((2))

try:
    df["date"] = pd.to_datetime(df["date"])
except Exception as e:
    st.error(f"Error converting date column: {e}")

#virhe tässä??
startDate = df["date"].min()
endDate = df["date"].max()


print(startDate)
print(endDate)
print(df["date"][0])
start=str(startDate)
print(start[:10])

with col1:
    date1 = st.date_input("Start Date", startDate)

with col2:
    date2 = st.date_input("End Date", endDate)

try:
    df = df[(df["date"] >= date1) & (df["date"] <= date2)].copy()
except Exception as e:
    st.error(f"Error filtering data by date: {e}")

# ja tässä??
st.sidebar.header("Choose your filter: ")

selected_tournament = st.sidebar.selectbox("Select Tournament:", df["tournament"].unique())
tournament_df = df[df["tournament"] == selected_tournament]

home_team = st.sidebar.multiselect("Pick the Home Team:", df["home_team"].unique())

away_team = st.sidebar.multiselect("Pick the Away Team:", df["away_team"].unique())

if not home_team and not away_team:
    filtered_df = df
else:
    filtered_df = df[df["home_team"].isin(home_team) & df["away_team"].isin(away_team)]


home_team_summary = filtered_df.groupby("home_team").size().reset_index(name="matches")
home_team_summary = home_team_summary.sort_values(by="matches", ascending=False)

away_team_summary = filtered_df.groupby("away_team").size().reset_index(name="matches")
away_team_summary = away_team_summary.sort_values(by="matches", ascending=False)

tournament_summary = filtered_df.groupby("tournament").size().reset_index(name="matches")
tournament_summary = tournament_summary.sort_values(by="matches", ascending=True)


with col1:
    st.subheader("Matches by Home Team")
    fig = px.bar(home_team_summary, x="matches", y="home_team", orientation="h", text="matches", labels={"home_team": "Home team"})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Matches by Away Team")
    fig = px.bar(away_team_summary, x="matches", y="away_team", orientation="h", text="matches", labels={"away_team": "Away team"})
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Matches by Tournament")
    fig = px.bar(tournament_summary, x="matches", y="tournament", orientation="h", text="matches", labels={"tournament": "Tournament"})
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)


home_team_summary = tournament_df.groupby("home_team").size().reset_index(name="matches")
home_team_summary = home_team_summary.sort_values(by="matches", ascending=True)

away_team_summary = tournament_df.groupby("away_team").size().reset_index(name="matches")
away_team_summary = away_team_summary.sort_values(by="matches", ascending=True)

tournament_summary = tournament_df.groupby("tournament").size().reset_index(name="matches")
tournament_summary = tournament_summary.sort_values(by="matches", ascending=True)

#goals scored by home team
home_goals_summary = tournament_df.groupby("home_team")["home_score"].sum().reset_index(name="goals_scored")

#goals scored by away team
away_goals_summary = tournament_df.groupby("away_team")["away_score"].sum().reset_index(name="goals_scored")

# Merge home and away goals summaries
goals_summary = pd.merge(home_goals_summary, away_goals_summary, how="outer", left_on="home_team", right_on="away_team")

# Fill NaN values with 0
goals_summary = goals_summary.fillna(0)

# Add total goals column
goals_summary["total_goals_scored"] = goals_summary["goals_scored_x"] + goals_summary["goals_scored_y"]

# Filter data for the selected tournament
tournament_goals_data = goals_summary

with col1:
    st.subheader("Total Matches in")
    fig = px.bar(home_team_summary, x="matches", y="home_team", orientation="h", text="matches", labels={"home_team": "Team"},  title=f"Total Matches in {selected_tournament}")
    st.plotly_chart(fig, use_container_width=True)


with col2:
    st.subheader("Total Matches Played in Selected Tournament")
    fig = px.bar(tournament_summary, x="matches", y="tournament", orientation="h", text="matches", labels={"tournament": "Tournament"})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Goals Scored in Tournament")
    fig = px.bar(tournament_goals_data, x="home_team", y="total_goals_scored",
                 labels={"total_goals_scored": "Total Goals Score"},
                 title=f"Total Goals Scored by Each Team in {selected_tournament}",
                 color_discrete_sequence=['green'])
    fig.update_traces(texttemplate='', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)


csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button('Download Filtered Data', data=csv, file_name="Filtered_FootballData.csv", mime="text/csv")

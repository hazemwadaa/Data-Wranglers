
import streamlit as st
import pandas as pd
import plotly.express as px


df = pd.read_excel(r"C:\Users\d\Desktop\security_data_300_rows.xlsx")


st.title("🚨 Security Intelligence Dashboard")

st.subheader("📊 Raw Data")
st.dataframe(df)

st.sidebar.header("Filter Data")

location = st.sidebar.selectbox("Select Location", df["Location"].unique())
incident = st.sidebar.selectbox("Select Incident Type", df["Incident_Type"].unique())

filtered_df = df[(df["Location"] == location) & (df["Incident_Type"] == incident)]

st.subheader("Filtered Data")
st.write(filtered_df)

df["DateTime"] = pd.to_datetime(df["Date"] + " " + df["Time"])
df["Hour"] = df["DateTime"].dt.hour


st.subheader("⏰ Crime by Hour")
fig1 = px.histogram(df, x="Hour", title="Incidents by Hour")
st.plotly_chart(fig1)


st.subheader("📌 Incident Types")
fig2 = px.pie(df, names="Incident_Type")
st.plotly_chart(fig2)


st.subheader("📍 Top Locations")
top_locations = df["Location"].value_counts()
st.bar_chart(top_locations)


st.subheader("📊 Key Metrics")
st.write("Total Incidents:", len(df))
st.write("High Risk Cases:", len(df[df["Severity"] == "High"]))

peak_hour = df["Hour"].value_counts().idxmax()
top_location = df["Location"].value_counts().idxmax()

st.write("🔥 Peak Hour:", peak_hour)
st.write("📍 Most Dangerous Location:", top_location)

last_week = df[df["DateTime"] > df["DateTime"].max() - pd.Timedelta(days=7)]
prev_week = df[df["DateTime"] <= df["DateTime"].max() - pd.Timedelta(days=7)]

st.write("Last Week:", len(last_week))
st.write("Previous Week:", len(prev_week))

import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap

m = folium.Map(location=[df["Latitude"].mean(), df["Longitude"].mean()], zoom_start=10)
HeatMap(df[["Latitude", "Longitude"]]).add_to(m)

st_folium(m)

if len(df[df["Severity"] == "High"]) > 50:
    st.error("⚠️ High Risk Alert!")

 
st.download_button("Download Report", data="Report content here", file_name="report.txt")


col1, col2, col3 = st.columns(3)

col1.metric("Total Incidents", len(df))
col2.metric("High Risk", len(df[df["Severity"]=="High"]))
col3.metric("Locations", df["Location"].nunique())

search = st.text_input("Search Location")
df = df[df["Location"].str.contains(search, case=False)]

trend = df.groupby("Date").size()

st.line_chart(trend)



st.subheader("📅 Weekly Report")


last_week_df = df[df["DateTime"] > df["DateTime"].max() - pd.Timedelta(days=7)]

total_week = len(last_week_df)
high_risk_week = len(last_week_df[last_week_df["Severity"] == "High"])

if not last_week_df.empty:
    top_location_week = last_week_df["Location"].value_counts().idxmax()
    peak_hour_week = last_week_df["Hour"].value_counts().idxmax()
else:
    top_location_week = "N/A"
    peak_hour_week = "N/A"


st.write(f"Total Incidents (Last 7 Days): {total_week}")
st.write(f"High Risk Cases: {high_risk_week}")
st.write(f"Top Location: {top_location_week}")
st.write(f"Peak Hour: {peak_hour_week}")


report_text = f"""
Weekly Security Report

Total Incidents: {total_week}
High Risk Cases: {high_risk_week}
Top Location: {top_location_week}
Peak Hour: {peak_hour_week}
"""

st.download_button(
    label="📥 Download Weekly Report",
    data=report_text,
    file_name="weekly_report.txt"
)

# after run the code Write this code in terminal
# python -m streamlit run c:/Users/d/Desktop/project.py

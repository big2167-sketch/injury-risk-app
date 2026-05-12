import sys
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# Allow app.py to import from backend folder
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from backend.data_processing import load_and_process_data

st.set_page_config(
    page_title="NFL Injury Risk Analysis",
    page_icon="🏈",
    layout="wide"
)

st.title("🏈 Injury Risk Analysis in the NFL")

st.write(
    "This app analyzes NFL tracking data to explore high-intensity movement situations "
    "using speed, acceleration, and movement intensity."
)

st.info(
    "Note: This app does not predict confirmed injuries. Since direct injury labels are not included, "
    "movement intensity is used as a proxy for potential injury-risk situations."
)
with st.expander("Project Summary"):
    st.write(
        "Research Question: How can NFL player movement data be used to identify "
        "high-intensity movement situations associated with elevated injury-risk conditions?"
    )

    st.write(
        "This app uses NFL tracking data to analyze player speed, acceleration, "
        "and movement intensity."
    )

    st.write(
        "Movement intensity is used as a proxy because confirmed injury labels "
        "are not included in the dataset."
    )

# Load data
data_path = BASE_DIR / "data" / "tracking_sample.csv"

df, q75, q90 = load_and_process_data(data_path)

# Sidebar filters
st.sidebar.header("Interactive Filters")

speed_options = sorted(df["speed_category"].dropna().unique())
accel_options = sorted(df["accel_category"].dropna().unique())
risk_options = sorted(df["risk_category"].dropna().unique())

selected_speed = st.sidebar.multiselect(
    "Select Speed Category",
    speed_options,
    default=speed_options
)

selected_accel = st.sidebar.multiselect(
    "Select Acceleration Category",
    accel_options,
    default=accel_options
)

selected_risk = st.sidebar.multiselect(
    "Select Risk Category",
    risk_options,
    default=risk_options
    
)
player_options = ["All Players"] + sorted(df["displayName"].dropna().unique())

selected_player = st.sidebar.selectbox(
    "Select Player",
    player_options
)

filtered_df = df[
    df["speed_category"].isin(selected_speed)
    & df["accel_category"].isin(selected_accel)
    & df["risk_category"].isin(selected_risk)

]
if selected_player != "All Players":
    filtered_df = filtered_df[filtered_df["displayName"] == selected_player]

if filtered_df.empty:
    st.warning("No data matches the selected filters. Try selecting more categories.")
    st.stop()

# Summary metrics
st.header("Summary Metrics")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Observations", f"{len(filtered_df):,}")

col2.metric(
    "Unique Players",
    f"{filtered_df['displayName'].nunique():,}"
)

col3.metric(
    "Average Speed",
    f"{filtered_df['speed_mph'].mean():.2f} mph"
)

col4.metric(
    "Max Speed",
    f"{filtered_df['speed_mph'].max():.2f} mph"
)

col5.metric(
    "Average Acceleration",
    f"{filtered_df['a'].mean():.2f}"
)

col6, col7 = st.columns(2)

col6.metric(
    "90th Percentile Speed",
    f"{filtered_df['speed_mph'].quantile(0.90):.2f} mph"
)

col7.metric(
    "90th Percentile Intensity",
    f"{filtered_df['movement_intensity'].quantile(0.90):.2f}"
)

with st.expander("Data Cleaning Notes"):
    st.write("- Football tracking rows were removed because ball speed does not represent player movement.")
    st.write("- Speed was converted from yards/second to miles per hour.")
    st.write("- Player speeds above 25 mph were removed as unrealistic outliers.")
    st.write("- Direct injury labels are not included, so risk is based on movement intensity.")

st.success(
    "Key Takeaway: Most player movement occurs at low speeds, but high-speed and high-acceleration events are important because they represent more intense movement situations."
)

# Visualizations
st.header("Visual Analysis")

left, right = st.columns(2)

with left:
    st.subheader("Player Movement by Speed Category")

    speed_counts = filtered_df["speed_category"].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(8, 5))
    speed_counts.plot(kind="bar", ax=ax)
    ax.set_title("Player Movement by Speed Category")
    ax.set_xlabel("Speed Category")
    ax.set_ylabel("Number of Player Tracking Observations")
    ax.tick_params(axis="x", rotation=20)
    st.pyplot(fig)

with right:
    st.subheader("Player Movement by Acceleration Category")

    accel_counts = filtered_df["accel_category"].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(8, 5))
    accel_counts.plot(kind="bar", ax=ax)
    ax.set_title("Player Movement by Acceleration Category")
    ax.set_xlabel("Acceleration Category")
    ax.set_ylabel("Number of Player Tracking Observations")
    ax.tick_params(axis="x", rotation=20)
    st.pyplot(fig)

left2, right2 = st.columns(2)
with left2:
    st.subheader("Speed vs Acceleration")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(filtered_df["speed_mph"], filtered_df["a"], alpha=0.25)
    ax.set_title("Speed vs Acceleration")
    ax.set_xlabel("Speed (mph)")
    ax.set_ylabel("Acceleration")
    ax.set_ylim(0, 6)
    st.pyplot(fig)

with right2:
    st.subheader("Movement Intensity Risk Categories")

    risk_order = [
        "Normal (Bottom 75%)",
        "Elevated (75–90%)",
        "High Risk Proxy (Top 10%)"
    ]

    risk_counts = filtered_df["risk_category"].value_counts().reindex(risk_order)

    fig, ax = plt.subplots(figsize=(8, 5))
    risk_counts.plot(kind="bar", ax=ax)
    ax.set_title("Movement Intensity Risk Categories")
    ax.set_xlabel("Risk Category")
    ax.set_ylabel("Number of Player Tracking Observations")
    ax.tick_params(axis="x", rotation=20)
    st.pyplot(fig)

st.header("Player Movement Comparison")

top_players = (
    df.groupby("displayName")["movement_intensity"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

fig, ax = plt.subplots(figsize=(9, 5))
top_players.plot(kind="bar", ax=ax)
ax.set_title("Top 10 Players by Average Movement Intensity")
ax.set_xlabel("Player")
ax.set_ylabel("Average Movement Intensity")
ax.tick_params(axis="x", rotation=45)
st.pyplot(fig)

st.caption(
    "This chart compares players based on average movement intensity. "
    "It is not an injury ranking, but it highlights players with more intense movement profiles in the sample."
)

# Movement intensity estimator
st.header("Interactive Movement Intensity Estimator")

st.write(
    "Use the sliders below to test how speed and acceleration affect the movement intensity score. "
    "This tool does not predict confirmed injuries, but it helps identify high-intensity movement situations."
)

st.info(
    "Movement Intensity = Speed (mph) × Acceleration. "
    "This combines how fast a player is moving with how quickly their movement is changing."
)
with st.expander("How to Use This App"):
    st.write("1. Use the sidebar filters to explore speed, acceleration, and risk categories.")
    st.write("2. Review the summary metrics to understand the selected data.")
    st.write("3. Use the charts to compare movement patterns.")
    st.write("4. Test custom speed and acceleration values in the estimator.")

slider_col1, slider_col2 = st.columns(2)

with slider_col1:
    user_speed = st.slider("Player Speed (mph)", 0.0, 25.0, 10.0, 0.5)

with slider_col2:
    user_accel = st.slider("Acceleration", 0.0, 6.0, 1.0, 0.1)

user_intensity = user_speed * user_accel

if user_intensity >= q90:
    risk_level = "High Risk Proxy"
    explanation = "This movement profile falls in the top 10% of movement intensity values."
elif user_intensity >= q75:
    risk_level = "Elevated Risk"
    explanation = "This movement profile falls between the 75th and 90th percentile."
else:
    risk_level = "Normal Risk"
    explanation = "This movement profile falls below the 75th percentile."

st.metric("Movement Intensity Score", f"{user_intensity:.2f}")
st.subheader(f"Estimated Risk Level: {risk_level}")
st.write(explanation)

st.header("Limitations")

st.write("- The app does not include confirmed injury labels.")
st.write("- Movement intensity is a proxy, not a confirmed injury prediction.")
st.write("- Field surface, weather, and stadium conditions are not included yet.")
st.write("- Future versions can merge tracking data with external game and injury datasets.")

# Data preview
st.header("Processed Data Preview")

st.dataframe(
    df[
        [
            "displayName",
            "s",
            "a",
            "speed_mph",
            "speed_category",
            "accel_category",
            "movement_intensity",
            "risk_category"
        ]
    ].head(100)
)

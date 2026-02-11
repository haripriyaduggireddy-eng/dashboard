import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------
# Page configuration
# ----------------------------------
st.set_page_config(
    page_title="NFHS-4 India Dashboard",
    layout="wide"
)

st.title("📊 National Family Health Survey (NFHS-4) Dashboard")
st.markdown("Interactive analysis of NFHS indicators across States, Area and Survey rounds")

# ----------------------------------
# Load Data
# ----------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("All India National Family Health Survey4.xlsx")
    return df

df = load_data()

# ----------------------------------
# Sidebar Filters
# ----------------------------------
st.sidebar.header("🔍 Filters")

state = st.sidebar.selectbox(
    "Select State / UT",
    sorted(df["India/States/UTs"].unique())
)

survey = st.sidebar.selectbox(
    "Select Survey",
    sorted(df["Survey"].unique())
)

area = st.sidebar.selectbox(
    "Select Area",
    sorted(df["Area"].unique())
)

# ----------------------------------
# Filter Data
# ----------------------------------
filtered_df = df[
    (df["India/States/UTs"] == state) &
    (df["Survey"] == survey) &
    (df["Area"] == area)
]

# ----------------------------------
# Indicator Selection
# ----------------------------------
indicator_columns = df.columns[3:]  # Exclude State, Survey, Area

indicator = st.selectbox(
    "📌 Select Indicator",
    indicator_columns
)

# ----------------------------------
# KPI Display
# ----------------------------------
value = filtered_df[indicator].values[0]

st.metric(
    label=indicator,
    value=f"{value}"
)

# ----------------------------------
# Comparison Chart Across States
# ----------------------------------
st.subheader("📈 State-wise Comparison")

compare_df = df[
    (df["Survey"] == survey) &
    (df["Area"] == area)
][["India/States/UTs", indicator]].dropna()

fig = px.bar(
    compare_df,
    x="India/States/UTs",
    y=indicator,
    title=f"{indicator} ({survey} - {area})",
    labels={"India/States/UTs": "State / UT"},
)

fig.update_layout(
    xaxis_tickangle=-45,
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------
# Data Table
# ----------------------------------
st.subheader("📋 Filtered Data View")
st.dataframe(filtered_df, use_container_width=True)

# ----------------------------------
# Download Option
# ----------------------------------
st.download_button(
    label="⬇️ Download Filtered Data",
    data=filtered_df.to_csv(index=False),
    file_name="nfhs_filtered_data.csv",
    mime="text/csv"
)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Toronto Island Ferry Analytics",
    page_icon="⛴️",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data(file):
    df = pd.read_excel(file)

    # Rename columns for consistency
    df.columns = [
        "_id",
        "Timestamp",
        "Redemption_Count",
        "Sales_Count"
    ]

    # Convert datetime
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    # Sort chronologically
    df = df.sort_values("Timestamp")

    # Handle missing values
    df["Sales_Count"] = df["Sales_Count"].fillna(0)
    df["Redemption_Count"] = df["Redemption_Count"].fillna(0)

    # Feature Engineering
    df["Hour"] = df["Timestamp"].dt.hour
    df["Date"] = df["Timestamp"].dt.date
    df["Day_Name"] = df["Timestamp"].dt.day_name()
    df["Month"] = df["Timestamp"].dt.month_name()
    df["Weekday"] = df["Timestamp"].dt.weekday

    df["Weekend_Weekday"] = np.where(
        df["Weekday"] >= 5,
        "Weekend",
        "Weekday"
    )

    # Seasons
    def get_season(month):
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Spring"
        elif month in [6, 7, 8]:
            return "Summer"
        else:
            return "Fall"

    df["Season"] = df["Timestamp"].dt.month.apply(get_season)

    # KPI Metrics
    df["Net_Movement"] = (
        df["Sales_Count"] - df["Redemption_Count"]
    )

    # Rolling Averages
    df["Sales_Rolling_1H"] = (
        df["Sales_Count"]
        .rolling(window=4, min_periods=1)
        .mean()
    )

    df["Sales_Rolling_4H"] = (
        df["Sales_Count"]
        .rolling(window=16, min_periods=1)
        .mean()
    )

    return df


# =========================
# SIDEBAR
# =========================
st.sidebar.title("⛴️ Toronto Island Ferry Analytics")

uploaded_file = st.sidebar.file_uploader(
    "Upload Ferry Ticket Dataset",
    type=["xlsx", "csv"]
)

if uploaded_file is not None:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = load_data(uploaded_file)

        # If uploaded from xlsx already processed
        if "_id" not in df.columns:
            df = load_data(uploaded_file)

    # =========================
    # FILTERS
    # =========================
    st.sidebar.header("Filters")

    min_date = df["Timestamp"].min().date()
    max_date = df["Timestamp"].max().date()

    date_range = st.sidebar.date_input(
        "Select Date Range",
        [min_date, max_date]
    )

    selected_season = st.sidebar.multiselect(
        "Select Season",
        options=df["Season"].unique(),
        default=df["Season"].unique()
    )

    selected_day_type = st.sidebar.multiselect(
        "Weekend / Weekday",
        options=df["Weekend_Weekday"].unique(),
        default=df["Weekend_Weekday"].unique()
    )

    # Filter Data
    filtered_df = df[
        (df["Timestamp"].dt.date >= date_range[0]) &
        (df["Timestamp"].dt.date <= date_range[1]) &
        (df["Season"].isin(selected_season)) &
        (df["Weekend_Weekday"].isin(selected_day_type))
    ]

    # =========================
    # HEADER
    # =========================
    st.title("⛴️ Real-Time Ferry Ticket Sales & Redemption Analytics")
    st.markdown("""
    Analytics Dashboard for Toronto Island Park Ferry Operations
    """)

    # =========================
    # KPI CARDS
    # =========================
    total_sales = int(filtered_df["Sales_Count"].sum())
    total_redemptions = int(filtered_df["Redemption_Count"].sum())
    net_movement = int(filtered_df["Net_Movement"].sum())

    peak_hour = (
        filtered_df.groupby("Hour")["Sales_Count"]
        .sum()
        .idxmax()
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "🎫 Total Tickets Sold",
        f"{total_sales:,}"
    )

    col2.metric(
        "✅ Total Tickets Redeemed",
        f"{total_redemptions:,}"
    )

    col3.metric(
        "📊 Net Passenger Movement",
        f"{net_movement:,}"
    )

    col4.metric(
        "⏰ Peak Demand Hour",
        f"{peak_hour}:00"
    )

    st.markdown("---")

    # =========================
    # TIME SERIES ANALYSIS
    # =========================
    st.subheader("📈 Ticket Sales vs Redemptions Over Time")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=filtered_df["Timestamp"],
            y=filtered_df["Sales_Count"],
            mode="lines",
            name="Sales Count"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=filtered_df["Timestamp"],
            y=filtered_df["Redemption_Count"],
            mode="lines",
            name="Redemption Count"
        )
    )

    fig.update_layout(
        height=500,
        xaxis_title="Timestamp",
        yaxis_title="Count",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)

    # =========================
    # HOURLY DEMAND
    # =========================
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🕒 Hourly Demand Trend")

        hourly = (
            filtered_df.groupby("Hour")[
                ["Sales_Count", "Redemption_Count"]
            ]
            .sum()
            .reset_index()
        )

        fig_hour = px.line(
            hourly,
            x="Hour",
            y=["Sales_Count", "Redemption_Count"],
            markers=True
        )

        fig_hour.update_layout(height=450)

        st.plotly_chart(
            fig_hour,
            use_container_width=True
        )

    # =========================
    # DAILY TREND
    # =========================
    with col2:
        st.subheader("📅 Daily Passenger Trend")

        daily = (
            filtered_df.groupby("Date")[
                ["Sales_Count", "Redemption_Count"]
            ]
            .sum()
            .reset_index()
        )

        fig_daily = px.area(
            daily,
            x="Date",
            y=["Sales_Count", "Redemption_Count"]
        )

        fig_daily.update_layout(height=450)

        st.plotly_chart(
            fig_daily,
            use_container_width=True
        )

    # =========================
    # SEASONAL ANALYSIS
    # =========================
    st.subheader("🌦️ Seasonal Comparison")

    seasonal = (
        filtered_df.groupby("Season")[
            ["Sales_Count", "Redemption_Count"]
        ]
        .sum()
        .reset_index()
    )

    fig_season = px.bar(
        seasonal,
        x="Season",
        y=["Sales_Count", "Redemption_Count"],
        barmode="group"
    )

    st.plotly_chart(
        fig_season,
        use_container_width=True
    )

    # =========================
    # WEEKEND VS WEEKDAY
    # =========================
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📌 Weekend vs Weekday")

        ww = (
            filtered_df.groupby("Weekend_Weekday")[
                ["Sales_Count", "Redemption_Count"]
            ]
            .sum()
            .reset_index()
        )

        fig_ww = px.pie(
            ww,
            names="Weekend_Weekday",
            values="Sales_Count",
            hole=0.4
        )

        st.plotly_chart(
            fig_ww,
            use_container_width=True
        )

    # =========================
    # NET MOVEMENT
    # =========================
    with col2:
        st.subheader("🚶 Net Passenger Movement")

        net_df = (
            filtered_df.groupby("Date")["Net_Movement"]
            .sum()
            .reset_index()
        )

        fig_net = px.bar(
            net_df,
            x="Date",
            y="Net_Movement"
        )

        st.plotly_chart(
            fig_net,
            use_container_width=True
        )

    # =========================
    # ROLLING AVERAGES
    # =========================
    st.subheader("📉 Rolling Average Analysis")

    fig_roll = go.Figure()

    fig_roll.add_trace(
        go.Scatter(
            x=filtered_df["Timestamp"],
            y=filtered_df["Sales_Rolling_1H"],
            mode="lines",
            name="1 Hour Rolling Avg"
        )
    )

    fig_roll.add_trace(
        go.Scatter(
            x=filtered_df["Timestamp"],
            y=filtered_df["Sales_Rolling_4H"],
            mode="lines",
            name="4 Hour Rolling Avg"
        )
    )

    fig_roll.update_layout(
        height=500,
        hovermode="x unified"
    )

    st.plotly_chart(
        fig_roll,
        use_container_width=True
    )

    # =========================
    # PEAK ANALYSIS
    # =========================
    st.subheader("🔥 Peak vs Off-Peak Analysis")

    peak_threshold = (
        filtered_df["Sales_Count"]
        .quantile(0.75)
    )

    filtered_df["Demand_Type"] = np.where(
        filtered_df["Sales_Count"] >= peak_threshold,
        "Peak",
        "Off-Peak"
    )

    peak_summary = (
        filtered_df.groupby("Demand_Type")[
            ["Sales_Count", "Redemption_Count"]
        ]
        .mean()
        .reset_index()
    )

    fig_peak = px.bar(
        peak_summary,
        x="Demand_Type",
        y=["Sales_Count", "Redemption_Count"],
        barmode="group"
    )

    st.plotly_chart(
        fig_peak,
        use_container_width=True
    )

    # =========================
    # DATA TABLE
    # =========================
    st.subheader("📄 Detailed Data Table")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    # =========================
    # INSIGHTS SECTION
    # =========================
    st.subheader("🧠 Operational Insights")

    busiest_day = (
        filtered_df.groupby("Day_Name")["Sales_Count"]
        .sum()
        .idxmax()
    )

    busiest_season = (
        filtered_df.groupby("Season")["Sales_Count"]
        .sum()
        .idxmax()
    )

    st.success(
        f"""
        • Peak demand occurs around {peak_hour}:00 hours.
        
        • Highest passenger traffic observed during {busiest_season}.
        
        • Busiest operational day is {busiest_day}.
        
        • Net passenger movement helps estimate congestion levels.
        
        • Rolling averages indicate sustained traffic trends for scheduling decisions.
        """
    )

else:
    st.title("⛴️ Toronto Island Ferry Analytics Dashboard")

    st.info(
        "Upload the Toronto Island Ferry dataset to begin analysis."
    )

    st.markdown("""
    ### Features Included

    ✅ Real-Time KPI Cards  
    ✅ Interactive Time-Series Analysis  
    ✅ Peak vs Off-Peak Detection  
    ✅ Seasonal Trend Analysis  
    ✅ Rolling Average Analytics  
    ✅ Net Passenger Movement Tracking  
    ✅ Operational Insights  
    """)

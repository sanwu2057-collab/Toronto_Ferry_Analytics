# 🚢 Toronto Island Ferry Analytics Dashboard

A comprehensive real-time analytics dashboard for Toronto Island Park Ferry operations built with Streamlit and Plotly.

## Features

✅ **Real-Time KPI Cards** - Track total tickets sold, redeemed, and net passenger movement  
✅ **Interactive Time-Series Analysis** - Visualize sales vs redemption trends over time  
✅ **Hourly & Daily Demand Trends** - Identify peak demand patterns  
✅ **Seasonal Trend Analysis** - Compare passenger traffic across seasons  
✅ **Rolling Average Analytics** - 1-hour and 4-hour moving averages for trend detection  
✅ **Peak vs Off-Peak Detection** - Segment demand periods with quantile-based analysis  
✅ **Net Passenger Movement Tracking** - Estimate congestion levels  
✅ **Weekend vs Weekday Comparison** - Pie charts showing traffic distribution  
✅ **Operational Insights** - AI-generated recommendations for scheduling and capacity planning  
✅ **Detailed Data Table** - Export and inspect raw data  

## Installation

### Local Development

```bash
# Clone the repository
git clone https://github.com/sanwu2057-collab/Toronto_Ferry_Analytics.git
cd Toronto_Ferry_Analytics

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

### Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"** and connect your GitHub repository
3. Select this repository and specify `app.py` as the entry point
4. Click **Deploy**

## Usage

1. **Upload Dataset**: Use the sidebar to upload your Ferry Ticket Dataset (`.xlsx` or `.csv` format)
2. **Apply Filters**: 
   - Select date range
   - Choose seasons (Winter, Spring, Summer, Fall)
   - Filter by weekend/weekday
3. **Explore Visualizations**: Interact with charts to zoom, pan, and hover for details
4. **Download Data**: Export the detailed data table for further analysis

## Data Format

The dashboard expects data with the following columns:
- `_id`: Record identifier
- `Timestamp`: Date and time of transaction
- `Redemption_Count`: Number of tickets redeemed
- `Sales_Count`: Number of tickets sold

## Dependencies

- **streamlit** - Web app framework
- **pandas** - Data manipulation and analysis
- **numpy** - Numerical computations
- **plotly** - Interactive visualizations
- **openpyxl** - Excel file support

See `requirements.txt` for specific versions.

## Project Structure

```
Toronto_Ferry_Analytics/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Key Metrics

- **Total Tickets Sold** - Cumulative ticket sales in selected period
- **Total Tickets Redeemed** - Cumulative ticket redemptions
- **Net Passenger Movement** - Difference between sales and redemptions (indicator of net flow)
- **Peak Demand Hour** - Hour with highest ticket sales

## Analytics Features

### Seasonal Analysis
Automatically categorizes data into:
- Winter (Dec, Jan, Feb)
- Spring (Mar, Apr, May)
- Summer (Jun, Jul, Aug)
- Fall (Sep, Oct, Nov)

### Demand Segmentation
Peak periods identified at 75th percentile of sales volume for meaningful segmentation.

### Rolling Averages
- **1-Hour Rolling Average**: Short-term trend smoothing (4 periods)
- **4-Hour Rolling Average**: Medium-term trend identification (16 periods)

## Future Enhancements

- Real-time data integration with ferry ticketing systems
- Predictive demand forecasting with ML models
- Weather correlation analysis
- Multi-language support
- Mobile-responsive design
- API endpoint for programmatic access

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or contributions, please create an issue in the GitHub repository.

---

**Built with ❤️ for Toronto Island Ferry Operations**

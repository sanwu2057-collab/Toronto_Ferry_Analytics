import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime

st.set_page_config(
    page_title='Toronto Ferry Executive Dashboard',
    page_icon='⛴️',
    layout='wide'
)

st.title('⛴️ Toronto Island Ferry Executive Analytics Dashboard')
st.caption('Senior Analyst Edition: Passenger Flow & Operational Intelligence')

@st.cache_data
def load_data(file):
    try:
        df=pd.read_excel(file)

        # datetime.time fix
        for col in df.columns:
            if df[col].dtype=='object':
                sample=df[col].dropna().iloc[0] if not df[col].dropna().empty else None
                if isinstance(sample,datetime.time):
                    df[col]=df[col].astype(str)

        # adjust Timestamp column name if needed
        time_col='Timestamp'
        dt=pd.to_datetime(df[time_col],errors='coerce')

        df['Hour']=dt.dt.hour
        df['Date']=dt.dt.date
        df['Day']=dt.dt.day_name()
        df['Month']=dt.dt.month_name()
        df['Time']=dt.dt.strftime('%H:%M:%S')

        # Example metrics
        if 'Sales Count' in df.columns and 'Redemption Count' in df.columns:
            df['Net Movement']=df['Sales Count']-df['Redemption Count']

        return df

    except Exception as e:
        st.error(f'Error: {e}')
        st.stop()

uploaded=st.sidebar.file_uploader('Upload Ferry Dataset',type=['xlsx','csv'])
if uploaded is None:
    st.info('Upload Toronto Island Ferry file')
    st.stop()

df=load_data(uploaded)

locations=st.sidebar.multiselect(
    'Day Filter',
    df['Day'].dropna().unique(),
    default=df['Day'].dropna().unique()
)

f=df[df['Day'].isin(locations)]

sales=f['Sales Count'].sum()
redeem=f['Redemption Count'].sum()
net=f['Net Movement'].sum()
peak=f.groupby('Hour')['Sales Count'].sum().idxmax()

c1,c2,c3,c4=st.columns(4)
c1.metric('Total Sales',f'{sales:,.0f}')
c2.metric('Redemptions',f'{redeem:,.0f}')
c3.metric('Net Passenger Flow',f'{net:,.0f}')
c4.metric('Peak Hour',f'{peak}:00')

left,right=st.columns(2)
with left:
    hr=f.groupby('Hour')['Sales Count'].sum().reset_index()
    st.plotly_chart(px.line(hr,x='Hour',y='Sales Count',markers=True,title='Passenger Demand by Hour'),use_container_width=True)

with right:
    compare=f.groupby('Hour')[['Sales Count','Redemption Count']].sum().reset_index()
    fig=go.Figure()
    fig.add_bar(x=compare['Hour'],y=compare['Sales Count'],name='Sales')
    fig.add_bar(x=compare['Hour'],y=compare['Redemption Count'],name='Redemptions')
    st.plotly_chart(fig,use_container_width=True)

st.subheader('Passenger Flow Heatmap')
heat=f.pivot_table(values='Sales Count',index='Day',columns='Hour',aggfunc='sum')
st.plotly_chart(px.imshow(heat,text_auto=True),use_container_width=True)

st.subheader('Daily Passenger Trend')
daily=f.groupby('Date')[['Sales Count','Redemption Count']].sum().reset_index()
st.plotly_chart(
    px.line(
        daily,
        x='Date',
        y=['Sales Count','Redemption Count'],
        markers=True,
        title='Daily Passenger Movement Trend'
    ),
    use_container_width=True
)

st.subheader('Net Passenger Movement Analysis')
netdf=f.groupby('Hour')['Net Movement'].sum().reset_index()
st.plotly_chart(
    px.area(
        netdf,
        x='Hour',
        y='Net Movement',
        title='Net Passenger Flow by Hour'
    ),
    use_container_width=True
)

st.subheader('Day-wise Demand Distribution')
daydf=f.groupby('Day')['Sales Count'].sum().reset_index()
st.plotly_chart(
    px.bar(
        daydf,
        x='Day',
        y='Sales Count',
        color='Sales Count',
        title='Demand by Day'
    ),
    use_container_width=True
)

st.subheader('Sales Distribution')
st.plotly_chart(
    px.box(
        f,
        y='Sales Count',
        title='Passenger Ticket Distribution'
    ),
    use_container_width=True
)

st.subheader('Operational Insights')
st.success(f'Peak demand occurs around {peak}:00')
st.info('Increase staffing and ferry frequency during peak periods.')
st.warning('Monitor high net movement periods for crowd management.')

st.dataframe(f,use_container_width=True)

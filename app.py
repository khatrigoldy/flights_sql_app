import streamlit as st
from dbhelper import DB
import plotly.graph_objects as go
import plotly.express as px

db = DB()


st.sidebar.title('Flights Analytics')

user_option = st.sidebar.selectbox('Menu',['Select one','Check Flights','Analytics'])

if user_option == 'Check Flights':
    st.title('Check Flights')

    col1,col2 = st.columns(2)

    with col1:
        city = db.fetch_city_name()
        source = st.selectbox('Source',sorted(city))
    with col2:
        city = db.fetch_city_name()
        destination = st.selectbox('Destination', sorted(city))

    if st.button('Search'):
        results = db.fetch_all_flights(source,destination)
        st.dataframe(results)

elif user_option == 'Analytics':
    airline, frequency = db.fetch_airline_frequency()



    # Flatten frequency list
    flat_frequency = [f[0] for f in frequency]



    fig = go.Figure(
        data=[go.Pie(
            labels = airline,
            values =flat_frequency,
            hoverinfo = "label+percent",
            textinfo ="value"
        )]
    )
    st.header("Pie chart")
    st.plotly_chart(fig)

    # city, frequency1 = db.busy_airport()
    #
    # # Flatten frequency list
    # flat_frequency1 = [f[0] for f in frequency1]
    #
    # fig = px.bar(
    #         x=city,
    #         y=flat_frequency1,
    #
    #     )
    # st.header("Bar chart")
    # st.plotly_chart(fig,theme="streamlit",use_container_width= True)

    city, frequency1 = db.busy_airport()
    flat_frequency1 = [f[0] for f in frequency1]

    fig = px.bar(
        x=city,
        y=flat_frequency1,
        labels={'x': 'City', 'y': 'Number of Flights'},
        text=flat_frequency1,  # shows the value on bars
        title=" Number of Flights per City "
    )

    # Customize layout
    fig.update_traces(marker_color='lightskyblue', textposition='outside')
    fig.update_layout(
        xaxis_title="City",
        yaxis_title="Number of Flights",
        title_font_size=20,
        height=600,
        title_x=0.5,  # center align title
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(showgrid=True, gridcolor='lightgrey'),
        xaxis_tickangle=-45  # angle for long city names
    )

    # Streamlit rendering
    st.header("Bar Chart - Busiest Airports")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    date, frequency2 = db.daily_frequency()
    flat_frequency2 = [f[0] for f in frequency2]

    # Create line chart
    fig = px.line(
        x=date,
        y=flat_frequency2,
        labels={'x': 'Date', 'y': 'Number of Flights'},
        title=" Daily Frequency of Flights"
    )

    # Customize appearance
    fig.update_traces(
        line=dict(color='royalblue', width=3),
        mode='lines+markers'
    )

    fig.update_layout(
        height=600,
        xaxis_title="Date",
        yaxis_title="Number of Flights",
        title_font_size=20,
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(showgrid=True, gridcolor='lightgrey'),
        xaxis=dict(showgrid=False, tickangle=-45)
    )

    # Display in Streamlit
    st.header("Line Chart - Daily Flights")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
else:
    st.title('Flight Data Explorer: SQL-Powered Insights on Indian Aviation')
    st.markdown("""
    Welcome to **Flight Data Explorer**, a data-driven project built using **SQL, AWS RDS, PyCharm, and Streamlit**.  
    This application allows users to explore and analyze domestic flight data through interactive visualizations.
    """)
    st.header("🔍 Key Features")
    st.markdown("""
    - **Flight Lookup Tool**: Search available flights between selected origin and destination cities.  
    - **Airline Share Analysis**: A **pie chart** shows the market share of airlines like Air India, Vistara, and others.  
    - **Flights per City**: A **bar chart** visualizes how many flights operate from each city.  
    - **Daily Flight Trends**: A **line chart** displays the frequency of flights on a day-to-day basis.  
    """)
    st.markdown("""
    The backend is powered by **MySQL hosted on AWS RDS**, while the front end is built using **Streamlit**,  
    ensuring a seamless user experience. This project showcases how cloud databases and Python can work together  
    for real-time aviation analytics.
    """)
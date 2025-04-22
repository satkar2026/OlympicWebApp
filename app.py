import streamlit as st
import pandas as pd
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import spicy




df = pd.read_csv(r"C:\Users\sathw\Downloads\archive (12)\athlete_events.csv")
region = pd.read_csv(r"C:\Users\sathw\Downloads\archive (12)\noc_regions.csv")

df = preprocessor.preprocess(df,region)

st.sidebar.title("Olympics Analysis")
st.sidebar.image(r"C:\Users\sathw\Downloads\olympic_rings.png")


st.sidebar.title("Olympics Analysis")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-Wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("select a year",years)
    selected_country = st.sidebar.selectbox("select a country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_country == 'overall' and selected_year == 'overall':
        st.title("Overall Analysis")
    elif selected_country != 'overall' and selected_year == 'overall':
        st.title("medal tally in"+ " "+ str(selected_country) +"  "+ "olympics")
    elif selected_country == 'overall' and selected_year != 'overall':
        st.title(str(selected_year)+ "overall performance")
    elif selected_country != 'overall' and selected_year != 'overall':
        st.title(selected_country+" "+ "performance in "+str(selected_year) + "olympics")
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] -1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("top Statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1,col2,col3 = st.columns(3)

    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Athletes")
        st.title(athletes)
    with col3:
        st.header("Nations")
        st.title(nations)
    nation_over_time = helper.data_over_time(df,'region')
    fig = px.line(nation_over_time, x="Edition", y="region", markers=True)
    st.title("Participating Nations Over The Years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Edition", y="Event", markers=True)
    st.title("Events Over The Years")
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x="Edition", y="Name", markers=True)
    st.title("Athletes Over The Years")
    st.plotly_chart(fig)

    st.title("Number of Events Over The time(Every sport)")
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(["Year", "Sport", "Event"])
    ax = sns.heatmap(x.pivot_table(index="Sport", columns="Year", values="Event", aggfunc='count').fillna(0).astype(int),
                annot=True)
    st.pyplot(fig)

    st.title("Most sucessfull Athletes")
    sport_list= df["Sport"].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,"overall")

    selected_sport = st.selectbox("select a sport",sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)
if user_menu == "Country-Wise Analysis":

    st.title("Country Wise Analysis")
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox("select a country",country_list)

    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x="Year", y="Medal", markers=True)
    st.title(selected_country + "Medal tally Over The Years")
    st.plotly_chart(fig)

    st.title(selected_country + "excels in following sport")
    pt = helper.country_event_heatmap(df,selected_country)
    fig,ax = plt.subplots(figsize=(20,20))
    ax=sns.heatmap(pt,annot=True)
    st.plotly_chart(fig)


    st.title("Top 10 countries"+" "+ selected_country)
    top10_df = helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)

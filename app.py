import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="covid data analysis")

# global functions?
@st.cache
def load_data():
    df = pd.read_csv('covid_19_data.csv')
    return df

def get_indian_data():
    df = load_data()
    df = df[df["Country/Region"] == 'India']
    return df

# page 2 functions
def india_group_date():
    df = get_indian_data()
    df = df.rename(columns={'ObservationDate':'date'})
    df = df.groupby('date', as_index=False).sum()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values('date')
    return df

def get_death():
    df = india_group_date()
    fig = px.line(df, 'date', 'Deaths')
    return fig

def get_recovery():
    df = india_group_date()
    fig = px.line(df, 'date', 'Recovered')
    return fig

def get_confirm():
    df = india_group_date()
    fig = px.line(df, 'date', 'Confirmed')
    return fig

# page 3 functions
def get_world_data():
    df = load_data()
    df = df.rename(columns={'ObservationDate':'date'})
    df = df.groupby('date', as_index=False).sum()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values('date')
    return df

def get_world_death():
    df = get_world_data()
    fig = px.line(df, 'date', 'Deaths')
    return fig

def get_world_recovery():
    df = get_world_data()
    fig = px.line(df, 'date', 'Recovered')
    return fig

def get_world_confirm():
    df = get_world_data()
    fig = px.line(df, 'date', 'Confirmed')
    return fig

# page 4 functions
def get_country():
    df = load_data()
    df = df.rename(columns={'ObservationDate':'date'})
    df['date'] = pd.to_datetime(df.date)
    df = df[df.date == max(df.date)]
    df = df.groupby('Country/Region', as_index=False).sum()
    return df

def get_country_death():
    df = get_country()
    fig = px.bar(df, 'Country/Region', 'Deaths')
    return fig

def get_country_recovery():
    df = get_country()
    fig = px.bar(df, 'Country/Region', 'Recovered')
    return fig

def get_country_confirm():
    df = get_country()
    fig = px.bar(df, 'Country/Region', 'Confirmed')
    return fig

# page 4 functions
def state_wise():
    df = get_indian_data()
    df = df.rename(columns={'ObservationDate':'date'})
    df['date'] = pd.to_datetime(df.date)
    df = df[df.date == max(df.date)]
    return df

def get_state_death():
    df = state_wise()
    fig = px.bar(df, 'Province/State', 'Deaths')
    return fig

def get_state_recovery():
    df = state_wise()
    fig = px.bar(df, 'Province/State', 'Recovered')
    return fig

def get_state_confirm():
    df = state_wise()
    fig = px.bar(df, 'Province/State', 'Confirmed')
    return fig

# page 5 functions
def growth_analysis():
    df = get_world_data()
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=df.date, y=df["Confirmed"],
                        mode='lines+markers',
                        name='Confirmed Cases'))
    fig.add_trace(go.Scatter(x=df.date, y=df["Recovered"],
                        mode='lines+markers',
                        name='Recovered Cases'))
    fig.add_trace(go.Scatter(x=df.date, y=df["Deaths"],
                        mode='lines+markers',
                        name='Death Cases'))
    fig.update_layout(title="Growth of different types of cases",
                     xaxis_title="Date",yaxis_title="Number of Cases",legend=dict(x=0,y=1,traceorder="normal"))
    return fig

def get_mortal_pie():
    df = get_world_data().copy()
    df['Mortality'] = (df.Deaths/df.Confirmed)*100
    fig = px.scatter(df, 'date', 'Mortality')
    return fig

def get_recover_pie():
    df = get_world_data().copy()
    df['Recovery'] = (df.Recovered/df.Confirmed)*100
    fig = px.scatter(df, 'date', 'Recovery')
    return fig

def page1():
    st.title('Covid-19 Data Analysis')
    df = load_data()
    x = 10
    st.header("A slight look of the data")
    st.write("  ")
    st.write(df.head(x))
    st.markdown("<hr>", unsafe_allow_html= True)
    col1, col2 = st.beta_columns(2)
    col1.subheader("Number of Rows:")
    col1.write(df.shape[0])
    col2.subheader("Number of Columns:")
    col2.write(df.shape[1])
    st.markdown("<hr>", unsafe_allow_html= True)

    st.header("Dataset Summary")
    st.write(" ")
    st.write(df.describe())

    st.header("Columns description")
    for i in df.columns:
        st.subheader(i)
        col1, col2 = st.beta_columns(2)
        col1.caption("Unique Values")
        col1.write(len(df[i].unique()))
        col2.caption("Type of Data")
        col2.write("String of Characters" if type(df[i].iloc[0]) is str else "Numerical")
        st.markdown("<hr>",unsafe_allow_html = True)

def page2():
    st.header("Data of India")
    st.plotly_chart(get_death())
    st.plotly_chart(get_recovery())
    st.plotly_chart(get_confirm())

def page3():
    st.header("Data of Whole World")
    st.plotly_chart(get_world_death())
    st.plotly_chart(get_world_recovery())
    st.plotly_chart(get_world_confirm())

def page4():
    st.header("Country wise Analysis")
    st.plotly_chart(get_country_death())
    st.plotly_chart(get_country_recovery())
    st.plotly_chart(get_country_confirm())

def page5():
    st.header("State wise Analysis")
    st.plotly_chart(get_state_death())
    st.plotly_chart(get_state_recovery())
    st.plotly_chart(get_state_confirm())

def page6():
    st.header("Date wise analysis")
    st.plotly_chart(growth_analysis())
    st.plotly_chart(get_mortal_pie())
    st.plotly_chart(get_recover_pie())

pages = {
    'Home' : page1,
    'India Total' : page2,
    'World Total' : page3,
    'Country Wise Analysis' : page4,
    'State Wise Analysis of India' : page5,
    'Datewise Analysis' : page6
    }

st.sidebar.title("covid-19 data analysis")
choice = st.sidebar.selectbox('Choose a page', list(pages.keys()))

pages[choice]()
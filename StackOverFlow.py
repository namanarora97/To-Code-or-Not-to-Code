# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 15:28:43 2022

@author: somya
"""

import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

 
@st.experimental_singleton
def load_data():
    #df = pd.read_csv("Crimes_2021_1.csv")
    df= pd.read_csv("InitialClean.csv")
    #salary_category = ["Low(<10,000)", "Low-Med(10k-49k)","Medium(49k-85k)", "High(85k-150k)","Very High(150<)"]
    
    # Drop all unused columns[TBD]
    drop_col =['CurrencySymbol','Respondent']
    #df.drop(drop_col)
    return df

#1. Introduction: Title& Header

alt.data_transformers.enable('default', max_rows = None)

#st.title("Interactive Data Science")
st.title("Factors that makes a programmer successful")
st.subheader("Team Zebra")

st.write("This dataset contains responses of 100,000 respondents who reported information ranging from their excercise habits to compensative levels")


#2. Data Loading

with st.spinner(text="Loading data..."):
    df = load_data()
    st.text("Visualize the overall dataset and some distributions here...")
    if st.checkbox('Show Table'):
        st.write(df.head(20))
        st.write(len(df))
        

#3. Graph1: Demographics

def clean_gender_col(gender):
    if gender not in ['Male','Female']:
        return 'LGBTQ+'
    else:
        return gender
df['Gender'] = df['Gender'].apply(clean_gender_col)

dict = {'Extremely dissatisfied':'01 Extremely dissatisfied',
       'Moderately dissatisfied':'02 Moderately dissatisfied',
       'Slightly dissatisfied':'03 Slightly  dissatisfied',
       'Neither satisfied nor dissatisfied':'04 Neither satisfied nor dissatisfied',
       'Slightly satisfied':'05 Slightly satisfied',
       'Moderately satisfied':'06 Moderately satisfied',
       'Extremely satisfied':'07 Extremely satisfied'}

df.replace({"JobSatisfaction": dict},inplace=True)
df.replace({"CareerSatisfaction": dict},inplace=True)

# TODO: Add Graph Description
st.header("Does Salary impacts your Career and Job satisfaction")
st.write(""" Insight: """)

# define dropdown
columns = ['JobSatisfaction','CareerSatisfaction']

select_box = alt.binding_select(options=columns, name='column')
sel = alt.selection_single(fields=['column'], bind=select_box, init={'column': 'JobSatisfaction'})


demo = alt.Chart(df[:10000]).properties(width = 700,height = 700).transform_fold(
    columns,
    as_=['column', 'value']
).transform_filter(
    sel  
).mark_point().encode(
    alt.X('ConvertedSalary:Q',scale=alt.Scale(domain=(0, 2000000))),
    y = 'count():N',
    color = 'value:N',
    tooltip = 'value:N',
).configure_mark(
    opacity=0.8,
).add_selection(
    sel
).interactive()
st.altair_chart(demo)


        

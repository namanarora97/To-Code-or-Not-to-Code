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
    df= pd.read_csv("https://metashady.blob.core.windows.net/public/InitialClean.csv")
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

#Personal Habits visualization


dict2 = {'''I don't typically exercise''':'''01 I don't typically exercise''',
       '1 - 2 times per week':'02 1 - 2 times per week',
       '3 - 4 times per week':'03 3 - 4 times per week',
       'Daily or almost every day':'04 Daily or almost every day'}

dict3 = {'Never':'01 Never',
       '1 - 2 times per week':'02 1 - 2 times per week',
       '3 - 4 times per week':'03 3 - 4 times per week',
       'Daily or almost every day':'04 Daily or almost every day'}

dict4 = {'Before 5:00 AM':'01 Before 5:00 AM',
       'Between 5:00 - 6:00 AM':'02 Between 5:00 - 6:00 AM',
       'Between 6:01 - 7:00 AM':'03 Between 6:01 - 7:00 AM',
       'Between 7:01 - 8:00 AM':'04 Between 7:01 - 8:00 AM',
       'Between 8:01 - 9:00 AM':'05 Between 8:01 - 9:00 AM',
       'Between 9:01 - 10:00 AM':'04 Between 9:01 - 10:00 AM',
       'Between 10:01 - 11:00 AM':'05 Between 10:01 - 11:00 AM',
       'Between 11:01 AM - 12:00 PM':'06 Between 11:01 AM - 12:00 PM',
       'After 12:01 PM':'07 After 12:01 PM',
       'I do not have a set schedule':'08 I do not have a set schedule',
       'I work night shifts':'09 I work night shifts'}
dict5 = {'Less than 1 hour':'01 Less than 1 hour',
       '1 - 4 hours':'02 1 - 4 hours',
       '5 - 8 hours':'03 5 - 8 hours',
       '9 - 12 hours':'04 9 - 12 hours',
       'Over 12 hours':'05 Over 12 hours'}

df.replace({"Exercise": dict2},inplace=True)
df.replace({"SkipMeals": dict3},inplace=True)
df.replace({"WakeTime": dict4},inplace=True)
df.replace({"HoursComputer": dict5},inplace=True)
#df.replace({"CareerSatisfaction": dict},inplace=True)

columns1=['Exercise', 'SkipMeals','WakeTime','HoursComputer']
df1 = df.dropna(subset=columns1, how='any')
input_dropdown = alt.binding_select(options=columns1, name="Select habit ")
picked = alt.selection_single(fields=["Select habit"], bind=input_dropdown,init={'Select habit': 'Exercise'})

hist = alt.Chart(df1[:10000]).transform_fold(columns1, as_= ['Select habit','value']).transform_filter(picked).mark_bar( color= 'Green', opacity=0.7).encode(
    alt.X("value:N",sort= "ascending"), 
    alt.Y("median(ConvertedSalary)"), 
    opacity='count(value):Q',
   
   tooltip = [alt.Tooltip('median(ConvertedSalary):N')
              ]
    
    ).add_selection(picked).properties(width=800,height=500)


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
    #alt.X('ConvertedSalary:Q',scale=alt.Scale(domain=(0, 2000000))),
    alt.X('FormalEducation'),
    alt.Y("median(ConvertedSalary)"), 
    color = 'value:N',
    tooltip = 'value:N',
).configure_mark(
    opacity=0.8,
).add_selection(
    sel
).interactive()
st.altair_chart(demo)
st.altair_chart(hist)


        

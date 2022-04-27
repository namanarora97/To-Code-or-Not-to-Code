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
@st.cache
def load_data():
    # df = pd.read_csv("Crimes_2021_1.csv")
    # df= pd.read_csv("https://metashady.blob.core.windows.net/public/InitialClean.csv")
    df = pd.read_csv(
        "https://metashady.blob.core.windows.net/public/InitialClean_NF.csv"
    )
    # salary_category = ["Low(<10,000)", "Low-Med(10k-49k)","Medium(49k-85k)", "High(85k-150k)","Very High(150<)"]

    # Drop all unused columns[TBD]
    drop_col = ["CurrencySymbol", "Respondent"]
    # df.drop(drop_col)
    return df


#################################################
# taken and modified from the interactivity lab
@st.cache
def get_slice_membership(df, genders, sexualOrientation, races, educations, age_range):
    """
    Implement a function that computes which rows of the given dataframe should
    be part of the slice, and returns a boolean pandas Series that indicates 0
    if the row is not part of the slice, and 1 if it is part of the slice.

    In the example provided, we assume genders is a list of selected strings
    (e.g. ['Male', 'Transgender']). We then filter the labels based on which
    rows have a value for gender that is contained in this list. You can extend
    this approach to the other variables based on how they are returned from
    their respective Streamlit components.
    """
    labels = pd.Series([1] * len(df), index=df.index)
    if genders:
        labels &= df["Gender2"].isin(genders)
    if sexualOrientation:
        labels &= df["SexualOrientation2"].isin(sexualOrientation)
    if races:
        labels &= df["RaceEthnicity2"].isin(races)
    if educations:
        labels &= df["FormalEducation"].isin(educations)
    if age_range:
        labels &= df["Age"].isin(age_range)
    # ... complete this function for the other demographic variables
    return labels


@st.cache
def get_new_df_4(df):
    pass


#################################################


# 1. Introduction: Title& Header

alt.data_transformers.enable("default", max_rows=None)

# st.title("Interactive Data Science")
st.title("To Code or Not to Code?")
st.subheader("Team Zebra")

st.write(
    "This dataset contains responses of 98,885 respondents who reported information ranging from their excercise habits to compensative levels"
)


# 2. Data Loading

with st.spinner(text="Loading data..."):
    df = load_data()
    st.text("Visualize the overall dataset and some distributions here...")
    if st.checkbox("Show Table"):
        st.write(df.head(20))
        st.write(len(df))


# 3. Graph1: Demographics


def clean_gender_col(gender):
    if gender not in ["Male", "Female"]:
        return "LGBTQ+"
    else:
        return gender


df["Gender"] = df["Gender"].apply(clean_gender_col)

dict = {
    "Extremely dissatisfied": "01 Extremely dissatisfied",
    "Moderately dissatisfied": "02 Moderately dissatisfied",
    "Slightly dissatisfied": "03 Slightly  dissatisfied",
    "Neither satisfied nor dissatisfied": "04 Neither satisfied nor dissatisfied",
    "Slightly satisfied": "05 Slightly satisfied",
    "Moderately satisfied": "06 Moderately satisfied",
    "Extremely satisfied": "07 Extremely satisfied",
}


# Personal Habits visualization
# Exercising
dict2 = {
    """I don't typically exercise""": """01 I don't typically exercise""",
    "1 - 2 times per week": "02 1 - 2 times per week",
    "3 - 4 times per week": "03 3 - 4 times per week",
    "Daily or almost every day": "04 Daily or almost every day",
}

# Skip Meal
dict3 = {
    "Never": "01 Never",
    "1 - 2 times per week": "02 1 - 2 times per week",
    "3 - 4 times per week": "03 3 - 4 times per week",
    "Daily or almost every day": "04 Daily or almost every day",
}

# Wake up time
dict4 = {
    "Before 5:00 AM": "01 Before 5:00 AM",
    "Between 5:00 - 6:00 AM": "02 Between 5:00 - 6:00 AM",
    "Between 6:01 - 7:00 AM": "03 Between 6:01 - 7:00 AM",
    "Between 7:01 - 8:00 AM": "04 Between 7:01 - 8:00 AM",
    "Between 8:01 - 9:00 AM": "05 Between 8:01 - 9:00 AM",
    "Between 9:01 - 10:00 AM": "06 Between 9:01 - 10:00 AM",
    "Between 10:01 - 11:00 AM": "07 Between 10:01 - 11:00 AM",
    "Between 11:01 AM - 12:00 PM": "08 Between 11:01 AM - 12:00 PM",
    "After 12:01 PM": "09 After 12:01 PM",
    "I do not have a set schedule": "10 I do not have a set schedule",
    "I work night shifts": "11 I work night shifts",
}

# Hours on Computer
dict5 = {
    "Less than 1 hour": "01 Less than 1 hour",
    "1 - 4 hours": "02 1 - 4 hours",
    "5 - 8 hours": "03 5 - 8 hours",
    "9 - 12 hours": "04 9 - 12 hours",
    "Over 12 hours": "05 Over 12 hours",
}

df["JobSatisfactionQuant"] = df["JobSatisfactionQuant"].fillna(0)

columns1 = ["Exercise", "SkipMeals", "WakeTime", "HoursComputer"]
df1 = df.dropna(subset=columns1, how="any")
input_dropdown = alt.binding_select(options=columns1, name="Habit")
picked = alt.selection_single(
    fields=["Habit"], bind=input_dropdown, init={"Habit": "Exercise"}
)

all_habits = [
    habit
    for habit in list(dict2.keys())
    + list(dict3.keys())
    + list(dict4.keys())
    + list(dict5.keys())
]

hist = (
    alt.Chart(df1.sample(10000, random_state=42))
    .transform_fold(columns1, as_=["Habit", "value"])
    .transform_filter(picked)
    .mark_bar(color="Green", opacity=0.9)
    .encode(
        alt.Y("value:N", sort=all_habits, title=("Chosen Value"),),
        alt.X("median(ConvertedSalary)", title="Median Salary in USD/year"),
        color=alt.Color(
            "mean(JobSatisfactionQuant):Q",
            legend=alt.Legend(title="Mean Job Satisfaction"),
        ),
        tooltip=[
            alt.Tooltip("mean(ConvertedSalary):Q", title="Mean Salary in USD/year"),
            alt.Tooltip("mean(JobSatisfactionQuant):Q", title="Mean Job Satisfaction"),
            alt.Tooltip('count(value):Q',title="Count of records")
        ],
    )
    .add_selection(picked)
    .properties(width=800, height=500)
)


# define dropdown
st.header("Predict Job satisfaction according to your country and Salary")

st.subheader("Slider")
slider = st.slider(label="Salary", min_value=0, max_value=200000, step=1000, value=5000)
st.write("Slider Value: ", slider)

country_selectbox = st.selectbox("Country", df["Country"].unique())
st.write("Dropdown Value: ", country_selectbox)

new_df = df[~df["JobSatisfaction"].isna()]
new_df = new_df[~new_df["CareerSatisfaction"].isna()]

new_df_2 = new_df[(new_df["Country"] == country_selectbox)]

new_df_2["distance"] = (new_df_2["ConvertedSalary"] - slider) ** 2
new_df_2["rank"] = new_df_2["distance"].rank(method="first")
new_df_3 = new_df_2[new_df_2["rank"] <= 10]

new_df_4 = new_df_3["JobSatisfaction"].value_counts(normalize=True).reset_index()
new_df_4.columns = ["JobSatisfaction", "Proportion"]
new_df_4 = new_df_4.sort_values(by="Proportion", ascending=False).reset_index(drop=True)

js_all = new_df[["JobSatisfaction"]].drop_duplicates()

prediction = new_df_4["JobSatisfaction"].values[0][3:]

new_df_4 = pd.merge(new_df_4, js_all, on="JobSatisfaction", how="right").fillna(0)

# st.write(new_df_2['JobSatisfaction'].value_counts(normalize = True))


mychart = (
    alt.Chart(new_df_4)
    .mark_bar(color="red", width=30)
    .encode(alt.X("JobSatisfaction"), alt.Y("Proportion"), tooltip="Proportion")
    .properties(width=500, height=500)
)

st.write(mychart)

st.subheader(
    "You are most likely to be: "
    + prediction
    + " with the chosen salary of "
    + str(slider)
    + " in "
    + country_selectbox
)


st.altair_chart(hist)

###########################################
selectedGender = st.multiselect(
    "Select Gender", np.unique(df["Gender2"][df["Gender2"].notnull()])
)
selectedOrientation = st.multiselect(
    "Select Sexual Orientation",
    np.unique(df["SexualOrientation2"][df["SexualOrientation2"].notnull()]),
)
selectedRace = st.multiselect(
    "Select Race", np.unique(df["RaceEthnicity2"][df["RaceEthnicity2"].notnull()])
)
selectedEducation = st.select_slider(
    "Select Highest Completed Level of Education",
    np.unique(df["FormalEducation"][df["FormalEducation"].notnull()]),
)
selectedAge = st.select_slider("Select Age", np.unique(df["Age"][df["Age"].notnull()]))


slice = get_slice_membership(
    df,
    selectedGender,
    selectedOrientation,
    selectedRace,
    [selectedEducation],
    [selectedAge],
)
slicedData = df[slice]


###########################################


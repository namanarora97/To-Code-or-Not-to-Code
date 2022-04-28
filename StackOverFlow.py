# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 15:28:43 2022

@author: somya
"""

import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
from MyBinarizer import MyBinarizer
import joblib
import urllib.request
from sklearn.preprocessing import MultiLabelBinarizer

# import pickle


# Referenced: https://docs.streamlit.io/library/api-reference/utilities/st.set_page_config
st.set_page_config(
    page_title="Factors that makes a programmer successful",
    page_icon=":shark",
    layout="wide",
    # initial_sidebar_state="expanded",
)

# Referenced: https://docs.streamlit.io/library/api-reference/layout/st.sidebar
add_selectbox = st.sidebar.radio(
    "To code or Not to code",
    (
        "Introduction",  # Welcome screen
        "Breaking the Habit",  # Ruhi's habits
        "Predict Job satisfaction",  # Somya's Country...
        "Today to Tomorrow",  # Somya's
        "Measure Success!",  # Nate's model
        "Predict Salary",  # Naman's Model
    ),
)


@st.cache(allow_output_mutation=True)
def load_model():
    return joblib.load(
        urllib.request.urlopen(
            "https://metashady.blob.core.windows.net/public/pipe_v2.pkl"
        )
    )


# @st.cache(allow_output_mutation=True)
def load_mlb():
    # return joblib.load("mlb.pkl")
    pass


@st.cache
def get_hist_df(df, Country, Salary=120000):
    df_ = df[
        (
            (df["Country"] == Country)
            & (~df["ConvertedSalary"].isna())
            & (df["ConvertedSalary"] > 100)
        )
    ][["ConvertedSalary"]]
    bins = list(range(0, 410000, 10000)) + [df_.ConvertedSalary.max()]
    df_["SalaryRange"] = pd.cut(df_["ConvertedSalary"], bins=bins, right=True)
    df_["SalaryBin"] = df_["SalaryRange"].apply(lambda x: int(x.left)).astype(int)
    yourbin = pd.cut([Salary], bins, right=True)[0]
    df_["YourSalary"] = df_["SalaryRange"].apply(lambda x: x == yourbin)
    df_["YourSalary"] = df_["YourSalary"].apply(lambda x: "You" if x else "Others")
    return df_[["SalaryBin", "YourSalary"]]


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
def get_slice_membership(
    df,
    genders=None,
    sexualOrientation=None,
    races=None,
    educations=None,
    age_range=None,
):
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
def get_job_satisfaction_df(df, country_selectbox, slider):
    """
    Preprocessing steps for job satisfaction prediction chart
    """
    new_df = df[~df["JobSatisfaction"].isna()]
    new_df = new_df[~new_df["CareerSatisfaction"].isna()]
    new_df_2 = new_df[(new_df["Country"] == country_selectbox)]
    new_df_2["distance"] = (new_df_2["ConvertedSalary"] - slider) ** 2
    new_df_2["rank"] = new_df_2["distance"].rank(method="first")
    new_df_3 = new_df_2[new_df_2["rank"] <= 10]
    new_df_4 = new_df_3["JobSatisfaction"].value_counts(normalize=True).reset_index()
    new_df_4.columns = ["JobSatisfaction", "Proportion"]
    new_df_4 = new_df_4.sort_values(by="Proportion", ascending=False).reset_index(
        drop=True
    )

    js_all = new_df[["JobSatisfaction"]].drop_duplicates()

    prediction = new_df_4["JobSatisfaction"].values[0]

    new_df_4 = pd.merge(new_df_4, js_all, on="JobSatisfaction", how="right").fillna(0)

    return prediction, new_df_4


@st.cache
def get_new_df(df):
    return df[~df["HopeFiveYears1"].isna() & ~df["CareerSatisfaction"].isna()]


#################################################


# 1. Introduction: Title& Header

alt.data_transformers.enable("default", max_rows=None)

# 2. Data Loading

with st.spinner(text="Loading data..."):
    df = load_data()


def clean_gender_col(gender):
    if gender not in ["Male", "Female"]:
        return "LGBTQ+"
    else:
        return gender


df["Gender"] = df["Gender"].apply(clean_gender_col)


if add_selectbox == "Introduction":
    st.title("To Code or Not to Code?")
    st.markdown("Made with :heart: by Team Zebra")
    st.markdown(
        "[Naman](mailto:namana@andrew.cmu.edu), [Nate](mailto:ndf@andrew.cmu.edu), [Somya](mailto:somyaa@andrew.cmu.edu), [Ruhi](mailto:ruhihemp@andrew.cmu.edu)."
    )
    # st.subheader("Team Zebra")
    st.image("survey-logo.png")
    st.write(
        "The dataset contains responses of 98,885 respondents who reported information ranging from their excercise habits to compensative levels"
    )
    st.write("We analyzed the data to find factors that make a programmer successful.")
    st.subheader("Use the sidebar to explore the data")
    # st.text("Visualize the overall dataset and some distributions here...")
    if st.checkbox("View a sample of the dataset"):
        st.write(df.head(20))
        st.write(len(df))


elif add_selectbox == "Today to Tomorrow":
    st.header("Today to Tomorrow")
    st.subheader(
        "Your satisfaction with your job today defines your actions for tomorrow."
    )
    st.write("We tried to explore this idea within the data.")
    # st.write(
    #     "This is a two way interactive graph through which the user can see how many respondents are satisfied/dissatisfied for a particular reason and vice-versa"
    # )
    st.write(
        "Try clicking through both plots to see how developers' 5-Year plans are affected by job satisfaction."
    )

    hope_brush = alt.selection_multi(fields=["HopeFiveYears1"])
    career_brush = alt.selection_multi(fields=["CareerSatisfaction"])

    new_df = get_new_df(df)

    hope_chart = (
        alt.Chart(new_df.sample(10000, random_state=1))
        .transform_filter(career_brush)
        .mark_bar()
        .encode(
            x=alt.X("count()", title="Number of respondents"),
            y=alt.Y("HopeFiveYears1", title="5-Year Plan"),
            color=alt.condition(
                hope_brush, alt.value("steelblue"), alt.value("lightgray")
            ),
        )
        .add_selection(hope_brush)
        .properties(width=750, height=300)
    )

    career_chart = (
        alt.Chart(new_df.sample(10000, random_state=1))
        .transform_filter(hope_brush)
        .mark_bar()
        .encode(
            x=alt.X("count()", title="Number of respondents"),
            y=alt.Y("CareerSatisfaction", title="Career Satisfaction"),
            tooltip="count()",
            color=alt.condition(
                career_brush, alt.value("salmon"), alt.value("lightgray")
            ),
        )
        .add_selection(career_brush)
        .properties(width=750, height=300)
    )

    st.altair_chart(hope_chart & career_chart)

#######################################################################################################################################

elif add_selectbox == "Predict Job satisfaction":
    # define dropdown
    st.header("Predict Job satisfaction according to your country and Salary")

    st.subheader("Slide to select a Salary")
    slider = st.slider(
        label="Salary", min_value=0, max_value=200000, step=1000, value=80000
    )
    st.write("Selected Value: ", slider)

    country_selectbox = st.selectbox("Country", df["Country"].unique(), 1)
    st.write("Selected Coutry: ", country_selectbox)

    prediction, new_df_4 = get_job_satisfaction_df(df, country_selectbox, slider)

    mychart = (
        alt.Chart(new_df_4)
        .mark_bar(color="steelblue")
        .encode(alt.X("Proportion"), alt.Y("JobSatisfaction"), tooltip="Proportion")
        .properties(width=800, height=500)
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

elif add_selectbox == "Breaking the Habit":
    # Breaking the Habit visualization
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

    st.header("Spending 12 hours a day on a computer to be happier?")
    st.subheader("Think again...")

    df1 = df.dropna(subset=columns1, how="any")
    input_dropdown = alt.binding_select(options=columns1, name="Habit")
    picked = alt.selection_single(
        fields=["Habit"], bind=input_dropdown, init={"Habit": "HoursComputer"}
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
            alt.Y(
                "value:N",
                sort=all_habits,
                title=("Chosen Value"),
            ),
            alt.X("median(ConvertedSalary)", title="Median Salary in USD/year"),
            color=alt.Color(
                "mean(JobSatisfactionQuant):Q",
                legend=alt.Legend(title="Mean Job Satisfaction"),
            ),
            tooltip=[
                alt.Tooltip("mean(ConvertedSalary):Q", title="Mean Salary in USD/year"),
                alt.Tooltip(
                    "mean(JobSatisfactionQuant):Q", title="Mean Job Satisfaction"
                ),
                alt.Tooltip("count(value):Q", title="Count of records"),
            ],
        )
        .add_selection(picked)
        .properties(width=800, height=500)
    )
    st.altair_chart(hist)

elif add_selectbox == "Measure Success!":
    #################################################

    # INPUT: string name of column
    # OUTPUT: dataframe with every unique entry as a one-hot encoding
    # Notes: entries must be seperated by ";"
    #       output will be in same order as dataframe passed in
    #            and can be appended if desired
    #       null entries will be categorized with a "1" in the "nan" column
    # CHANGE 'DATA' TO WHATEVER THE MAIN DATAFRAME IS NAMED
    def oneHot(columnName):
        tempData = pd.DataFrame(df[columnName].str.split(";"))
        tempData = tempData[columnName].tolist()
        for i in range(len(tempData)):
            if type(tempData[i]) == float:
                tempData[i] = [str(tempData[i])]
        mlb = MultiLabelBinarizer()
        mlb.fit(tempData)
        oneHot = pd.DataFrame(mlb.transform(tempData), columns=mlb.classes_)
        return oneHot

    # CHANGE 'DATA' TO WHATEVER THE MAIN DATAFRAME IS NAMED IN YOUR WORKSHEET
    # for this function aggName and oheColumn are both single strings.
    # support for multiple aggregation columns is below
    def plotableOHE(aggName, oheColumn):
        # use oneHot to oneHot the column of interest
        oheFrame = oneHot(oheColumn)
        # add the aggregate column (ie salary).
        oheFrame[aggName] = df[aggName]
        # remove rows where the aggregate value is null
        oheFrame = oheFrame[oheFrame[aggName].notnull()]
        # get the counts of each label
        ones = np.ones(len(oheFrame[aggName]))
        countColumn = np.dot(ones, oheFrame)
        # get the total of each label
        outputFrame = pd.DataFrame(oheFrame[aggName].dot(oheFrame))
        outputFrame.insert(loc=0, column=oheColumn, value=outputFrame.index)
        outputFrame.reset_index(drop=True, inplace=True)
        countsName = oheColumn + "Counts"
        outputFrame.insert(loc=1, column=countsName, value=countColumn)
        # the aggName row will have squared in the dot product- we just drop it
        outputFrame = outputFrame[outputFrame[oheColumn] != aggName]
        averageName = aggName + "Average"
        outputFrame[averageName] = outputFrame[aggName] / outputFrame[countsName]
        outputFrame.rename(columns={aggName: aggName + "Sum"}, inplace=True)
        return outputFrame

    # aggNames is a list of numerical column inputs. Can only work with one OHE column
    def multiplePlotOHE(aggNames, oheColumn):
        outputFrame = plotableOHE(aggNames[0], oheColumn)
        for agg in aggNames[1:]:
            newOutputFrame = plotableOHE(agg, oheColumn)
            outputFrame = outputFrame.join(
                newOutputFrame.set_index(oheColumn), on=oheColumn, rsuffix="_other"
            )
            dropColumn = oheColumn + "Counts_other"
            outputFrame.drop(dropColumn, axis=1, inplace=True)
        return outputFrame

    #################################################
    ###########################################
    qualList = [
        "LanguageWorkedWith",
        "UndergradMajor",
        "IDE",
        "FormalEducation",
        "DevType",
        "HopeFiveYears1",
        "PlatformWorkedWith",
        "FrameworkWorkedWith",
        "OperatingSystem",
        "VersionControl",
    ]
    quantList = [
        "ConvertedSalary",
        "JobSatisfactionQuant",
        "YearsCodingQuantSmall",
        "CompanySizeQuantSmall",
        "YearsCodingProfQuantSmall",
        "NumberMonitors",
    ]

    quants = [quantList[5], quantList[3]]
    qual = qualList[1]
    qual = st.selectbox("Select Category", qualList)
    quants[0] = st.selectbox("Select primary measurement", quantList)
    quants[1] = st.selectbox("Select secondary measurement", quantList)
    # st.write(qual)
    # st.write(quants)
    #
    # quants = random.choices(quantList, k=2)
    # qual = random.choice(qualList)

    # print(quants)
    # print(qual)

    plotData = multiplePlotOHE(quantList, qual)

    title = qual + " " + quants[0] + " and " + quants[1]
    y = quants[0] + "Average:Q"
    yTitle = "Average " + quants[0]
    color = quants[1] + "Average"

    multi = alt.selection_multi(encodings=["x"], toggle="true", empty="none")

    autoChart = (
        alt.Chart(plotData, title=title)
        .mark_bar(opacity=0.7, tooltip=True)
        .encode(
            y=alt.Y(qual, sort="x"), x=alt.X(y, stack=None, title=yTitle), color=color
        )
        .properties(width=800, height=500)
        .add_selection(multi)
        .encode(opacity=alt.condition(multi, alt.value(1), alt.value(0.4)))
    )

    base = (
        alt.Chart()
        .mark_bar(opacity=0.7, tooltip=True)
        .encode()
        .properties(width=240, height=100)
    )

    desiredColumns0 = [qual + "Counts", "CompanySizeQuantSmallAverage"]
    desiredColumns = [
        ["ConvertedSalaryAverage", "YearsCodingQuantSmallAverage"],
        ["JobSatisfactionQuantAverage", "NumberMonitorsAverage"],
    ]
    modChart = alt.vconcat(data=plotData, title=qual)
    for i in range(2):
        row = alt.hconcat()
        row |= base.encode(
            y=alt.Y(qual, title=" "),
            x=desiredColumns0[i] + ":Q",
            tooltip=desiredColumns0[i] + ":Q",
        )
        for y_encoding in desiredColumns[i]:
            row |= base.encode(
                y=alt.Y(qual, axis=alt.Axis(labels=False), title=" "),
                x=alt.X(y_encoding + ":Q"),
                tooltip=y_encoding + ":Q",
            )
        modChart &= row

    invisible = alt.Chart().mark_bar(opacity=0).encode().properties(width=0, height=0)

    st.altair_chart(autoChart & modChart.transform_filter(multi) & invisible)

    #############################################


elif add_selectbox == "Predict Salary":

    st.header("How much can you earn?")

    st.subheader("Let's get some information first.")

    with st.form("Prediction"):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            Age = st.selectbox(
                "Age",
                [
                    "18 - 24 years old",
                    "25 - 34 years old",
                    "35 - 44 years old",
                    "45 - 54 years old",
                    "55 - 64 years old",
                    "65 years or older",
                    "Under 18 years old",
                ],
                index=1,
            )
            Country = st.selectbox(
                "Country",
                [
                    "Afghanistan",
                    "Albania",
                    "Algeria",
                    "Andorra",
                    "Argentina",
                    "Armenia",
                    "Australia",
                    "Austria",
                    "Azerbaijan",
                    "Bahamas",
                    "Bahrain",
                    "Bangladesh",
                    "Barbados",
                    "Belarus",
                    "Belgium",
                    "Benin",
                    "Bhutan",
                    "Bolivia",
                    "Bosnia and Herzegovina",
                    "Botswana",
                    "Brazil",
                    "Bulgaria",
                    "Cambodia",
                    "Cameroon",
                    "Canada",
                    "Chile",
                    "China",
                    "Colombia",
                    "Congo, Republic of the...",
                    "Costa Rica",
                    "Croatia",
                    "Cuba",
                    "Cyprus",
                    "Czech Republic",
                    "Côte d'Ivoire",
                    "Democratic Republic of the Congo",
                    "Denmark",
                    "Dominica",
                    "Dominican Republic",
                    "Ecuador",
                    "Egypt",
                    "El Salvador",
                    "Eritrea",
                    "Estonia",
                    "Ethiopia",
                    "Fiji",
                    "Finland",
                    "France",
                    "Gambia",
                    "Georgia",
                    "Germany",
                    "Ghana",
                    "Greece",
                    "Guatemala",
                    "Guyana",
                    "Honduras",
                    "Hong Kong (S.A.R.)",
                    "Hungary",
                    "Iceland",
                    "India",
                    "Indonesia",
                    "Iran, Islamic Republic of...",
                    "Iraq",
                    "Ireland",
                    "Israel",
                    "Italy",
                    "Jamaica",
                    "Japan",
                    "Jordan",
                    "Kazakhstan",
                    "Kenya",
                    "Kuwait",
                    "Kyrgyzstan",
                    "Latvia",
                    "Lebanon",
                    "Lesotho",
                    "Libyan Arab Jamahiriya",
                    "Liechtenstein",
                    "Lithuania",
                    "Luxembourg",
                    "Madagascar",
                    "Malawi",
                    "Malaysia",
                    "Maldives",
                    "Malta",
                    "Mauritius",
                    "Mexico",
                    "Monaco",
                    "Mongolia",
                    "Montenegro",
                    "Morocco",
                    "Mozambique",
                    "Myanmar",
                    "Namibia",
                    "Nepal",
                    "Netherlands",
                    "New Zealand",
                    "Nicaragua",
                    "Nigeria",
                    "Norway",
                    "Oman",
                    "Other Country (Not Listed Above)",
                    "Pakistan",
                    "Panama",
                    "Paraguay",
                    "Peru",
                    "Philippines",
                    "Poland",
                    "Portugal",
                    "Qatar",
                    "Republic of Korea",
                    "Republic of Moldova",
                    "Romania",
                    "Russian Federation",
                    "Rwanda",
                    "Saint Lucia",
                    "Saudi Arabia",
                    "Senegal",
                    "Serbia",
                    "Sierra Leone",
                    "Singapore",
                    "Slovakia",
                    "Slovenia",
                    "Somalia",
                    "South Africa",
                    "South Korea",
                    "Spain",
                    "Sri Lanka",
                    "Sudan",
                    "Suriname",
                    "Swaziland",
                    "Sweden",
                    "Switzerland",
                    "Syrian Arab Republic",
                    "Taiwan",
                    "Tajikistan",
                    "Thailand",
                    "The former Yugoslav Republic of Macedonia",
                    "Togo",
                    "Trinidad and Tobago",
                    "Tunisia",
                    "Turkey",
                    "Turkmenistan",
                    "Uganda",
                    "Ukraine",
                    "United Arab Emirates",
                    "United Kingdom",
                    "United Republic of Tanzania",
                    "United States",
                    "Uruguay",
                    "Uzbekistan",
                    "Venezuela, Bolivarian Republic of...",
                    "Viet Nam",
                    "Yemen",
                    "Zimbabwe",
                ],
                148,
            )
            Gender2 = st.selectbox(
                "Select your Gender", ["Female", "Male", "Non-Binary"], 1
            )
            Hobby = st.selectbox(
                "Do you code as a hobby?",
                ["Yes", "No"],
                0,
            )
            OpenSource = st.selectbox(
                "Do you contribute to open source projects?",
                ["Yes", "No"],
                0,
            )
        with col2:
            LanguageWorkedWith = st.multiselect(
                "Languages you have worked with",
                [
                    "Assembly",
                    "Bash/Shell",
                    "C",
                    "C#",
                    "C++",
                    "CSS",
                    "Clojure",
                    "Cobol",
                    "CoffeeScript",
                    "Delphi/Object Pascal",
                    "Erlang",
                    "F#",
                    "Go",
                    "Groovy",
                    "HTML",
                    "Hack",
                    "Haskell",
                    "Java",
                    "JavaScript",
                    "Julia",
                    "Kotlin",
                    "Lua",
                    "Matlab",
                    "Objective-C",
                    "Ocaml",
                    "PHP",
                    "Perl",
                    "Python",
                    "R",
                    "Ruby",
                    "Rust",
                    "SQL",
                    "Scala",
                    "Swift",
                    "TypeScript",
                    "VB.NET",
                    "VBA",
                    "Visual Basic 6",
                ],
                default=["C", "C#", "C++", "JavaScript", "Python", "Ruby", "Java"],
            )
            FrameworkWorkedWith = st.multiselect(
                "Frameworks you have worked with",
                [
                    ".NET Core",
                    "Angular",
                    "Cordova",
                    "Django",
                    "Hadoop",
                    "Node.js",
                    "None",
                    "React",
                    "Spark",
                    "Spring",
                    "TensorFlow",
                    "Torch/PyTorch",
                    "Xamarin",
                ],
                default=["Angular", "React", "Spark", "TensorFlow", "Torch/PyTorch"],
            )
        with col3:
            FormalEducation = st.selectbox(
                "Please provide your highest level of formal education",
                [
                    "Associate degree",
                    "Bachelor's",
                    "High school",
                    "I never completed any formal education",
                    "Master's",
                    "Other doctoral degree (Ph.D, Ed.D., etc.)",
                    "Primary/elementary school",
                    "Professional degree (JD, MD, etc.)",
                    "Some college",
                ],
                1,
            )

            UndergradMajor = st.selectbox(
                "Please select your undergraduate major",
                [
                    "Business",
                    "Computer Science",
                    "Engineering (non-computer)",
                    "Fine Arts",
                    "Health Science",
                    "Humanities",
                    "Information Systems",
                    "Mathematics",
                    "Natural Science",
                    "None",
                    "Not Applicable",
                    "Social Science",
                    "Undeclared",
                    "Web Design",
                ],
                1,
            )

            CompanySize = st.selectbox(
                "Please select your previous/current company size",
                [
                    "Not Applicable",
                    "0 to 1 Employees",
                    "Fewer than 10 employees",
                    "10 to 19 employees",
                    "20 to 99 employees",
                    "100 to 499 employees",
                    "500 to 999 employees",
                    "1,000 to 4,999 employees",
                    "5,000 to 9,999 employees",
                    "10,000 or more employees",
                ],
                5,
            )
        with col4:
            DevType = st.multiselect(
                "What type of developer(s) are you?",
                [
                    "Back-end developer",
                    "C-suite executive (CEO, CTO, etc.)",
                    "Data or business analyst",
                    "Data scientist or machine learning specialist",
                    "Database administrator",
                    "Designer",
                    "Desktop or enterprise applications developer",
                    "DevOps specialist",
                    "Educator or academic researcher",
                    "Embedded applications or devices developer",
                    "Engineering manager",
                    "Front-end developer",
                    "Full-stack developer",
                    "Game or graphics developer",
                    "Marketing or sales professional",
                    "Mobile developer",
                    "Product manager",
                    "QA or test developer",
                    "Student",
                    "System administrator",
                ],
                default=[
                    "Back-end developer",
                    "Data scientist or machine learning specialist",
                    "Front-end developer",
                    "Full-stack developer",
                ],
            )

            YearsCodingProf = st.selectbox(
                "How many years have you been a professional developer?",
                [
                    "0-2 years",
                    "3-5 years",
                    "6-8 years",
                    "9-11 years",
                    "12-14 years",
                    "15-17 years",
                    "18-20 years",
                    "21-23 years",
                    "24-26 years",
                    "27-29 years",
                    "30 or more years",
                ],
                1,
            )

            Employment = st.selectbox(
                "What is your current employment status?",
                [
                    "full-time",
                    "part-time",
                    "Independent contractor, freelancer, or self-employed",
                    "Not employed, and not looking for work",
                    "Not employed, but looking for work",
                    "Retired",
                ],
            )

        submitted = st.form_submit_button("Submit")

        if submitted:
            # st.experimental_rerun()
            pipe = load_model()
            mlb = load_mlb()

            df = pd.DataFrame()
            df = df.append(
                {
                    "Age": Age,
                    "LanguageWorkedWith": LanguageWorkedWith,
                    "FrameworkWorkedWith": FrameworkWorkedWith,
                    "Country": Country,
                    "Hobby": Hobby,
                    "OpenSource": OpenSource,
                    "FormalEducation": FormalEducation,
                    "UndergradMajor": UndergradMajor,
                    "DevType": DevType,
                    "YearsCodingProf": YearsCodingProf,
                    "Employment": Employment,
                    "Gender2": Gender2,
                    "CompanySize": CompanySize,
                },
                ignore_index=True,
            )

            # st.dataframe(df)

            prediction = round(pipe.predict(df)[0])

            standing = (
                alt.Chart(get_hist_df(load_data(), "United States", 120000))
                .mark_bar(size=18)
                .encode(
                    x=alt.X(
                        "SalaryBin:O", sort="ascending", title="Salary Range ($/year)"
                    ),
                    y=alt.Y("count()", title="Number of Respondents"),
                    color=alt.Color("YourSalary", legend=alt.Legend(title="Salary")),
                )
                .properties(width=1400, height=600)
            )

            st.subheader("Your predicted annual salary is: $" + str(prediction))
            st.subheader("Let's take a look at how you rank. ")
            st.altair_chart(standing)

        ###########################################

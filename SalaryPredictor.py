import streamlit as st
import altair as alt
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np
from MyBinarizer import MyBinarizer
import joblib


# @st.cache(allow_output_mutation=True)
def load_model():
    return joblib.load("pipe_v2.pkl")


# @st.cache(allow_output_mutation=True)
def load_mlb():
    return joblib.load("mlb.pkl")


st.header("How much can you earn?")

st.subheader("Let's get some information first.")


with st.form("Prediction"):
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
    )

    Hobby = st.selectbox(
        "Do you code as a hobby?",
        ["Yes", "No"],
    )

    OpenSource = st.selectbox(
        "Do you contribute to open source projects?",
        ["Yes", "No"],
    )

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
    )

    CompanySize = st.selectbox(
        "Please select your previous/current company size",
        [
            "0 to 1 Employees",
            "1,000 to 4,999 employees",
            "10 to 19 employees",
            "10,000 or more employees",
            "100 to 499 employees",
            "20 to 99 employees",
            "5,000 to 9,999 employees",
            "500 to 999 employees",
            "Fewer than 10 employees",
            "Not Applicable",
        ],
    )

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
    )

    YearsCodingProf = st.selectbox(
        "How many years have you been a professional developer?",
        [
            "0-2 years",
            "12-14 years",
            "15-17 years",
            "18-20 years",
            "21-23 years",
            "24-26 years",
            "27-29 years",
            "3-5 years",
            "30 or more years",
            "6-8 years",
            "9-11 years",
        ],
    )

    Employment = st.selectbox(
        "What is your current employment status?",
        [
            "Independent contractor, freelancer, or self-employed",
            "Not employed, and not looking for work",
            "Not employed, but looking for work",
            "Retired",
            "full-time",
            "part-time",
        ],
    )

    Gender2 = st.selectbox("Select your Gender", ["Female", "Male", "Non-Binary"])

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

        st.subheader("Your predicted salary is: $" + str(prediction))

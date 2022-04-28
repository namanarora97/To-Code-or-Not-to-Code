# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 15:28:43 2022

@author: somya
"""
########################################
import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
import random
########################################

@st.experimental_singleton
def load_data():
    # df = pd.read_csv("Crimes_2021_1.csv")
    df = pd.read_csv("InitialClean.csv")
    # salary_category = ["Low(<10,000)", "Low-Med(10k-49k)","Medium(49k-85k)", "High(85k-150k)","Very High(150<)"]

    # Drop all unused columns[TBD]
    drop_col = ['CurrencySymbol', 'Respondent']
    # df.drop(drop_col)
    return df

#################################################
# taken and modified from the interactivity lab

#INPUT: string name of column
#OUTPUT: dataframe with every unique entry as a one-hot encoding
#Notes: entries must be seperated by ";"
#       output will be in same order as dataframe passed in
#            and can be appended if desired
#       null entries will be categorized with a "1" in the "nan" column
#CHANGE 'DATA' TO WHATEVER THE MAIN DATAFRAME IS NAMED
def oneHot(columnName):
    tempData = pd.DataFrame(df[columnName].str.split(";"))
    tempData = tempData[columnName].tolist()
    for i in range(len(tempData)):
        if type(tempData[i])==float:
            tempData[i]=[str(tempData[i])]
    mlb = MultiLabelBinarizer()
    mlb.fit(tempData)
    oneHot = pd.DataFrame(mlb.transform(tempData), columns = mlb.classes_)
    return oneHot

#CHANGE 'DATA' TO WHATEVER THE MAIN DATAFRAME IS NAMED IN YOUR WORKSHEET
#for this function aggName and oheColumn are both single strings.
#support for multiple aggregation columns is below
def plotableOHE(aggName, oheColumn):
    #use oneHot to oneHot the column of interest
    oheFrame = oneHot(oheColumn)
    #add the aggregate column (ie salary).
    oheFrame[aggName] = df[aggName]
    #remove rows where the aggregate value is null
    oheFrame = oheFrame[oheFrame[aggName].notnull()]
    #get the counts of each label
    ones = np.ones(len(oheFrame[aggName]))
    countColumn = np.dot(ones,oheFrame)
    #get the total of each label
    outputFrame = pd.DataFrame(oheFrame[aggName].dot(oheFrame))
    outputFrame.insert(loc=0,column=oheColumn, value=outputFrame.index)
    outputFrame.reset_index(drop=True, inplace=True)
    countsName = oheColumn + "Counts"
    outputFrame.insert(loc=1,column=countsName, value=countColumn)
    #the aggName row will have squared in the dot product- we just drop it
    outputFrame=outputFrame[outputFrame[oheColumn]!=aggName]
    averageName = aggName+"Average"
    outputFrame[averageName] = outputFrame[aggName]/outputFrame[countsName]
    outputFrame.rename(columns = {aggName:aggName+"Sum"}, inplace = True)
    return outputFrame


# aggNames is a list of numerical column inputs. Can only work with one OHE column
def multiplePlotOHE(aggNames, oheColumn):
    outputFrame = plotableOHE(aggNames[0], oheColumn)
    for agg in aggNames[1:]:
        newOutputFrame = plotableOHE(agg, oheColumn)
        outputFrame = outputFrame.join(newOutputFrame.set_index(oheColumn), on=oheColumn, rsuffix='_other')
        dropColumn = oheColumn + "Counts_other"
        outputFrame.drop(dropColumn, axis=1, inplace=True)
    return outputFrame




#################################################


# 1. Introduction: Title& Header

alt.data_transformers.enable('default', max_rows=None)

# st.title("Interactive Data Science")
st.title("Factors that makes a programmer successful")
st.subheader("Team Zebra")

st.write(
    "This dataset contains responses of 98,885 respondents who reported information ranging from their excercise habits to compensative levels")

# 2. Data Loading

with st.spinner(text="Loading data..."):
    df = load_data()
    st.text("Visualize the overall dataset and some distributions here...")
    if st.checkbox('Show Table'):
        st.write(df.head(20))
        st.write(len(df))



###########################################
qualList = ["LanguageWorkedWith", "UndergradMajor", "IDE", "FormalEducation", "DevType", "HopeFiveYears1",
            "PlatformWorkedWith", "FrameworkWorkedWith", "OperatingSystem", "VersionControl"]
quantList = ["ConvertedSalary", "JobSatisfactionQuant", "YearsCodingQuantSmall",
             "CompanySizeQuantSmall", "YearsCodingProfQuantSmall", "NumberMonitors"]

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

multi = alt.selection_multi(encodings=['x'], toggle="true", empty='none')

autoChart = alt.Chart(plotData, title=title).mark_bar(opacity=0.7, tooltip=True).encode(
    y=alt.Y(qual, sort='x'),
    x=alt.X(y, stack=None, title=yTitle),
    color=color
).properties(width=800, height=500
).add_selection(
    multi
).encode(
    opacity=alt.condition(multi, alt.value(1), alt.value(.4))
)

base = alt.Chart().mark_bar(opacity=0.7, tooltip=True).encode(

).properties(
     width=240,
     height=100
)

desiredColumns0 = [qual+"Counts", "CompanySizeQuantSmallAverage"]
desiredColumns = [["ConvertedSalaryAverage", "YearsCodingQuantSmallAverage"], \
                  ["JobSatisfactionQuantAverage", "NumberMonitorsAverage"]]
modChart = alt.vconcat(data=plotData, title=qual)
for i in range(2):
    row = alt.hconcat()
    row |= base.encode(y=alt.Y(qual, title=" "), x=desiredColumns0[i] + ":Q", tooltip=desiredColumns0[i] + ":Q")
    for y_encoding in desiredColumns[i]:
        row |= base.encode(y=alt.Y(qual, axis=alt.Axis(labels=False), title=" "), x=alt.X(y_encoding+":Q"), tooltip=y_encoding+":Q")
    modChart &= row

invisible = alt.Chart().mark_bar(opacity=0).encode().properties(
     width=0,
     height=0
)

st.altair_chart(autoChart & modChart.transform_filter(multi) & invisible)

#############################################



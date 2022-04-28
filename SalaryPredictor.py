

import streamlit as st
import altair as alt
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.base import BaseEstimator,TransformerMixin
import pandas as pd
import numpy as np
from MyBinarizer import MyBinarizer
import joblib

@st.cache
def load_model():
    return joblib.load("model.joblib")


st.header("How much can you earn?")



import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from MyBinarizer import MyBinarizer
from sklearn.model_selection import train_test_split
import joblib


# Load the data from Azure blob storage
df = pd.read_csv("https://metashady.blob.core.windows.net/public/InitialClean_NF.csv")

# Apply the fixes
df_pred = df[~df.ConvertedSalary.isna()]

# Apply the fixes
df_pred = df_pred[
    [
        "Age",
        "Gender2",
        "LanguageWorkedWith",
        "FrameworkWorkedWith",
        "Country",
        "Hobby",
        "OpenSource",
        "FormalEducation",
        "UndergradMajor",
        "CompanySize",
        "DevType",
        "YearsCodingProf",
        "ConvertedSalary",
        "Employment",
    ]
]

# Drop nulls
df_pred = df_pred.dropna(
    axis=0, subset=df_pred.loc[:, (df_pred.isna().sum() / len(df_pred) < 0.1)].columns
)


def fix_CompanySize(r):
    """
    Fix the CompanySize column
    """
    if type(r.CompanySize) != str:
        if r.Employment == "Independent contractor, freelancer, or self-employed":
            r.CompanySize = "0 to 1 Employees"
        elif r.Employment in [
            "Not employed, but looking for work",
            "full-time",
            "Not employed, and not looking for work",
            "part-time",
            "Retired",
        ]:
            r.CompanySize = "Not Applicable"
    return r


def fix_UndergradMajor(r):
    """
    Fix the UndergradMajor column
    """
    if r.FormalEducation.strip() in [
        "High school",
        "I never completed any formal education",
        "Associate degree",
        "Primary/elementary school",
    ]:
        r.UndergradMajor = "Not Applicable"
    return r


# Apply the fixes
df_pred = df_pred.apply(fix_CompanySize, axis=1)
df_pred.FrameworkWorkedWith.replace(np.nan, "None", inplace=True)

df_pred = df_pred.apply(fix_UndergradMajor, axis=1)
df_pred.UndergradMajor.replace(np.nan, "None", inplace=True)

df_pred.FrameworkWorkedWith.replace(np.nan, "None", inplace=True)

# Create the X and y
x_cols = [
    "Age",
    "LanguageWorkedWith",
    "FrameworkWorkedWith",
    "Country",
    "Hobby",
    "OpenSource",
    "FormalEducation",
    "UndergradMajor",
    "CompanySize",
    "DevType",
    "YearsCodingProf",
    "Employment",
    "Gender2",
]
y_col = ["ConvertedSalary"]

# Save for later use
df_pred.to_csv("cleaned_df_pred_v3.csv", index=False)
df_pred.to_pickle("df_pred_v3.pkl")

# Create the X and y
df_pred_X = df_pred[x_cols].apply(
    lambda column: column.apply(lambda item: np.array(item.split(";")))
)

df_pred_Y = df_pred[y_col]

# Perform test/train split
X_train, X_test, y_train, y_test = train_test_split(
    df_pred_X, df_pred_Y, test_size=0.1, random_state=42
)

# Create the pipeline
categorical_features = list(df_pred_X.columns)

categorical_transformer = Pipeline(steps=[("encoder", MyBinarizer())])

preprocessor = ColumnTransformer(
    transformers=[("categorical", categorical_transformer, categorical_features)]
)

pipe = Pipeline(
    steps=[("preprocessor", preprocessor), ("rf", RandomForestRegressor(verbose=2))]
)

# Create the grid for grid search
param_grid = {
    "rf__n_estimators": [50, 100, 200, 300, 400],
    "rf__min_samples_split": [2, 3, 4],
    "rf__min_samples_leaf": [1, 2, 3],
    "rf__max_features": ["auto", "sqrt", "log2", 3, 4, 5],
}

# Create the grid search
search = GridSearchCV(pipe, param_grid, n_jobs=-1, verbose=10)

# Fit the model
search.fit(X_train, y_train)

# Save the model to make predictions later
joblib.dump(search, "./pipe_v2.pkl")

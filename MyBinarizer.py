from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

# This class is used to binarize a multi-label column
# It can be understood as a multi-label one-hot encoder


class MyBinarizer(BaseEstimator, TransformerMixin):
    def __init__(self):
        """
        Set up the class
        """
        print(">>>> Binarizer Initialized")
        self.mlb_list = []

    def fit(self, X, y=None):
        """
        Fit the binarizer on all the features in the dataframe
        """
        print(">>>> Fit called")
        for column in list(X.columns):
            mlb = MultiLabelBinarizer()
            self.mlb_list.append((column, mlb.fit(X[column]), list(mlb.classes_)))
        # print(self.mlb_list)
        return self

    def transform(self, X, y=None):
        """
        Return the transformed dataframe
        """
        print(">>>> Transform called")
        X_ = pd.DataFrame()
        for item in self.mlb_list:
            column, mlb, cols = item
            X_temp = pd.DataFrame(mlb.transform(X[column]), columns=cols)
            X_ = pd.concat([X_, X_temp], axis=1)
        return X_

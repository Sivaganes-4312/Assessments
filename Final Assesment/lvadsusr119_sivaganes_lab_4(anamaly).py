# -*- coding: utf-8 -*-
"""lvadsusr119-Sivaganes-Lab-4(Anamaly).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wFco8r8F4VhBUr_yhv9GG4E0EwlXpLxl
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import warnings as wr
wr.filterwarnings("ignore")

data = pd.read_csv("/content/social_network.csv")
data.head()

data.isnull().sum()

data.shape

Q1 = data.quantile(0.25)
Q3 = data.quantile(0.75)
IQR = Q3 - Q1

outliers = ((data < (Q1 - 1.5 * IQR)) | (data > (Q3 + 1.5 * IQR))).any(axis=1)
print(outliers)

cleaned_data = data[~outliers]

print("Shape of the data:", cleaned_data.shape)
print("Descriptive statistics:")
print(cleaned_data.describe())

for i in cleaned_data.columns:
    plt.figure()
    sns.histplot(cleaned_data[i], kde=True)
    plt.title(f'Histogram of {i}')
    plt.xlabel(i)
    plt.ylabel('Frequency')
    plt.show()

X = cleaned_data[['login_activity', 'posting_activity', 'social_connections']]
y = cleaned_data['suspicious_activity']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = IsolationForest(contamination=0.1)
model.fit(X_train)

y_pred = model.predict(X_train)

cleaned_data["anomaly_score"] = model.decision_function(X)

anomalies = cleaned_data.loc[cleaned_data["anomaly_score"] < 0]

plt.scatter(cleaned_data["social_connections"],cleaned_data["anomaly_score"], label="Not Anomaly")
plt.scatter(anomalies["social_connections"], anomalies["anomaly_score"], color="r", label="Anomaly")
plt.xlabel("Social Connections")
plt.ylabel("Anomaly Score")
plt.legend()
plt.show()
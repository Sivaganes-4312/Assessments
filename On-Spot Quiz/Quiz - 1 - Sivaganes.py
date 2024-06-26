# -*- coding: utf-8 -*-
"""Untitled26.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HHWHX8Otk9JP06IG73Ljl9WpyRrMCNB9
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import xgboost

import pandas as pd

df = pd.read_csv('/content/DSAI-LVA-DATASET for Quiz.csv')

def pass_segmentation(x):
  if x>=75:
    return "Passed with high score"
  elif(x>=50 and x<75):
    return "Passed with low score"
  else:
    return "Failed"
df['Pass'] = df["PreviousTestScore"].apply(pass_segmentation)
df

def education_segmentation(row):
  x = row['StudyTime']
  y = row['ParentEducation']
  if x > 7 and y =="College":
    return "Masters"
  elif x<=7 and y=="College":
    return "College"
  else:
    return "HighSchool"
df['ParentEducation']= df.apply(education_segmentation,axis = 1)
df

encode = LabelEncoder()
df['ParentEducation'] = encode.fit_transform(df['ParentEducation'] )
df['Pass'] = encode.fit_transform(df['Pass'])

split_ratio = 0.8

split_index = int(len(df) * split_ratio)

df_train = df.iloc[:split_index]
df_test = df.iloc[split_index:]

df_train.to_csv('train_data.csv', index=False)
df_test.to_csv('test_data.csv', index=False)

model = RandomForestClassifier()
model1 = DecisionTreeClassifier()
model2 = xgboost.XGBClassifier()
train = pd.read_csv('/content/train_data.csv')
test = pd.read_csv('/content/test_data.csv')
x = train.drop(columns = 'Pass',axis = 1)
y = train['Pass']
xtest = test.drop(columns = 'Pass',axis = 1)
ytest = test['Pass']
model.fit(x,y)
y_pred = model.predict(xtest)
model1.fit(x,y)
y_pred1 = model1.predict(xtest)
model2.fit(x,y)
y_pred2 = model2.predict(xtest)
accuracy_scored = accuracy_score(ytest,y_pred)
accuracy_scored_1 = accuracy_score(ytest,y_pred1)
accuracy_scored_2 = accuracy_score(ytest,y_pred2)
print("Accuracy score for RandomForest: ",accuracy_scored)
print("Accuracy score for DecisionTree: ",accuracy_scored_1)
print("Accuracy score for XGBoost: ",accuracy_scored_2)

sns.barplot([accuracy_scored,accuracy_scored_1,accuracy_scored_2])
plt.ylabel('Accuracy')
plt.xlabel(['RF','KNN','XGB'])
plt.show()
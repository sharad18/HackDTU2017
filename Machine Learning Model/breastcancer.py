def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

import numpy as np 
import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import KFold  
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn import metrics
from sklearn import preprocessing

df = pd.read_csv('data.csv')

le = preprocessing.LabelEncoder()
df['diagnosis'] = le.fit_transform(df['diagnosis'])

df.drop('id', axis=1, inplace=True)
df.drop('Unnamed: 32', axis=1, inplace=True)
df.drop('fractal_dimension_worst', axis=1, inplace=True)
df.drop('symmetry_worst', axis=1, inplace=True)
df.drop('concave points_worst', axis=1, inplace=True)
df.drop('concavity_worst', axis=1, inplace=True)
df.drop('compactness_worst', axis=1, inplace=True)
df.drop('smoothness_worst', axis=1, inplace=True)
df.drop('area_worst', axis=1, inplace=True)
df.drop('perimeter_worst', axis=1, inplace=True)
df.drop('texture_worst', axis=1, inplace=True)
df.drop('radius_worst', axis=1, inplace=True)
df.drop('fractal_dimension_se', axis=1, inplace=True)
df.drop('symmetry_se', axis=1, inplace=True)
df.drop('concave points_se', axis=1, inplace=True)
df.drop('concavity_se', axis=1, inplace=True)
df.drop('compactness_se', axis=1, inplace=True)
df.drop('smoothness_se', axis=1, inplace=True)
df.drop('area_se', axis=1, inplace=True)
df.drop('perimeter_se', axis=1, inplace=True)
df.drop('texture_se', axis=1, inplace=True)
df.drop('radius_se', axis=1, inplace=True)

traindf, testdf = train_test_split(df, test_size = 0.3)


def classification_model(model, data, predictors, outcome):
  model.fit(data[predictors],data[outcome])
  predictions = model.predict(data[predictors])
  accuracy = metrics.accuracy_score(predictions,data[outcome])
  #print("Accuracy : %s" % "{0:.3%}".format(accuracy))
  kf = KFold(data.shape[0], n_folds=5)
  error = []
  for train, test in kf:
    train_predictors = (data[predictors].iloc[train,:])
    train_target = data[outcome].iloc[train]
    model.fit(train_predictors, train_target)
    error.append(model.score(data[predictors].iloc[test,:], data[outcome].iloc[test]))
    #print("Cross-Validation Score : %s" % "{0:.3%}".format(np.mean(error)))
  model.fit(data[predictors],data[outcome]) 

predictor_var = ['radius_mean','perimeter_mean','area_mean','compactness_mean','concave points_mean', 'texture_mean', 'smoothness_mean', 'concavity_mean', 'symmetry_mean', 'fractal_dimension_mean']
outcome_var='diagnosis'
model = RandomForestClassifier(n_estimators=100,min_samples_split=25, max_depth=7, max_features=2)
classification_model(model, traindf,predictor_var,outcome_var)

from sklearn.externals import joblib
joblib.dump(model, 'model.pkl')
model_columns = list(x.columns)
joblib.dumps(model_columns, 'model_columns.pkl')

def Prediction_model(model, user_val):
    pred = model.predict([user_val])
    if pred == [0]:
    	print ('Diagnosis is BENIGN')
    else:
    	print ('Diagnosis is MALIGNANT')

#user_val = [17, 123, 1000, 0.30, 0.15, 13, 0.10, 0.30, 0.46, 0.10]
#Prediction_model(model, user_val)




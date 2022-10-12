# Import packages
from sklearn.ensemble import VotingClassifier
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
import pandas as pd
import joblib
import gzip
from sklearn.datasets import load_breast_cancer


# Load the dataset
from sklearn.datasets import load_breast_cancer
data_temp = load_breast_cancer()
data = pd.DataFrame(data_temp.data, columns = data_temp.feature_names) 


# Preselected feature
selected_features = [
    'mean concavity',
    'mean concave points',
    'mean perimeter',
    'worst texture',
    'worst area'
]


# Preprocess dataset

data['diagnosis'] = data_temp.target

# Split into train and test set, 80%-20%
y = data.pop('diagnosis')
X = data
X = X[selected_features.copy()]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create an ensemble of 3 models
estimators = []
estimators.append(('logistic', LogisticRegression()))
estimators.append(('cart', DecisionTreeClassifier()))
estimators.append(('svm', SVC()))

# Create the Ensemble Model
ensemble = VotingClassifier(estimators)

# Make preprocess Pipeline
pipe = Pipeline([
    ('imputer', SimpleImputer()),  # Missing value Imputer
    ('scaler', MinMaxScaler(feature_range=(0, 1))),  # Min Max Scaler
    ('model', ensemble)  # Ensemble Model
])

# Train the model
pipe.fit(X_train, y_train)

# Test Accuracy
print("Accuracy: %s%%" % str(round(pipe.score(X_test, y_test), 3) * 100))

# Export model
joblib.dump(pipe, gzip.open('../model/model_binary.dat.gz', "wb"))
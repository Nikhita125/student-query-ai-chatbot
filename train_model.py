import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

data = pd.read_csv("dataset/intents.csv")

X = data["question"]
y = data["intent"]

model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", LogisticRegression())
])

model.fit(X, y)

joblib.dump(model, "model/chatbot_model.pkl")

print("Model trained successfully!")
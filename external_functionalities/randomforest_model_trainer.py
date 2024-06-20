import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib

def model_trainer():
    df = pd.read_csv('external_functionalities/sample_skills.csv')
    X = df['SKILLS']
    y = df['SKILLS']
    vectorizer = TfidfVectorizer()
    X_vectorized = vectorizer.fit_transform(X)
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_vectorized, y)
    joblib.dump(model, 'external_functionalities/trained_model.pkl')
    joblib.dump(vectorizer, 'external_functionalities/vectorizer.pkl')
#model_trainer()

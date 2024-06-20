import joblib

model = joblib.load('external_functionalities/trained_model.pkl')

vectorizer = joblib.load('external_functionalities/vectorizer.pkl')


def make_predictions(interest):
  new_input = ", ".join(interest)
  new_input_vectorized = vectorizer.transform([new_input])
  predictions = model.predict(new_input_vectorized)
  skills_array = predictions.tolist()
  return skills_array[0].split(',')

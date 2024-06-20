import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv('external_functionalities/Online_Courses.csv')
df = df.dropna(subset=['Skills'])

df['Combined_Skills'] = df['Skills'].apply(lambda x: ' '.join(x.split(',')))


vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['Combined_Skills'])



def get_recommendations(input_skills, top_n=5):
    input_skills_str = ' '.join(input_skills)
    input_skills_vec = vectorizer.transform([input_skills_str])
    similarity_scores = cosine_similarity(input_skills_vec, X)
    top_indices = similarity_scores.argsort(axis=1)[:, -top_n:][0][::-1]
    recommended_courses = df.iloc[top_indices]['Title'].values
    courses = []
    id = 0
    for course in recommended_courses:
        courses.append({
            'id' : id,
            'course_name' : course,
            'course_url' : create_google_search_url(course)
        })
        id +=1
    
    return courses

def create_google_search_url(course_title):
        query = course_title.replace(" ", "+")
        google_search_url = f"https://www.google.com/search?q={query}"
        return google_search_url
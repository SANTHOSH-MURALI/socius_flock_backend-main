import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class JobRecommendationService:
    def __init__(self, csv_file):
        self.job_data = self.load_job_data(csv_file)
        self.vectorizer = TfidfVectorizer(stop_words='english')
    def load_job_data(self, csv_file):
        job_data = []
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                job_data.append(row)
        return job_data
        
    def recommend_jobs(self, user_interests):
        recommended_jobs = []
        job_descriptions = [job['Skills'] for job in self.job_data]
        self.vectorizer.fit(job_descriptions)
        user_interests_text = ' '.join(user_interests) 
        user_interests_vector = self.vectorizer.transform([user_interests_text])
        job_description_vectors = self.vectorizer.transform(job_descriptions)

        similarity_scores = cosine_similarity(user_interests_vector, job_description_vectors)[0]

        sorted_jobs_indices = sorted(range(len(similarity_scores)), key=lambda i: similarity_scores[i], reverse=True)

        for index in sorted_jobs_indices[:10]:
            job = self.job_data[index]
            recommended_jobs.append(job)
        return recommended_jobs
        
def get_job_recommendation(user_interests):
  job_recommendation_service = JobRecommendationService('external_functionalities/job_details.csv')
  recommended_jobs = job_recommendation_service.recommend_jobs(user_interests)
  response_body = []
  for job in recommended_jobs:
      response_body.append({
        'job_title':job['Job Title'],
        'job_link':job['job_link']
      })
  return response_body



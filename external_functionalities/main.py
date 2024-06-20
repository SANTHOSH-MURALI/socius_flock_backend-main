from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import time
import pandas as pd
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import linear_kernel
from external_functionalities.randomforest_model_trainer import model_trainer

def extract_job_details(job_div):
    job_title = job_div.find(class_='title').text.strip()
    company_name = job_div.find(class_='comp-name').text.strip()
    salary = job_div.find(class_='sal').text.strip()
    location = job_div.find(class_='locWdth').text.strip()
    job_description = job_div.find(class_='job-desc').text.strip()
    skills = [tag.text.strip() for tag in job_div.find_all(class_='tag-li')]
    job_link = job_div.find('a', class_='title')['href']
    return job_title, company_name, salary, location, job_description, skills, job_link
def scrape_naukri_jobs(num_pages=1):
    driver = webdriver.Chrome()

    with open('external_functionalities/job_details.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Job Title', 'Company Name', 'Salary', 'Location', 'Job Description', 'Skills','job_link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for page in range(1, num_pages + 1):
            url = f"https://www.naukri.com/jobs-in-india-{page}"
            driver.get(url)
            time.sleep(3)

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            job_divs = soup.find_all('div', class_='srp-jobtuple-wrapper')
            
            for job_div in job_divs:
                try:
                  job_title, company_name, salary, location, job_description, skills, job_link = extract_job_details(job_div)
                  writer.writerow({'Job Title': job_title, 'Company Name': company_name, 'Salary': salary, 'Location': location, 'Job Description': job_description, 'Skills': ', '.join(skills),'job_link':job_link})
                except Exception as e:
                  pass

    driver.quit()

def extract_skills_from_job_description(job_description):
    skills = [word.lower() for word in job_description.split()]
    return skills

def get_in_demand_skills(num_pages=1):
    scrape_naukri_jobs(num_pages)



def identify_top_skills(csv_file):
    with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        all_skills = []
        for row in reader:
            skills = row['Skills'].split(',')
            all_skills.extend([skill.strip() for skill in skills])

        skills_counter = Counter(all_skills)
        top_skills = skills_counter.most_common(20)
        return top_skills


    
def web_crawler_main():
    get_in_demand_skills(num_pages=50)
    df = pd.read_csv("external_functionalities/Online_Courses.csv")
    df = df[["Title", "URL", "Skills"]]
    csv_file = 'external_functionalities/job_details.csv' 
    top_skills = identify_top_skills(csv_file)
    skills = []
    for skill, count in top_skills:
        skills.append(skill)

    df.dropna(subset=['Skills'], inplace=True)

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['Skills'])

    X_train, X_test = train_test_split(tfidf_matrix, test_size=0.2, random_state=42)

    cosine_sim_train = linear_kernel(X_train, X_train)
    cosine_sim_test = linear_kernel(X_test, X_train)
    def recommend_courses(index, cosine_sim=cosine_sim_train):
        sim_scores = list(enumerate(cosine_sim[index]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11] 
        course_indices = [i[0] for i in sim_scores]
        return df.iloc[course_indices]

    index = 0 

    def create_google_search_url(course_title):
        query = course_title.replace(" ", "+")
        google_search_url = f"https://www.google.com/search?q={query}"
        return google_search_url
    recommendations = recommend_courses(index, cosine_sim=cosine_sim_test)

    with open('external_functionalities/today_job_trend_course.csv','w',newline='', encoding='utf-8') as job_trends:
      fieldnames = ['Title', 'Search_Url']
      writer = csv.DictWriter(job_trends, fieldnames=fieldnames)
      writer.writeheader()
      for title in recommendations['Title']:
        writer.writerow({'Title':title,'Search_Url':create_google_search_url(title)})
        
    ### add new skill combinations to the existing csv file
    job_details_df = pd.read_csv('external_functionalities/job_details.csv')
    skills_column = job_details_df['Skills']

    skills_df = pd.DataFrame({'Skills': skills_column})
    skills_df.to_csv('external_functionalities/sample_skills.csv', mode='a', header=False, index=False)
    model_trainer()
        
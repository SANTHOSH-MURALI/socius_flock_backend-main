from flask import request
from flask import Blueprint
from config import db
from common import response_functions,response_strings
from util.current_user import get_current_user
from models.models import Skills, User
import traceback
from external_functionalities.course_recommendation import get_recommendations as course_recommender
from external_functionalities.prediction import make_predictions
import random
from external_functionalities.job_recommendation import get_job_recommendation

user_route = Blueprint('user_route',__name__,url_prefix='/api/user')


@user_route.get("")
def user_details():
  try:
    session = db.session()
    session.begin()
    email = get_current_user()['email']
    user = session.query(User).filter(User.email == email).first()
    response_body = {
      'user_name' : user.name,
      'user_email' : user.email
    }
    session.commit()
    session.close()
    return response_functions.success_response_sender(data=response_body,message=response_strings.user_data_fetch_success)
  except Exception as e:
    traceback.print_exception(e)
    session.rollback()
    session.close()
    return response_functions.bad_request_sender(None,response_strings.invalid_data_string)
  
@user_route.get('/courses')
def get_recommended_courses():
  try:
    session = db.session()
    session.begin()
    email = get_current_user()['email']
    user = session.query(User).filter(User.email == email).first()
    skills = session.query(Skills).filter(Skills.user == user).order_by(Skills.updated_at.desc()).limit(5).all()
    if len(skills) < 5:
      session.rollback()
      session.close()
      return response_functions.not_found_sender(None,response_strings.should_have_five_skills)
    skills_formatted = [ skill.skill_name for skill in skills]
    final_predictions = set()
    result_list = []
    for skill in skills_formatted :
      result = make_predictions([skill])
      if result is None or len(result) <=2:
        continue
      random_range = random.randint(2,len(result))
      for temp in range(random_range):
        random_index = random.randint(0,len(result)-1)
        final_predictions.add(result[random_index])
      for element in final_predictions:
        result_list.append(element)
    session.commit()
    session.close()
    return response_functions.success_response_sender(course_recommender(result_list),response_strings.success_response)
  except Exception as e:
    session.rollback()
    session.close()
    traceback.print_exception(e)
    return response_functions.bad_request_sender(None,response_strings.invalid_data_string)
  
@user_route.get('/jobs')
def get_recommended_jobs():
  try:
    session = db.session()
    session.begin()
    email = get_current_user()['email']
    user = session.query(User).filter(User.email == email).first()
    skills = session.query(Skills).filter(Skills.user == user).order_by(Skills.updated_at.desc()).limit(5).all()
    if len(skills) < 5:
      session.rollback()
      session.close()
      return response_functions.not_found_sender(None,response_strings.should_have_five_skills)
    skills_formatted = [ skill.skill_name for skill in skills]
    session.commit()
    session.close()
    return response_functions.success_response_sender(get_job_recommendation(skills_formatted),response_strings.Data_fetched_succes)
  except Exception as e:
    session.rollback()
    session.close()
    print(e)
    return response_functions.bad_request_sender(None,response_strings.invalid_data_string)
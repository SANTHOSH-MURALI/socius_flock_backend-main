from flask import Blueprint, make_response,request
from marshmallow import ValidationError
from util import verify_data
from models.models import User,Activity
from common import response_strings,response_functions
from flask_jwt_extended import create_access_token,create_refresh_token
from util import session_genarator
import datetime
from validators import SignUp,Login
from config import db


auth_route = Blueprint('auth_route',__name__,url_prefix='/api/auth')


@auth_route.post('/signup')
def sign_up():
  sign_up_details = request.get_json()
  try:
    session = db.session()
    session.begin()
    SignUp.SigUp().load(sign_up_details)
    if verify_data.validate_signup_data(sign_up_details):
      user = session.query(User).filter(User.email == sign_up_details['email']).first()
      if user != None:
        return response_functions.conflict_error_sender(None,response_strings.data_already_exist_message)
      user = User(sign_up_details['name'],sign_up_details['email'],sign_up_details['password'])
      session.add(user)
      session.commit()
      session.rollback()
      return response_functions.created_response_sender(None,response_strings.user_created_success)
    else:
      return response_functions.bad_request_sender(None,response_strings.invalid_data_string) 
  except ValidationError as e:
    return response_functions.bad_request_sender(None,response_strings.invalid_data_string)
  except Exception as e:
    print(e)
    session.rollback()
    session.close()
    return response_functions.server_error_sender(None,response_strings.server_error_message)
        

@auth_route.post('/login')
def login():
  login_details = request.get_json()
  try:
    Login.Login().load(login_details)
    session = db.session()
    session.begin()
    if verify_data.validate_login_data(login_details):
      user = session.query(User).filter(User.email == login_details['email']).first()
      if user == None:
        return response_functions.not_found_sender(None,response_strings.user_not_found)
      session_id = session_genarator.get_random_id()
      if verify_data.validate_user_login(login_details,user):
        access_token = create_access_token(user.email,additional_claims={'session_id':session_id})
        refresh_token = create_refresh_token(user.email,additional_claims={'session_id':session_id})
        token_response = {
            'access_token':access_token,
            'refresh_token':refresh_token
         }
        user_activity = Activity(user)
        user_activity.session_id=session_id
        session.add(user_activity)
        session.commit()
        session.close()
        response = make_response(response_functions.success_response_sender(token_response, response_strings.user_login_success))
        response.set_cookie('access_token', access_token, httponly=True)
        response.set_cookie('refresh_token', refresh_token, httponly=True)
        return response
      else:
        return response_functions.forbidden_response_sender(None,response_strings.invalid_credentials)
    else:
      return response_functions.bad_request_sender(None,response_strings.invalid_data_string) 
  except Exception as e:
    session.rollback()
    session.close()
    return response_functions.bad_request_sender(None,response_strings.invalid_data_string)
        
@auth_route.get('/logout')
def logout():
  session = db.session()
  session.begin()
  session_id = request.headers['Session_Id']
  activity = session.query(Activity).filter(Activity.session_id == session_id).first()
  activity.logout_at = datetime.datetime.now()
  session.add(activity)
  session.commit()
  session.close()
  return response_functions.success_response_sender(None,response_strings.user_logout_success)


# @auth_route.get('/refresh')
# def refresh():
#   session_id = request.headers['Session_Id']
#   session = db.session()
#   session.begin()
#   activity = session.query(Activity).filter(Activity.session_id == session_id).first()
#   if activity != None and activity.logout_at == None:
#     user = activity.user
#     access_token = create_access_token(user.email,additional_claims={'session_id':session_id})
#     refresh_token = create_refresh_token(user.email,additional_claims={'session_id':session_id})
#     token_response = {
#       'access_token':access_token,
#       'refresh_token':refresh_token
#     }
#     session.commit()
#     session.close()
#     return response_functions.success_response_sender(token_response,response_strings.refresh_token_success)
#   else:
#     session.commit()
#     session.close()
#     return response_functions.forbidden_response_sender(None,response_strings.invalid_credentials)
  
  
  
# @auth_route.post('/create_role/<role_name>/')
# def create_role(role_name):
#   role = Role()
#   role.role_name = role_name
#   user_services.create_role(role)
#   return "Role Created",200

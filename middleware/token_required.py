from datetime import datetime
from datetime import timedelta
from flask import make_response, request
from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from common import response_strings,response_functions
from config import db
from models.models import Activity
from util.current_user import set_current_user,set_token

open_paths = [
    '/api/auth/signup',
    '/api/auth/login',
    '/favicon.ico'
]


def token_reqiured(*args,**kwargs):
  if request.method == 'OPTIONS' :
    return response_functions.success_response_sender(data=None,message="")
  if request.path in open_paths:
    pass
  else:
    session = db.session()
    access_token = request.cookies.get('access_token')
    refresh_token = request.cookies.get('refresh_token')
    if not access_token or not refresh_token:
          return response_functions.forbidden_response_sender(None, response_strings.invalid_credentials)
    try:
      access_token_data = None
      try:
        access_token_data = decode_token(access_token)
        current_time = datetime.utcnow()
        expiration_time = datetime.utcfromtimestamp(access_token_data['exp'])
        if expiration_time >= current_time - timedelta(minutes=10):
          raise Exception
        activity = Activity.query.filter(Activity.session_id == access_token_data['session_id'],Activity.logout_at == None).first()
        if activity == None:
          session.close()
          return response_functions.forbidden_response_sender(None, response_strings.invalid_credentials)
        set_current_user(activity=activity)
        set_token(access_token=access_token,refresh_token=refresh_token)
      except Exception as e:
        try:
          refresh_token_data = decode_token(refresh_token)
          activity = session.query(Activity).filter(Activity.session_id == refresh_token_data['session_id'],Activity.logout_at == None).first()
          if activity == None:
            session.close()
            return response_functions.forbidden_response_sender(None, response_strings.invalid_credentials)
          set_current_user(activity=activity)
          access_token_data = refresh_token_data
          set_token(access_token=create_access_token(identity=activity.user.email,additional_claims={'session_id':activity.session_id}),refresh_token=create_refresh_token(identity=activity.user.email,additional_claims={'session_id':activity.session_id}))
        except Exception as e:
          session.close()
          return response_functions.forbidden_response_sender(None, response_strings.invalid_credentials)
      session.close()
      request.environ['HTTP_USER_DATA'] = access_token_data['sub']
      request.environ['HTTP_SESSION_ID'] = access_token_data['session_id']
    except Exception as e:
        return response_functions.forbidden_response_sender(None, response_strings.invalid_credentials)
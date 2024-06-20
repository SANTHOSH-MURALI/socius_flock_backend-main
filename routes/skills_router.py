from flask import request, Blueprint
from config import db
from common import response_functions, response_strings
from util.current_user import get_current_user
from models.models import User, Skills
import traceback
from datetime import datetime

user_skill_route = Blueprint('user_skill_route', __name__, url_prefix='/api/skills')


@user_skill_route.route("", methods=['POST'])
def create_skill():
    try:
        email = get_current_user()['email']
        user = db.session.query(User).filter(User.email == email).first()
        
        skill_name = str(request.json.get('skill_name')).lower()
        if not skill_name:
            return response_functions.bad_request_sender(None, response_strings.invalid_data_string)
        exist = db.session.query(Skills).filter(Skills.skill_name == skill_name).first()
        if exist is not None:
          return response_functions.conflict_error_sender(None,response_strings.data_already_exist_message)
        skill = Skills(skill_name=skill_name, user=user)
        db.session.add(skill)
        db.session.commit()
        return response_functions.success_response_sender(None,message=response_strings.skill_created_success)
    except Exception as e:
        traceback.print_exception(e)
        db.session.rollback()
        return response_functions.server_error_sender(None,response_strings.server_error_message)
      
@user_skill_route.route("/update/<int:skill_id>", methods=['PUT'])
def update_skill(skill_id):
    try:
        email = get_current_user()['email']
        user = db.session.query(User).filter(User.email == email).first()
        skill = db.session.query(Skills).filter(Skills.id == skill_id, Skills.user == user).first()
        if not skill:
            return response_functions.not_found_sender(None, response_strings.data_not_found)
        skill_name = request.json.get('skill_name')
        if not skill_name:
            return response_functions.bad_request_sender(None, response_strings.invalid_data_string)
        skill.skill_name = skill_name
        skill.updated_at = datetime.utcnow()
        db.session.commit()
        return response_functions.success_response_sender(message=response_strings.update_message)
    except Exception as e:
        traceback.print_exception(e)
        db.session.rollback()
        return response_functions.server_error_sender(None,response_strings.server_error_message)


@user_skill_route.route("/delete/<int:skill_id>", methods=['DELETE'])
def delete_skill(skill_id):
    try:
        email = get_current_user()['email']
        user = db.session.query(User).filter(User.email == email).first()
        skill = db.session.query(Skills).filter(Skills.id == skill_id, Skills.user == user).first()
        if not skill:
            return response_functions.not_found_sender(None, response_strings.data_not_found)
        db.session.delete(skill)
        db.session.commit()
        return response_functions.success_response_sender(None,message=response_strings.skill_deleted_success)
    except Exception as e:
        traceback.print_exception(e)
        db.session.rollback()
        return response_functions.server_error_sender(None,response_strings.server_error_message)


@user_skill_route.route("/latest", methods=['GET'])
def latest_skills():
    try:
        email = get_current_user()['email']
        user = db.session.query(User).filter(User.email == email).first()
        latest_skills = (
            db.session.query(Skills)
            .filter(Skills.user == user)
            .order_by(Skills.updated_at.desc())
            .limit(5)
            .all()
        )
        skill_list = [{'skill_name' :skill.skill_name , "id" : skill.id} for skill in latest_skills]
        return response_functions.success_response_sender(data={'latest_skills': skill_list}, message=response_strings.Data_fetched_succes)
    except Exception as e:
        traceback.print_exception(e)
        return response_functions.server_error_sender(None,response_strings.server_error_message)
      

@user_skill_route.route("/all", methods=['post'])
def get_all_skills():
    try:
        email = get_current_user()['email']
        search = request.json['search_query']
        user = db.session.query(User).filter(User.email == email).first()
        latest_skills = None
        if search == '' :
          latest_skills = (
            db.session.query(Skills)
            .filter(Skills.user == user)
            .order_by(Skills.updated_at.desc())
            .all()
          )
        else :
          latest_skills = (
            db.session.query(Skills)
            .filter(Skills.user == user,Skills.skill_name.like(f'%{search}%'))
            .order_by(Skills.updated_at.desc())
            .all()
          )
        skill_list = [{'skill_name' :skill.skill_name , "id" : skill.id} for skill in latest_skills]
        return response_functions.success_response_sender(data={'skills': skill_list}, message=response_strings.Data_fetched_succes)
    except Exception as e:
        traceback.print_exception(e)
        return response_functions.server_error_sender(None,response_strings.server_error_message)
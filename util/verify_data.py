
import re
from config import bcrypt

email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def validate_signup_data(signup_data):
    name_pattern = r'^[a-zA-Z]+(?:\s[a-zA-Z]+)*$'
    if re.match(name_pattern,signup_data['name']) and re.match(email_pattern,signup_data['email']):
        return True
    else :
        return False
    
    
def validate_login_data(login_data):    
    if re.match(email_pattern,login_data['email']):
        return True
    return False

def validate_user_login(login_data,user_data):
    return bcrypt.check_password_hash(user_data.password,login_data['password'])

    
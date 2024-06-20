from flask import jsonify,make_response
from http import HTTPStatus
from util.current_user import get_token

response_body = {
    'data':{},
    'http_status':'',
    'message':''
}

def success_response_sender(data,message):
    return common_response_sender(data,message,HTTPStatus.OK)

def forbidden_response_sender(data,message):
    return common_response_sender(data,message,HTTPStatus.FORBIDDEN)

def bad_request_sender(data,message):
    return common_response_sender(data,message,HTTPStatus.BAD_REQUEST)

def not_found_sender(data,message):
    return common_response_sender(data,message,HTTPStatus.NOT_FOUND)

def created_response_sender(data,message):
    return common_response_sender(data,message,HTTPStatus.CREATED)

def server_error_sender(data,message):
    return common_response_sender(data,message,HTTPStatus.INTERNAL_SERVER_ERROR)

def conflict_error_sender(data,message):
    return common_response_sender(data,message,HTTPStatus.CONFLICT)
    
    
def common_response_sender(data,message,http_status:HTTPStatus):
    
    response_body['data'] = data
    response_body['http_status'] = http_status.phrase
    response_body['message'] = message
    response =  make_response(jsonify(response_body),http_status.value)
    try:
        token = get_token()  
        if token : 
            response.set_cookie('access_token', token['access_token'], httponly=True)
            response.set_cookie('refresh_token', token['refresh_token'], httponly=True)
    except Exception as e:
        pass
    return response
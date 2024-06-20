from contextvars import ContextVar
current_user: ContextVar[dict] = ContextVar('current_user')

token : ContextVar[dict] = ContextVar('token_requiring')

def set_current_user(activity) -> None:
    current_user.set({
      'email' : activity.user.email,
      'session_id' : activity.session_id,
    })
  
def get_current_user():
    return current_user.get()
  
def set_token(access_token,refresh_token) -> None:
  
  token.set({
    'access_token' : access_token,
    'refresh_token' : refresh_token
  })


def get_token():
  return token.get()

from config import db,bcrypt,jwt,Config
from flask import Flask
from routes import auth_router,user_router,skills_router
from middleware.token_required import token_reqiured
from flask_cors import CORS



def createapp():
  
  app = Flask(__name__)
  app.config.from_object(Config)
  app.secret_key = Config.APP_SECRET_KEY
  app.register_blueprint(auth_router.auth_route)
  app.register_blueprint(user_router.user_route)
  app.register_blueprint(skills_router.user_skill_route)
  CORS(app, supports_credentials=True, origins='*', allow_headers="*", always_send=True)
  app.before_request(token_reqiured)
  db.init_app(app=app)
  bcrypt.init_app(app=app)
  jwt.init_app(app=app)
  return app
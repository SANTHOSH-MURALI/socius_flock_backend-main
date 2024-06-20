import os
import dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

dotenv.load_dotenv()


class Config : 
  PORT = os.getenv('PORT')
  SQLALCHEMY_DATABASE_URI = os.getenv('MYSQL_DB_URL')
  APP_SECRET_KEY = os.getenv('SECRET_KEY')
  JWT_SECRET_KEY = os.getenv('APP_JWT_SECRET')
  JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))
  JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES'))
  
  
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
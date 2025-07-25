from os import environ
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = environ.get('mysql+pymysql://root:@localhost/sistema_ganadero_database')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = environ.get("SECRET_KEY")
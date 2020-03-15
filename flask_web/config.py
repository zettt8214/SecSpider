import os

class Config:
    SECRET_KEY="hard to guess string"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:root@127.0.0.1:3306/secinfo?charset=utf8'
    SECRET_KEY = "hard to guess string"


config={
    'development':DevelopmentConfig
}
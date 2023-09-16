import os

class Config:

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    LINE_PAY_ID = '2000604812'
    LINE_PAY_SECRET = '879668915dfffad250c16f2349c279f0'

    STORE_IMAGE_URL = 'https://i.imgur.com/Oxhenpw.jpg'

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://roylai:nXSYgQnSp2EZSoKq0H3TxXRIKpvZGqJg@dpg-cjbik5vdb61s738d8jm0-a.singapore-postgres.render.com/a_ewvc'
    
class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')



    

    


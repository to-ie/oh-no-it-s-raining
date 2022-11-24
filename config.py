import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # change secret key for production    
    SECRET_KEY = os.environ.get('SECRET_KEY') or '4JB3&9o1cXl6gi2KUXdtKC@$o9T0'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # include the mail server here 
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    # change the inbox credentials below
    MAIL_USERNAME = os.environ.get('your@email.address')
    MAIL_PASSWORD = os.environ.get('yourpassword')
    # change admin email address here
    ADMINS = ['admin@email.address']
    POSTS_PER_PAGE = 10
    
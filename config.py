import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # change secret key for production
    SECRET_KEY = os.environ.get('SECRET_KEY') or '4JB3&9o1cXl6gi2KUXdtKC@$o9T0'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # include the mail server here
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = int(587)
    MAIL_USE_TLS = True
    # change the inbox credentials below
    MAIL_USERNAME = 'ohnoitsrainingdublin@gmail.com'
    MAIL_PASSWORD = 'khiaqbacyceimeth'
    # change admin email address here
    ADMINS = ['ohnoitsrainingdublin@gmail.com']
    POSTS_PER_PAGE = 10

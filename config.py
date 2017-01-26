import os
basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = "how-do-you-know"

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = ('sqlite:///' + os.path.join(basedir, 'app.db') +
                               '?check_same_thread=False')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

BWITS_PER_PAGE = 3
TEMPLATES_AUTO_RELOAD = True
SQLALCHEMY_TRACK_MODIFICATIONS = True

FB_KEY = os.environ.get('FB_SECRET_KEY')
# Auth
OAUTH_CREDENTIALS = {
    'facebook': {
        'id': '240571076396508',
        'secret': FB_KEY
    }
}

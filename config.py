import os
basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = "how-do-you-know"

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

BWITS_PER_PAGE = 3
TEMPLATES_AUTO_RELOAD = True
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Auth
OAUTH_CREDENTIALS = {
    'facebook': {
        'id': '240571076396508',
        'secret': '14d71ee085d3e78a3615f1125bc22af8'
    }
}

from app import db
from hashlib import md5
from datetime import datetime

followers = db.Table(
    'followers', db.Column('follower_id', db.Integer, db.ForeignKey('user.id')), db.Column('followed_id', db.Integer, db.ForeignKey('user.id')))


class User(db.Model):
    # User Registration Info
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column('email', db.String(120), unique=True, index=True)
    profile_picture = db.Column(db.String(1000))

    # Bwitter Info
    bwits = db.relationship('Bwit', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    followed = db.relationship('User', secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')

    @staticmethod
    def make_unique_nickname(nickname):
        if (User.query.filter_by(nickname=nickname).first() is None):
            return nickname
        version = 2
        while (True):
            new_nickname = nickname + str(version)
            if (User.query.filter_by(nickname=new_nickname).first() is None):
                break
            version += 1
        return new_nickname

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    def avatar(self, size):
        return('http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size))

    def first_name(self, nickname):
        # split at space in name
        name = nickname.split(' ')
        return name[0]

    def follow(self, user):
        if (not self.is_following(user)):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if (self.is_following(user)):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return (self.followed.filter(
            followers.c.followed_id == user.id).count() > 0)

    def followed_bwits(self):
        return Bwit.query.join(followers, (
            followers.c.followed_id == Bwit.user_id)).filter(followers.c.follower_id == self.id).order_by(Bwit.timestamp.desc())

    def __repr__(self):
        return '<User %r>' % (self._username)


class Bwit(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr(self):
        return '<Bwit %r>' % (self.body)

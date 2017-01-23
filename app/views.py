from flask import session, request, flash, url_for, redirect
from flask import render_template, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import EditForm, BwitForm, LoginForm
from .models import User, Bwit
from datetime import datetime
from config import BWITS_PER_PAGE
from .oauth import OAuthSignIn


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
@login_required
def index(page=1):
    form = BwitForm()
    if (form.validate_on_submit()):
        bwit = Bwit(body=form.bwit.data, timestamp=datetime.utcnow(),
                    author=g.user)
        db.session.add(bwit)
        db.session.commit()
        flash('Your bwit is now live!')
        return redirect(url_for('index'))
    bwits = g.user.followed_bwits().paginate(1, BWITS_PER_PAGE, False)
    return render_template('index.html', user=user, bwits=bwits, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        pass
    return render_template('login.html', title="Sign in",
                           form=form)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


def after_login(resp):
    if ((resp.email is None) or (resp.email == '')):
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()

    if (user is None):
        nickname = resp.nickname
        if ((nickname is None) or (nickname == '')):
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False

    if ('remember_me' in session):
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))


@app.before_request
def before_request():
    g.user = current_user
    if (g.user.is_authenticated):
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user._get_current_object())
        db.session.commit()


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email, profile_picture = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email,
                    profile_picture=profile_picture)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<nickname>')
@app.route('/user/<nickname>/<int:page>')
@login_required
def user(nickname, page=1):
    user = User.query.filter_by(nickname=nickname).first()
    if (user is None):
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    bwits = user.bwits.paginate(page, BWITS_PER_PAGE, False)
    return render_template('user.html', user=user, bwits=bwits)


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm(g.user.nickname)
    if (form.validate_on_submit()):
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form=form)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.route('/follow/<nickname>')
@login_required
def follow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if (user is None):
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))

    if (user == g.user):
        flash('You can\'t follow yourself!')
        return redirect(url_for('user', nickname=nickname))
    u = g.user.follow(user)

    if (u is None):
        flash('Cannot follow ' + nickname + '.')
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You are now following ' + nickname + '!')
    return redirect(url_for('user', nickname=nickname))


@app.route('/unfollow/<nickname>')
@login_required
def unfollow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if (user is None):
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))

    if (user == g.user):
        flash('You can\'t unfollow yourself!')
        return redirect(url_for('user', nickname=nickname))
    u = g.user.unfollow(user)

    if (u is None):
        flash('Cannot unfollow ' + nickname + '.')
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You have stopped following ' + nickname + '.')
    return redirect(url_for('user', nickname=nickname))

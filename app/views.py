from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm

user = {'nickname': 'Chintan'}  # fake user


@app.route('/')
@app.route('/index')
def index():
    bwits = [   # fake list of bwits
        {
            'user': {'nickname': 'John'},
            'bwit': 'Beautiful day in Portland!'
        },
        {
            'user': {'nickname': 'Susan'},
            'bwit': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', user=user, bwits=bwits)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.date)))
        return redirect('/index')
    return render_template('login.html', user=user, title="Sign in",
                           form=form, providers=app.config['OPENID_PROVIDERS'])

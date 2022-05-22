from flask import render_template, flash, redirect, url_for, request,jsonify
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User,gameRecord

import random


@app.route('/')
def hello():
    return render_template('hello.html',title='Hello!')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('game'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('game')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/game')
@login_required
def game():
    score_val = random.randint(1,100)
    return render_template('game1.html', title='Home', num_times='10',score_val=score_val)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/record')
def record():
    data = json.loads(request.form.get('data'))
    user_name = data["username"]
    chance_remain = data["chance_remain"]
    is_success = data["is_success"]
    gRecord = gameRecord(user_name=user_name,chance_remain=chance_remain,is_success=is_success)
    db.session.add(gRecord)
    db.session.commit()
    return

@app.route('/user/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    records = gameRecord.query.all()
    posts = [
        {'author': user, 'record': records},
        {'author': user, 'record': records}
    ]
    return render_template('profile.html', user=user,posts=posts)
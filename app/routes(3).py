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
            print(form.password.data)
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
        # print(User.username)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/record', methods=['GET'])
def record():
    username = request.args.get('username', '')
    is_success = request.args.get('is_success', '')
    if is_success == "false":
        is_success = False
    else:
        is_success = True
    chance_remain = request.args.get('chance_remain', '')
    print(username)
    print(is_success)
    print(chance_remain)
    gRecord = gameRecord(user_name=username,chance_remain=chance_remain,is_success=is_success)
    db.session.add(gRecord)
    db.session.commit()
    return render_template('game1.html', title='Home')

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

@app.route('/rank_list', methods=['GET'])
def rank_list():
    gr = gameRecord.query.order_by('user_name').all()
    un_list = []
    rate_list = []
    sign_val = 0
    for i in gr:
        if i.user_name not in un_list and sign_val == 0:
            true_time = 0
            false_time = 0
            un_list.append(i.user_name)
            if i.is_success:
                true_time+=1
            else:
                false_time+=1
        elif i.user_name not in un_list and sign_val != 0:
            if true_time !=0:
                rate_list.append(round(true_time/(true_time+false_time),2))
            else:
                rate_list.append(0.0)
            true_time = 0
            false_time = 0
            un_list.append(i.user_name)

        if i.is_success:
            true_time+=1
        else:
            false_time+=1
        sign_val+=1
        if sign_val == len(gr):
            if true_time !=0:
                rate_list.append(round(true_time/(true_time+false_time),2))
            else:
                rate_list.append(0.0)

    print(rate_list)
    rate_list, un_list = quick_sort(rate_list,un_list,0,len(rate_list)-1)

    for i in range(len(rate_list)):
        rate_list[i] = str(rate_list[i]*100)+"%"

    res_data = { 'un_list':un_list,'rate_list':rate_list}
    return jsonify(res_data)


def quick_sort(array1,array2,start,end):
    if start>end:
        return array1,array2
    mid_data,left,right = array1[start],start,end
    while left<right:
        while array1[right] <= mid_data and left <right:
            right -=1
        array1[left] = array1[right]
        array2[left] = array2[right]
        while array1[left] >= mid_data and left < right:
            left += 1
        array1[right] = array1[left]
        array2[right] = array2[left]
    array1[left] = mid_data
    quick_sort(array1,array2,start,left-1)
    quick_sort(array1,array2,left+1,end)
    return array1, array2
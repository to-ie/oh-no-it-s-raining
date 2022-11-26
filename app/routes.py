from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, ActivityForm
from app.models import User
from datetime import datetime
from app.forms import ActivityForm, EmptyForm
from app.models import Activity, Area, Bookmark
from app.forms import ResetPasswordRequestForm
from app.email import send_password_reset_email
from app.forms import ResetPasswordForm

@app.route('/')
@app.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    activities = Activity.query.order_by(Activity.timestamp.desc()).paginate(
        page=page, per_page=5, error_out=False)
    return render_template('index.html', title='Home', activities=activities)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # if the user is already authenticated, redirect the user to the 
        # members page. 
        return redirect(url_for('member'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(usernamelowercase=form.username.data.lower()).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('member'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, 
            emaillowercase=form.email.data.lower(), usernamelowercase=form.username.data.lower())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('member'))
    return render_template('register.html', title='Register', form=form)

@app.route('/member')
@login_required
def member():
    page = request.args.get('page', 1, type=int)
    activities = Activity.query.order_by(Activity.timestamp.desc()).paginate(
        page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('member', page=activities.next_num) \
        if activities.has_next else None
    prev_url = url_for('member', page=activities.prev_num) \
        if activities.has_prev else None
    return render_template("member.html", title='Explore', activities=activities.items,
                          next_url=next_url, prev_url=prev_url)

@app.route('/suggest', methods=['GET', 'POST'])
@login_required
def suggest():
    form = ActivityForm()
    if form.validate_on_submit():
        activity = Activity(title=form.activitytitle.data, 
            body=form.activitybody.data, location=form.activitylocation.data, 
            author=current_user)
        db.session.add(activity)
        db.session.commit()
        flash('Your suggested activity is now live!')
        return redirect(url_for('member'))
    return render_template("suggestion.html", title='Suggest an activity', 
        form=form)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)
    
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    if current_user == user:      
        return render_template('user.html', user=user)
    elif current_user != user:
        flash("You can't access this page.")
        return redirect(url_for('user', username=current_user.username))

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

from app.forms import EditProfileForm

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username, current_user.email)
    if form.validate_on_submit():
        current_user.username = form.username.data 
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    activities = Activity.query.order_by(Activity.timestamp.desc()).all()
    return render_template('edit_profile.html', title='Edit Profile', form=form,
        activities=activities)

@app.route('/activity/<activityid>')
@login_required
def activitypage(activityid):
    activitypage = Activity.query.filter_by(id=activityid).first_or_404()
    activities = Activity.query.filter_by(id=activityid).all()
    return render_template('activity.html', id=activityid,
        activityid = activityid, activitypage=activitypage)

from app.forms import EditActivityForm

@app.route('/edit_activity/<activityid>', methods=['GET', 'POST'])
@login_required
def edit_activity(activityid):
    form = EditActivityForm()
    currentactivity = Activity.query.filter_by(id=activityid).first_or_404()
    if current_user == currentactivity.author:
        if form.validate_on_submit():
            currentactivity.title = form.activitytitle.data
            currentactivity.location = form.activitylocation.data
            currentactivity.body = form.activitybody.data
            db.session.commit()
            flash('Your changes have been saved.')
            return redirect(url_for('activitypage', activityid=activityid))
        elif request.method == 'GET':
            form.activitytitle.data = currentactivity.title
            form.activitylocation.data = currentactivity.location
            form.activitybody.data = currentactivity.body   
    elif current_user != currentactivity.author:
        flash("You can't edit this activity as you did not create it.")
        return redirect(url_for('user', username=current_user.username))
    return render_template('edit_activity.html', title='Edit Activity', user=user,
        form=form)

@app.route('/delete_activity/<activityid>', methods=['GET', 'POST'])
@login_required
def delete_activity(activityid):
    currentactivity = Activity.query.filter_by(id=activityid).first_or_404()
    if current_user == currentactivity.author:
        db.session.delete(currentactivity)
        db.session.commit()
        flash('Your activity was deleted.')
        return redirect(url_for('user', username=current_user.username))
    elif current_user != currentactivity.author:
        flash("You can't delete this activity as you did not create it.")
        return redirect(url_for('posted', username=current_user.username))

@app.route('/bookmark/<activityid>', methods=['GET', 'POST'])
@login_required
def bookmark(activityid):
    form = EmptyForm()
    bookmark = Bookmark.query.filter_by(user_id=current_user.id).filter_by(
        activity_id=activityid).first()

    if bookmark:
        flash('This activity is already saved in your profile.')
        return redirect(url_for('activitypage', activityid = activityid)) 
    else: 
        addbookmark = Bookmark(user_id=current_user.id, activity_id=activityid)
        db.session.add(addbookmark)
        db.session.commit()
        flash('This activity is now saved in your profile.')

    return redirect(url_for('activitypage', activityid = activityid))

@app.route('/posted/<username>')
@login_required
def posted(username):
    user = User.query.filter_by(username=username).first_or_404()
    if current_user == user:
        page = request.args.get('page', 1, type=int)
        activities = Activity.query.filter_by(author=user).order_by(Activity.timestamp.desc()).paginate(
            page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)
        next_url = url_for('posted', username=current_user.username, page=activities.next_num) \
            if activities.has_next else None
        prev_url = url_for('posted', username=current_user.username, page=activities.prev_num) \
            if activities.has_prev else None        
        return render_template('posted_activities.html', user=user, activities=activities.items,
            next_url=next_url, prev_url=prev_url)
    elif current_user != user:
        flash("You can't access this page.")
        return redirect(url_for('posted', username=current_user.username))

@app.route('/saved/<username>')
@login_required
def saved(username):
    user = User.query.filter_by(username=username).first_or_404()
    bookmarkactivityid = Bookmark.query.filter_by(user_id=user.id)
    activities = Activity.query.filter_by(author=user).order_by(Activity.timestamp.desc())
    # ---
    # This one works
    # activities = Activity.query.filter_by(author=user).order_by(Activity.timestamp.desc())
    # ----
    return render_template('saved_activities.html', user=user, activities=activities)




## TODO
## If not your user no access 
## Pagination
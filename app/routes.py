from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, ActivityForm
from app.forms import ActivityForm, EmptyForm, EditProfileAdminForm
from app.forms import ResetPasswordRequestForm, Filter, ResetPasswordForm
from app.models import Activity, Area, Bookmark
from app.models import User
from datetime import datetime
from app.email import send_password_reset_email

@app.route('/')
@app.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    activities = Activity.query.filter_by(moderation = "0").order_by(
        Activity.timestamp.desc()).paginate(page=page, per_page=5, 
        error_out=False)
    return render_template('index.html', title='Home', activities=activities)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # if the user is already authenticated, redirect the user to the 
        # members page. 
        return redirect(url_for('member'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(usernamelowercase=form.username.data
            .lower()).first()
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
            emaillowercase=form.email.data.lower(), usernamelowercase=
            form.username.data.lower())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('member'))
    return render_template('register.html', title='Register', form=form)

@app.route('/member', methods=['GET', 'POST'])
@login_required
def member():
    form = Filter()
    # filters
    if form.validate_on_submit():
        location=form.activitylocation.data
        activities = Activity.query.filter_by(moderation = "0").filter_by(
            location=location).order_by(Activity.timestamp.desc())   
        
        # return redirect('filter', activities=activities)
        return render_template('member.html', activities=activities, 
            form = form,location=location)

    #show activities
    page = request.args.get('page', 1, type=int)
    activities = Activity.query.filter_by(moderation = "0").order_by(
        Activity.timestamp.desc()).paginate(page=page, per_page=
        app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('member', page=activities.next_num) \
        if activities.has_next else None
    prev_url = url_for('member', page=activities.prev_num) \
        if activities.has_prev else None


    return render_template("member.html", title='Explore', activities=
        activities.items, next_url=next_url, prev_url=prev_url, form=form)


# @app.route('/filter/', methods=['GET'])
# @login_required
# def filter():
#     #show activities
#     # location = activity.location
#     activities = Activity.query.filter_by(moderation = "0").filter_by(
#         location=location).order_by(Activity.timestamp.desc())    
#     return render_template('filter.html', activities=activities)

    # page = request.args.get('page', 1, type=int)
    # activities = Activity.query.filter_by(moderation = "0").filter_by(
    #     location=location).order_by(Activity.timestamp.desc()).paginate(
    #     page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    # next_url = url_for('member', page=activities.next_num) \
    #     if activities.has_next else None
    # prev_url = url_for('member', page=activities.prev_num) \
    #     if activities.has_prev else None
    # return render_template("filter.html", title='Explore', activities=
    #     activities.items, next_url=next_url, prev_url=prev_url)




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
        flash('Your suggested activity is pending review. It will be live \
            soon.')
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
    elif current_user.admin == 1:
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
    return render_template('edit_profile.html', title='Edit Profile', form=form)

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
    if current_user == currentactivity.author or current_user.admin == 1:
        if form.validate_on_submit():
            currentactivity.title = form.activitytitle.data
            currentactivity.location = form.activitylocation.data
            currentactivity.body = form.activitybody.data
            currentactivity.moderation = 1
            db.session.commit()
            flash('Your changes have been saved. Your activity is being \
                reviewed and will be live shortly.')
            return redirect(url_for('activitypage', activityid=activityid))
        elif request.method == 'GET':
            form.activitytitle.data = currentactivity.title
            form.activitylocation.data = currentactivity.location
            form.activitybody.data = currentactivity.body   
    elif current_user != currentactivity.author:
        flash("You can't edit this activity as you did not create it.")
        return redirect(url_for('user', username=current_user.username))
    return render_template('edit_activity.html', title='Edit Activity', 
        user=user, form=form)

@app.route('/delete_activity/<activityid>', methods=['GET', 'POST'])
@login_required
def delete_activity(activityid):
    currentactivity = Activity.query.filter_by(id=activityid).first_or_404()
    if current_user == currentactivity.author or current_user.admin == 1:
        db.session.delete(currentactivity)
        # Delete any entries that are bookmarked by other users
        bookmark_to_delete = Bookmark.query.filter_by(
            activity_id=activityid).all()
        for b in bookmark_to_delete:
            db.session.delete(b)
        db.session.commit()
        flash('Your activity was deleted.')
        return redirect(url_for('user', username=current_user.username))
    elif current_user != currentactivity.author:
        flash("You can't delete this activity as you did not create it.")
        return redirect(url_for('posted', username=current_user.username))

@app.route('/bookmark/<activityid>', methods=['GET', 'POST'])
@login_required
def bookmark(activityid):
    # bookmark a specific activity and save it to the Bookmark table
    form = EmptyForm()
    bookmark = Bookmark.query.filter_by(user_id=current_user.id).filter_by(
        activity_id=activityid).first()
    if bookmark:
        flash('This activity is already saved in your profile.')
    else: 
        addbookmark = Bookmark(user_id=current_user.id, activity_id=activityid)
        db.session.add(addbookmark)
        db.session.commit()
        flash('This activity is now saved in your profile.')
    return redirect(url_for('activitypage', activityid = activityid, 
        bookmark=bookmark))

@app.route('/removebookmark/<activityid>', methods=['GET', 'POST'])
@login_required
def removebookmark(activityid):
    form = EmptyForm()
    bookmark_to_remove = Bookmark.query.filter_by(user_id=
        current_user.id).filter_by(activity_id=activityid).first()
    if bookmark_to_remove:
        b = Bookmark.query.filter_by(user_id=current_user.id).filter_by(
            activity_id=activityid).first()
        db.session.delete(b)
        db.session.commit()
        flash('This activity is now removed from your list.')
    else: 
        flash("This activity is not on your 'save for later' list and \
            can't be removed.")
    return redirect(url_for('activitypage', activityid = activityid, 
        bookmark_to_remove=bookmark_to_remove))

@app.route('/posted/<username>')
@login_required
def posted(username):
    user = User.query.filter_by(username=username).first_or_404()
    if current_user == user:
        page = request.args.get('page', 1, type=int)
        activities = Activity.query.filter_by(author=user).order_by(
            Activity.timestamp.desc()).paginate(
            page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)
        next_url = url_for('posted', username=current_user.username, 
            page=activities.next_num) \
            if activities.has_next else None
        prev_url = url_for('posted', username=current_user.username, 
            page=activities.prev_num) \
            if activities.has_prev else None        
        return render_template('posted_activities.html', user=user, 
            activities=activities.items,
            next_url=next_url, prev_url=prev_url)
    elif current_user != user:
        flash("You can't access this page.")
        return redirect(url_for('posted', username=current_user.username))

@app.route('/saved/<username>')
@login_required
def saved(username):
    user = User.query.filter_by(username=username).first_or_404()
    if current_user == user:
        page = request.args.get('page', 1, type=int)
        # this is cool, merging the two tables to find the relevant bookmarked 
        # activities.
        activities = Activity.query.join(Bookmark, (Bookmark.activity_id == 
            Activity.id)).filter(Bookmark.user_id == user.id).filter(
        Activity.moderation == 0).order_by(Activity.timestamp.desc()).paginate(
            page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)
        next_url = url_for('saved', username=current_user.username, 
            page=activities.next_num) \
            if activities.has_next else None
        prev_url = url_for('saved', username=current_user.username, 
            page=activities.prev_num) \
            if activities.has_prev else None        
        return render_template('saved_activities.html', user=user, 
            activities=activities.items,
            next_url=next_url, prev_url=prev_url)
    elif current_user != user:
        flash("You can't access this page.")
        return redirect(url_for('username', username=current_user.username))
    return render_template('saved_activities.html', user=user, 
        activities=activities)

@app.route('/admin/users', methods=['GET', 'POST'])
@login_required
def adminusermanagement():
    if current_user.admin == 1:
        users = User.query.order_by(User.id.asc())
    else: 
        flash('This is a restricted area.')
        return redirect(url_for('index'))
    return render_template("user_management.html", title='User management', 
        users=users)

@app.route('/edit_profile_admin/<username>', methods=['GET', 'POST'])
@login_required
def edit_profile_admin(username):
    if current_user.admin == 1:
        user = User.query.filter_by(username=username).first()
        form = EditProfileAdminForm(user_username=user.username, 
            user_email=user.email)
        if form.validate_on_submit():
            user.username = form.username.data
            user.email = form.email.data
            user.about_me = form.about_me.data
            db.session.commit()
            flash('Your changes have been saved.')
            return redirect(url_for('user', username=user.username))
        elif request.method == 'GET':
            form.username.data = user.username
            form.email.data = user.email
            form.about_me.data = user.about_me
        return render_template('edit_profile_admin.html', title='Edit Profile', 
            username=username, form=form)
    else:
        flash('This is a restricted area.')
        return redirect(url_for('index'))

@app.route('/makeadmin/<username>', methods=['GET', 'POST'])
@login_required
def makeadmin(username):
    if current_user.admin == 1:
        users = User.query.order_by(User.id.asc())
        user = User.query.filter_by(username=username).first()
        form = EmptyForm()
        if username == current_user.username:
            flash("You can't remove admin rights for your own user. What if you\
             were the last admin?")
            return redirect(url_for('adminusermanagement'))
        else:
            if user.admin == 1:
                user.admin = 0
                db.session.commit()
                flash('Your changes have been saved: the user is no longer an \
                    admin.')
                return redirect(url_for('adminusermanagement'))
            else:
                user.admin = 1
                db.session.commit()
                flash('Your changes have been saved: the user is now an admin.')
                return redirect(url_for('adminusermanagement'))
            return redirect(url_for('adminusermanagement'))
    else: 
        flash('This is a restricted area.')
        return redirect(url_for('index'))

@app.route('/delete/<username>', methods=['GET', 'POST'])
@login_required
def deleteuser(username):
    form = EmptyForm()
    if current_user.admin == 1:
        user = User.query.filter_by(username = username).first()
        
        if user:
            # activities posted by user
            activitites_user_delete = user.activity.all()
            
            # bookmarks by the user 
            activities_bookmarked_user = Bookmark.query.filter_by(
                user_id = user.id).all()

            # delete bookmarked activities made by user by other  
            if activitites_user_delete:
                for a in activitites_user_delete:
                    t = a.id
                    o = Bookmark.query.filter_by(activity_id = t).first()
                    if o:
                        db.session.delete(o)
            
            # delete activities posted by user       
            if activitites_user_delete:
                for b in activitites_user_delete:
                    db.session.delete(b)

            # delete user's bookmarks
            for c in activities_bookmarked_user:
                db.session.delete(c)

            db.session.delete(user)
            db.session.commit()
        else: 
            flash('This user does not exist.')
    else: 
        flash('This is a restricted area.')
        return redirect(url_for('index'))
    return redirect(url_for('adminusermanagement'))

@app.route('/admin/moderation', methods=['GET', 'POST'])
@login_required
def adminmorderation():
    if current_user.admin == 1:
        activities = Activity.query.order_by(
            Activity.moderation.desc()).order_by(Activity.timestamp.desc())
    else: 
        flash('This is a restricted area.')
        return redirect(url_for('index'))
    return render_template("moderation.html", title='Activity moderation', 
        activities=activities)

@app.route('/admin/<activityid>', methods=['GET', 'POST'])
@login_required
def moderateactivity(activityid):
    if current_user.admin == 1:
        activity = Activity.query.filter_by(id=activityid).first()
        form = EmptyForm()
        if activity.moderation == 1:
            activity.moderation = 0
            db.session.commit()
            flash('Your changes have been saved: the activity is now live.')
            return redirect(url_for('adminmorderation'))
        else:
            activity.moderation = 1
            db.session.commit()
            flash('Your changes have been saved: the activity is marked for \
                moderation.')
            return redirect(url_for('adminmorderation'))
        return redirect(url_for('adminmorderation'))
    else: 
        flash('This is a restricted area.')
        return redirect(url_for('index'))

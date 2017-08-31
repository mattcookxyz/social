from flask import Flask, g, render_template, flash, redirect, url_for
from flask_login import (LoginManager, login_user, logout_user,
                                            login_required, current_user)
from flask_bcrypt import check_password_hash
import models, forms


DEBUG = True
PORT = 5000
HOST = '0.0.0.0'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'development'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view == 'login'


@login_manager.user_loader
def load_user(user_id):
    '''Return user object passed into user_loader function.'''
    try:
        return models.User.get(id=user_id)
    except models.DoesNotExist:
        return None
    except Exception as e:
        return e


@app.before_request
def before_request():
    '''Connect to database before each request.'''
    g.db = models.db
    g.db.get_conn()


@app.after_request
def after_request(response):
    '''Disconnect from database after each request.'''
    g.db.close()
    return response


@app.route('/')
def index():
    '''Homepage. Index if logged out, feed if logged in.'''
    if current_user.is_authenticated:
        return render_template('feed.html')
    else:
        return render_template('index.html')


@app.route('/user/<username>')
def view_profile(username):
    '''Display user profile for a given username.'''
    user = models.User.get(models.User.username == username)
    profile = models.Profile.get(models.Profile.user == user)
    return render_template('profile.html', user=user, profile=profile)


@app.route('/user/<username>/editprofile', methods=('GET', 'POST'))
@login_required
def edit_profile(username):
    '''Edit user profile.'''
    form = forms.ProfileForm()
    user = models.User.get(models.User.username == username)
    profile = models.Profile.get(models.Profile.user == user)

    # Update fields, redirect to view updated profile.
    if current_user == user and form.validate_on_submit():
        if form.about.data:
            profile.about = form.about.data
        if form.twitter.data:
            profile.twitter = form.twitter.data
        if form.facebook.data:
            profile.facebook = form.facebook.data
        if form.instagram.data:
            profile.instagram = form.instagram.data
        profile.save()
        return redirect(url_for('view_profile', username = username))

    # Show edit profile form if authenticated as the correct user.
    if current_user == user:
        return render_template('editprofile.html', form=form)

    # Wrong user tries to access edit page.
    else:
        return "Nice try, but that's not your profile bruh."


@app.route('/register', methods=('GET', 'POST'))
def register():
    '''Show registration form for a new user.'''
    form = forms.RegisterForm()

    # POST
    if form.validate_on_submit():
        flash("You have successfully registered.", "success")
        models.User.create_user(
            username=str(form.username.data),
            email=str(form.email.data),
            password=str(form.password.data))
        user = models.User.get(models.User.username == form.username.data)
        models.Profile.create(user=user)
        return redirect(url_for('login'))

    # Otherwise, GET
    return render_template('register.html', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    '''Show login form.'''

    form = forms.LoginForm()

    # POST
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your e-mail or password did not match our records.",
                    "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You are now logged in, " + user.username
                        + "!", "success")
                return redirect(url_for('index'))
            else:
                flash("Your e-mail or password did not match our records.",
                        "error")

    # Otherwise, GET
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    '''Logout user.'''
    logout_user()
    flash("You've been logged out. Come back soon!", "success")
    return redirect(url_for('index'))


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, host=HOST, port=PORT)

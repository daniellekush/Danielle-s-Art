from flask import render_template, flash, request, redirect, url_for, session
from flask_login import login_user, login_required, current_user, logout_user
from . import app, db, models
from .forms import newSuggestionForm, newLoginForm
from werkzeug.security import generate_password_hash, check_password_hash

app.secret_key = '693de3d4edc66bcdbeda97f23f0a554cbbe6a6351d30efad4ff1437ec1f4949a'

#Path to the Home page
@app.route('/')
def home():
	app.logger.debug("Entered Home page")
	return render_template('Home.html', title='Home', disclaimer=True)

#Path to the DC page
@app.route('/dc')
def dc():
	app.logger.debug("Entered DC page")
	return render_template('DC.html', title='DC', images=True)

#Path to the Logos page
@app.route('/logos')
def logos():
	app.logger.debug("Entered Logos page")
	return render_template('Logos.html', title='Logos', images=True)

#Path to the SignUp page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
        form = newLoginForm()
        app.logger.debug("Entered SignUp page")
        if form.validate_on_submit():
                app.logger.debug("Logged username: %s Logged password: %s", form.username.data, form.password.data)
                exists = models.User.query.filter_by(username=form.username.data).first()
                if exists:
                        flash('This username already exists.', 'error')
                else:
                        user = models.User(username=form.username.data, password=generate_password_hash(form.password.data, method='sha256'))
                        db.session.add(user)
                        db.session.commit()
                        app.logger.info("%s signed up", form.username.data)
                        return redirect(url_for('login'))
        return render_template('Login.html', form=form, title='Sign Up')

#Path to the Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
        form = newLoginForm()
        app.logger.debug("Entered Login page")
        if form.validate_on_submit():
                user = models.User.query.filter_by(username=form.username.data).first()
                app.logger.debug("Attempted login - username: %s password: %s", form.username.data, form.password.data)
                if not user:
                      app.logger.warning("Login attempt for non-existing user %s", form.username.data)
                      flash('This user does not exist.', 'error')
                elif check_password_hash(user.password, form.password.data):
                      login_user(user, remember=True)
                      app.logger.info("%s logged in successfully", form.username.data)
                      return redirect(url_for('home'))
                else:
                      app.logger.info("%s failed to login", form.username.data)
                      flash('Incorrect password.', 'error')
        return render_template('Login.html', form=form, title='Login')

#Path to the Account page
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
        app.logger.debug("Entered Account page")
        form = newLoginForm()
        if form.validate_on_submit():
                if (form.username.data == current_user.username):
                        user = models.User.query.filter_by(username=current_user.username).first()
                        password = generate_password_hash(form.password.data, method='sha256')
                        user.password = password
                        db.session.commit()
                        app.logger.info("%s changed their password", current_user.username)
                        flash('You have successfully changed your password!')
                else:
                        app.logger.debug("Attempt at changing password without verifying username correctly")
                        flash('Your username is not correct. Please verify your username to change your password.', 'error')
        return render_template('Account.html', form=form)
#Log out of account
@app.route('/logout')
@login_required
def logout():
        app.logger.info("%s logged out", current_user.username)
        logout_user()
        return redirect(url_for('home'))

#Path to the Suggestions form page
@app.route('/suggestions', methods=['GET', 'POST'])
@login_required
def suggestion():
        form = newSuggestionForm()
        suggestions = models.Suggestion.query.all()
        app.logger.debug("Entered Suggestions page")
        if form.validate_on_submit():
                app.logger.info("New suggestion %s for %s", form.title.data, form.sType.data)
                sug = models.Suggestion(sType=form.sType.data, title=form.title.data, desc=form.desc.data)
                db.session.add(sug)
                db.session.commit()
                return redirect(url_for('home'))
        return render_template('Suggestions.html', form=form, suggestions=suggestions)

from ressources import app
from flask import render_template, redirect, url_for, flash
from ressources.models import Item, User, Exercise
from ressources.forms import RegisterForm, LoginForm
from ressources import db
from flask_login import login_user

@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')

@app.route("/register", methods = ['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        
        return redirect(url_for('home_page')) # calls the function home_page
    
    if form.errors != {}: # If there's no errors in the validation phase
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
        return render_template('register.html', form=form)
    
    return render_template('register.html', form=form)

@app.route("/login", methods = ['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user) # This is very important!!! if you use this you can have the information about the user so you can show them in the html
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Username and password are not matching! Please try again', category='danger')
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@app.route("/exercises", methods = ['GET', 'POST'])
def exercise_page():
    exercises = Exercise.query.all()
    return render_template('exercises.html',exercises=exercises)

@app.route("/create_exercise", methods = ['GET', 'POST'])
def create_exercise_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        
        return redirect(url_for('exercise_page')) # calls the function exercise_page
    
    if form.errors != {}: # If there's no errors in the validation phase
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
        return render_template('create_exercise.html', form=form)
    return render_template('create_exercise.html', form=form)

@app.route('/delete/<int:id>')
def delete(id):
    exercise_to_delete = Exercise.query.get_or_404(id)
    try:
        db.session.delete(exercise_to_delete)
        db.session.commit()
        return redirect(url_for('exercise_page'))
    except:
        return  flash(f'Exercise failed to be deleted', category='danger')

@app.route('/code-server')
def code_server():
    # Replace with the IP address or domain where your Docker container is hosted
    code_server_url = 'http://localhost:8080'  
    return redirect(code_server_url)
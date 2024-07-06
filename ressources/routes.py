from ressources import app
from flask import render_template, redirect, url_for, flash, request
from ressources.models import User, Exercise
from ressources.forms import EditUserForm, LoginForm, ExerciseForm, CreateUserForm
from ressources import db
from flask_login import login_user, current_user, logout_user

from jinja2 import Environment, select_autoescape

env = Environment(autoescape=select_autoescape())


@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')

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

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home_page'))

# Exercises page

@app.route("/exercises", methods = ['GET', 'POST'])
def exercise_page():
    exercises = Exercise.query.all()
    authors = {}
    for exercise in exercises:
        author_id = exercise.author # Get the author id equivalent of username id
        author = User.query.get(author_id) # Get the information that the id has
        if author:
            authors[exercise.id] = author.username # Now that we got information we want to get the actual name of the author
        else:
            authors[exercise.id] = "Unknown"
    return render_template('exercises.html', exercises=exercises, authors=authors, author_id=author_id) # Now we assign author instead of the number in html

@app.route("/create_exercise", methods = ['GET', 'POST'])
def create_exercise_page():
    form = ExerciseForm()
    if current_user!=current_user:
        user = current_user.get_id() # return username in get_id()
    else:
        user = 0 # or 'some fake value', whatever
    print('You are ',user)
        
    if form.validate_on_submit():
        exercise_to_create = Exercise(name=form.exercise_name.data,
                                      subject=form.subject.data,
                                      description=form.description.data,
                                      content=form.content.data,
                                      author=user)
        db.session.add(exercise_to_create)
        db.session.commit()
        return redirect(url_for('exercise_page')) # calls the function exercise_page
    
    if form.errors != {}: # If there's no errors in the validation phase
        for err_msg in form.errors.values():
            flash(f'There was an error with creating an exercise: {err_msg}', category='danger')
        return render_template('create_exercise.html', form=form)
    
    return render_template('create_exercise.html', form=form)

@app.route('/edit_exercise/<int:id>', methods = ['GET', 'POST'])
def edit_exercise_page(id):
    exercise_to_update = Exercise.query.get_or_404(id)
    print(exercise_to_update.name)
    form = ExerciseForm()
    if current_user!=current_user:
        user = current_user.get_id() # return username in get_id()
    else:
        user = 0 # or 'some fake value', whatever
        
    if form.validate_on_submit():
        exercise_to_update.name = form.exercise_name.data
        exercise_to_update.subject = form.subject.data
        exercise_to_update.description = form.description.data
        exercise_to_update.content = form.content.data
        exercise_to_update.author = user
        db.session.add(exercise_to_update)
        db.session.commit()
        flash("Exercise updated")
        return redirect(url_for('exercise_page')) # calls the function exercise_page
    form.exercise_name.data = exercise_to_update.name
    form.subject.data = exercise_to_update.subject
    form.description.data = exercise_to_update.description
    form.content.data = exercise_to_update.content
    return render_template('edit_exercise.html', form=form) # calls the function exercise_page

@app.route('/delete_exercise/<int:id>')
def delete_exercise(id):
    exercise_to_delete = Exercise.query.get_or_404(id)
    try:
        db.session.delete(exercise_to_delete)
        db.session.commit()
        flash(f"{exercise_to_delete.name} deleted successfully", category='success')
        return redirect(url_for('exercise_page'))
    except:
        return  flash(f'Exercise failed to be deleted', category='danger')

# Users page

@app.route("/users", methods = ['GET', 'POST'])
def user_page():
    users = User.query.all()
    return render_template('users.html', users=users) # Now we assign author instead of the number in html

@app.route("/create_user", methods = ['GET', 'POST'])
def create_user_page():
    form = CreateUserForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              authority=form.authority.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('user_page')) # calls the function home_page
    
    if form.errors != {}: # If there's no errors in the validation phase
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
        return render_template('create_user.html', form=form)
    
    return render_template('create_user.html', form=form)

@app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
def edit_user_page(id):
    user_to_update = User.query.get_or_404(id)
    form = EditUserForm(current_user=user_to_update)
    
    if form.validate_on_submit():
        user_to_update.username = form.username.data
        user_to_update.email_address = form.email_address.data
        user_to_update.authority = form.authority.data

        # Check if new password is provided
        if form.password1.data and form.password2.data:
            user_to_update.password = form.password1.data

        db.session.commit()
        flash("User updated successfully", category='success')
        return redirect(url_for('user_page')) 

    if form.errors:
        for err_msg in form.errors.values():
            flash(f'There was an error with updating the user: {err_msg}', category='danger')

    form.username.data = user_to_update.username
    form.email_address.data = user_to_update.email_address
    form.authority.data = user_to_update.authority
    return render_template('edit_user.html', form=form)


@app.route('/delete_user/<int:id>')
def delete_user(id):
    user_to_delete = User.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirect(url_for('user_page'))
    except:
        return  flash(f'User failed to be deleted', category='danger')


@app.route('/code-server')
def code_server():
    # Replace with the IP address or domain where your Docker container is hosted
    code_server_url = 'http://localhost:8080'  
    return redirect(code_server_url)
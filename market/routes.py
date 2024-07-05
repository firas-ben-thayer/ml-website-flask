from market import app, mail 
from flask import render_template, redirect, url_for, flash, request, redirect
from market.models import Item,User, Contact
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, ContactUs
from market import db, app, mail
from flask_login import login_user, logout_user
from flask_mail import Message

@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')

@app.route("/market", methods = ['GET', 'POST'])
def market_page():
    purchase_form = PurchaseItemForm()
    if purchase_form.validate_on_submit():
        print(purchase_form['submit'])
    items = Item.query.all()
    return render_template('market.html', items=items, purchase_form=purchase_form)

@app.route("/register", methods = ['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        
        return redirect(url_for('market_page')) # calls the function market_page
    
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

@app.route('/code-server')
def code_server():
    # Replace with the IP address or domain where your Docker container is hosted
    code_server_url = 'http://localhost:8080'  
    return redirect(code_server_url)
# New feature route
@app.route('/about_page', methods = ['GET', 'POST'])
def about_page():
    form = ContactUs()
    if form.validate_on_submit():
        message_to_us = Contact(name=form.name.data,
                              email=form.email.data,
                              message=form.message.data)
        db.session.add(message_to_us)
        db.session.commit()
        
        return redirect(url_for('about_page')) # calls the function market_page
    
    if form.errors != {}: # If there's no errors in the validation phase
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a message: {err_msg}', category='danger')
        return render_template('about.html', form=form)
    return render_template('about.html',form=form)



@app.route('/about', methods=['GET', 'POST'])
def about():
    from market import mail
    form = ContactUs()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data

        # Compose the email message
        msg = Message('Contact Us',  # Subject
                      sender=email,  # Sender address from form
                      recipients=['nima.saghi1993@gmail.com'])  # Replace with your email

        msg.body = f'Name: {name}\nEmail: {email}\nMessage: {message}'

        try:
            mail.send(msg)
            flash('Your message has been sent successfully!', 'success')
            return redirect(url_for('about'))
        except Exception as e:
            flash(f'An error occurred while sending your message: {str(e)}', 'danger')

    return render_template('about.html', title='About Us', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home_page'))


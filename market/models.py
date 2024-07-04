from market import db, app, bcrypt, login_manager
from flask_login import UserMixin # this contains predetermined calls that we need in login_manager along with login_manager check https://flask-login.readthedocs.io/en/latest/#how-it-works fpr more info

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User (db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=20), unique=True, nullable=False)
    email_address = db.Column(db.String(length=80), unique=True, nullable=False)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer, nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)
    exercices = db.relationship('Exercise', backref='owned_user', lazy=True)
    
    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f"{str(self.budget)[:-3]},{str(self.budget)[-3:]}$"
        else:
            return f"{self.budget}$"
    
    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
        
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
class Item(db.Model):
    id = price = db.Column(db.Integer(), primary_key = True, nullable=False)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f'Item {self.name}'

class Exercise(db.Model):
    id = db.Column(db.Integer(), primary_key = True, nullable=False)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    subject = db.Column(db.String(length=50), nullable=False)
    description = db.Column(db.String(), nullable=False, unique=True)
    content = db.Column(db.String(), nullable=False)
    author = db.Column(db.Integer(), db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f'Item {self.name}'
app.app_context().push() # This is needed when we want to create a new database when we run the code db.create_all() we need to push context first
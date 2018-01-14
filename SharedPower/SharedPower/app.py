from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'GROUP' #All caps.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users\Jerrelle\Desktop\SharedPower\SharedPower\sharedpower.db' #Change if the .db filename name changes or if the backup is needed to be used.
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
app.debug = True #Switch to True if testing, otherwise leave it as False.

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Enter a valid email to register on SharedPower'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=5, max=10)])
    password = StringField('password', validators=[InputRequired(), Length(min=8, max=80)])

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/tools')
def tools():
    return render_template('tools.html')

@app.route('/aboutsp')
def aboutsp():
    return render_template('aboutsp.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first() #First() as the username will be unique therefore only one result shall be given.
        if user:
            if user.password == form.password.data: #Ensures the password the user has inputted is equal to the same password that was inputted during registration. (The form)
                return redirect(url_for('dashboard')) #Redirects legitimate users to the protected dashboard.
        return 'You have entered an incorrect password/username combo, please try again or sign up (/signup) if you have not done so already.' #Failsafe for an incorrect email/pass combo.

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user) # This adds the user to the final database connected to the SharedPower website.
        db.session.commit()
        return '<h1> Thank you for registering! Your account has been successfully created!</h1>'

        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' +form.password.data + '</h1>'

    return render_template('signup.html', form=form)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run()

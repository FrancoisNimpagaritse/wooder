
from flask import Flask, render_template, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

db = SQLAlchemy()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wooder.db'
app.config['SECRET_KEY'] = 'thisisascretkey'

db.init_app(app)
app.app_context().push()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)


class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False, unique=True)
    description = db.Column(db.String(500))
    date_start = db.Column(db.Date(), nullable=False)
    date_end = db.Column(db.Date(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Expense(db.Model):
    amount = db.Column(db.Integer, nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    date_transaction = db.Column(db.Date(), nullable=False)
    descritpion = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    date_transaction = db.Column(db.Date(), nullable=False)
    descritpion = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("email: " + request.form.get('email'))
        print("password: " + request.form.get('password'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(firstname) < 2:
            flash('Le prénom doit avoir aumoins 4 caractères !', category='error')
        elif len(lastname) < 4:
            flash('Le nom doit avoir aumoins 4 caractères !', category='error')
        elif len(email) < 3:
            flash('L"email saisi est invalide !', category='error')
        elif len(password1) < 8:
            flash('Le mot de passe doit avoir aumoins 8 caractères !', category='error')
        elif password1 != password2:
            flash('Les deux mots de passe ne sont pas identiques !', category='error')
        else:
            pwd_hash = generate_password_hash(password1, method='sha256')
            new_user = User(firstname=firstname, lastname=lastname, email=email, password=pwd_hash)
            db.session.add(new_user)
            db.session.commit()

            flash('Compte crée correctement.', category='success')
            return redirect(url_for('index'))

    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/project')
def project():
    return render_template('projects.html')


@app.route('/expense')
def expense():
    return render_template('expenses.html')


@app.route('/sale')
def sale():
    return render_template('sales.html')


if __name__ == '__main__':
    app.run(debug=True)

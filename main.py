
from flask import Flask, render_template, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

db = SQLAlchemy()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wooder.db'
app.config['SECRET_KEY'] = 'thisisascretkey'

db.init_app(app)
app.app_context().push()

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


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
    return render_template('index.html', user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Connexion réussie.', category='success')
                login_user(user, remember=True)
                return redirect(url_for('index'))
            else:
                flash('Identifiants incorrects!', category='error')
        else:
            flash('Cet email n\'existe pas!', category='error')

    return render_template('login.html', user=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email)
        if user:
            flash('Un autilisateur avec cet email existe déjà! Choisissez un autre.', category='error')
        elif len(firstname) < 2:
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

    return render_template('register.html', user=current_user)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)


@app.route('/project')
@login_required
def project():
    return render_template('projects.html', user=current_user)


@app.route('/expense')
@login_required
def expense():
    return render_template('expenses.html', user=current_user)


@app.route('/sale')
@login_required
def sale():
    return render_template('sales.html', user=current_user)


if __name__ == '__main__':
    app.run(debug=True)


from flask import Flask, render_template, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime

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
    estimated_cost = db.Column(db.Integer)
    estimated_revenue = db.Column(db.Integer)
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
        """
        user = User.query.filter_by(email=email)
        print(user)
        print(email)
        if user:
            flash('Un utilisateur avec cet email existe déjà! Choisissez un autre.', category='error')
        """
        if len(firstname) < 2:
            flash('Le prénom doit avoir aumoins 4 caractères !', category='error')
        elif len(lastname) < 4:
            flash('Le nom doit avoir aumoins 4 caractères !', category='error')
        elif len(email) < 3:
            flash('L"email saisi est invalide !', category='error')
        elif len(password1) < 6:
            flash('Le mot de passe doit avoir aumoins 6 caractères !', category='error')
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


@app.route('/project', methods=['GET', 'POST'])
@login_required
def project():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        estimated_cost = int(request.form.get('estimated_cost'))
        estimated_revenue = int(request.form.get('estimated_revenue'))

        y, m, d = request.form.get('date_start').split('-')
        date_start = datetime(int(y), int(m), int(d))

        y, m, d = request.form.get('date_end').split('-')
        date_end = datetime(int(y), int(m), int(d))

        # end date should be greater than start date
        if date_end <= date_start:
            flash('La date de fin doit être supérieure à la date de début', 'error')

        else:
            new_project = Business(title=title, description=description, date_start=date_start, date_end=date_end, estimated_cost=estimated_cost, estimated_revenue=estimated_revenue, user_id=current_user.id)
            db.session.add(new_project)
            db.session.commit()
            flash('Projet créé avec succès', category='success')

    return render_template('projects.html', user=current_user, projects=Business.query.all())


@app.route('/project_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def project_edit(id):
    project = Business.query.get_or_404(id)

    if request.method == 'POST':
        project.title = request.form.get('title')
        project.description = request.form.get('description')
        project.estimated_cost = int(request.form.get('estimated_cost'))
        project.estimated_revenue = int(request.form.get('estimated_revenue'))

        y, m, d = request.form.get('date_start').split('-')
        project.date_start = datetime(int(y), int(m), int(d))

        y, m, d = request.form.get('date_end').split('-')
        project.date_end = datetime(int(y), int(m), int(d))

        db.session.commit()
        flash('Projet mis à jour', category='success')
        return redirect(url_for('project'))
    else:
        return render_template('project_edit.html', project=project, user=current_user)


@app.route('/project_delete/<int:id>')
@login_required
def project_delete(id):
    project_to_delete = Business.query.get_or_404(id)

    if project_to_delete:
        db.session.delete(project_to_delete)
        db.session.commit()
        flash('Projet supprimé avec succès', 'success')
        return redirect(url_for('project'))


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

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db

auth = Blueprint("auth", __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Connexion réussie.', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.index'))
            else:
                flash('Identifiants incorrects!', category='error')
        else:
            flash('Cet email n\'existe pas!', category='error')

    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email)
        if user:
            flash('Un utilisateur avec cet email existe déjà! Choisissez un autre.', category='error')

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
            return redirect(url_for('views.index'))

    return render_template('register.html', user=current_user)

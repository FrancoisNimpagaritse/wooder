from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, current_user
from datetime import datetime
from .models import Business, Expense, Sale
from . import db

views = Blueprint("views", __name__)


@views.route("/")
def index():
    return render_template('index.html', user=current_user)


@views.route('/dashboard')
@login_required
def dashboard():
    list_total_expense_per_project()
    list_total_sales_per_project()

    return render_template('dashboard.html', user=current_user)


def list_total_expense_per_project(): # active project ==> add status(active/closed) field on project
    pass # project_id: total_exp as a list of tuples or as a dictionary


def list_total_sales_per_project():
    pass # project_id: total_sale


@views.route('/projects', methods=['GET', 'POST'])
@login_required
def project():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        op_checked = request.form.get("active")
        if op_checked:
            active = True
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
            new_project = Business(title=title, description=description, active=active, date_start=date_start, date_end=date_end, estimated_cost=estimated_cost, estimated_revenue=estimated_revenue, user_id=current_user.id)
            db.session.add(new_project)
            db.session.commit()
            flash('Projet créé avec succès', category='success')

    return render_template('projects.html', user=current_user, projects=Business.query.all())


@views.route('/project_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def project_edit(id):
    project = Business.query.get_or_404(id)

    if request.method == 'POST':
        project.title = request.form.get('title')
        project.description = request.form.get('description')
        op_checked = request.form.get("active")
        if op_checked:
            project.active = True
        project.estimated_cost = int(request.form.get('estimated_cost'))
        project.estimated_revenue = int(request.form.get('estimated_revenue'))

        y, m, d = request.form.get('date_start').split('-')
        project.date_start = datetime(int(y), int(m), int(d))

        y, m, d = request.form.get('date_end').split('-')
        project.date_end = datetime(int(y), int(m), int(d))

        db.session.commit()
        flash('Projet mis à jour', category='success')
        return redirect(url_for('views.project'))
    else:
        return render_template('project_edit.html', project=project, user=current_user)


@views.route('/project_delete/<int:id>')
@login_required
def project_delete(id):
    project_to_delete = Business.query.get_or_404(id)

    if project_to_delete:
        db.session.delete(project_to_delete)
        db.session.commit()
        flash('Projet supprimé avec succès.', 'success')
        return redirect(url_for('project'))


@views.route('/expenses', methods=['GET', 'POST'])
@login_required
def expense():
    if request.method == 'POST':
        amount = request.form.get("amount")
        category = request.form.get("category")

        y, m, d = request.form.get('date_transaction').split('-')
        date_transaction = datetime(int(y), int(m), int(d))

        financier = request.form.get('financier')
        description = request.form.get("description")
        business_id = request.form.get("project_id")

        new_expense = Expense(amount=amount, category=category, date_transaction=date_transaction, financier=financier, description=description, business_id=business_id, user_id=current_user.id)
        db.session.add(new_expense)
        db.session.commit()
        flash('Dépense créée avec succès', category='success')

    return render_template('expenses.html', user=current_user, expenses=Expense.query.all(), projects=Business.query.all())


@views.route('/expense_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def expense_edit(id):
    expense_to_edit = Expense.query.get_or_404(id)

    if request.method == 'POST':
        expense_to_edit.amount = request.form.get("amount")
        expense_to_edit.category = request.form.get("category")

        y, m, d = request.form.get('date_transaction').split('-')
        expense_to_edit.date_transaction = datetime(int(y), int(m), int(d))

        expense_to_edit.financier = request.form.get("financier")
        expense_to_edit.description = request.form.get("description")
        expense_to_edit.business_id = request.form.get("project_id")

        db.session.commit()
        flash("Transaction dépense modifiée avec succès.", category="success")
        return redirect(url_for('views.expense'))

    return render_template('expense_edit.html', expense=expense_to_edit, user=current_user, projects=Business.query.all())


@views.route('/expense_delete/<int:id>')
def expense_delete(id):
    expense_to_delete = Expense.query.get_or_404(id)

    if expense_to_delete:
        db.session.delete(expense_to_delete)
        db.session.commit()
        flash('Transaction dépense supprimé avec succès.', category='success')
        return redirect(url_for('views.expense'))


@views.route('/sales', methods=['GET', 'POST'])
@login_required
def sale():
    if request.method == 'POST':
        amount = request.form.get("amount")
        y, m, d = request.form.get('date_transaction').split('-')
        date_transaction = datetime(int(y), int(m), int(d))

        description = request.form.get("description")
        business_id = request.form.get("project_id")

        new_sale = Sale(amount=amount, date_transaction=date_transaction, description=description, business_id=business_id, user_id=current_user.id)
        db.session.add(new_sale)
        db.session.commit()
        flash('Transaction de vente créée avec succès', category='success')

    return render_template('sales.html', user=current_user, sales=Sale.query.all(), projects=Business.query.all())


@views.route('/sale_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def sale_edit(id):
    sale_to_edit = Sale.query.get_or_404(id)

    if request.method == 'POST':
        sale_to_edit.amount = request.form.get("amount")
        y, m, d = request.form.get('date_transaction').split('-')
        sale_to_edit.date_transaction = datetime(int(y), int(m), int(d))

        sale_to_edit.description = request.form.get("description")
        sale_to_edit.business_id = request.form.get("project_id")

        db.session.commit()
        flash("Transaction de vente modifiée avec succès.", category="success")
        return redirect(url_for('views.sale'))

    return render_template('sale_edit.html', sale=sale_to_edit, user=current_user, projects=Business.query.all())


@views.route('/sale_delete/<int:id>')
def sale_delete(id):
    sale_to_delete = Sale.query.get_or_404(id)

    if sale_to_delete:
        db.session.delete(sale_to_delete)
        db.session.commit()
        flash('Transaction de vente supprimée avec succès.', category='success')
        return redirect(url_for('sale'))

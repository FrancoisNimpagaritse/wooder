
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/logout')
def logout():
    return render_template('index.html')


@app.route('/register')
def register():
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


if __name__ == '__main__':
    app.run(debug=True)
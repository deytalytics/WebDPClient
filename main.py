from flask import Flask, request, render_template, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from cr_sqlite_db import save_user_to_db
app = Flask(__name__)
app.secret_key = 'secret_key'

# Database to store registered users
users = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        print(username, password, confirm_password)

        # Hash the password for security
        hashed_password = generate_password_hash(password)

        # Save the user in the database
        save_user_to_db(username, hashed_password)

        return redirect('/login')

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        print(username, password)

        # Check if the user exists in the database
        if username in users:
            # Check if the password is correct
            if check_password_hash(users[username], password):
                session['username'] = username
                return redirect('/dashboard')

        print(username)
        return 'Invalid username or password'

    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return f'Welcome, {session["username"]}'

    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='8000')

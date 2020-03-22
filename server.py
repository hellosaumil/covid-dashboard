import os, re, sys, json
from flask import Flask, request, render_template, send_file, make_response, jsonify, redirect, url_for
from user_management import load_users, add_user

import flask_login

app = Flask(__name__)
headers = {'Content-Type' : 'application/json'}
app.secret_key = 'super secret string'  # Change this!

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


@app.route('/', methods=["GET"])
def dashboardGET():
    return redirect(url_for('dashboard'))



class User(flask_login.UserMixin):
    pass

def get_users():
    return load_users()

@login_manager.user_loader
def user_loader(email):

    curr_users = get_users()

    if email not in curr_users.keys():
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):

    curr_users = get_users()

    email = request.form.get('email')
    if email not in curr_users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == curr_users[email]['password']

    return user

@app.route('/login', methods=['GET'])
def login():
    return '''
           <form action='login_post' method='POST'>
            <input type='text' name='username' id='username' placeholder='username'/>
            <input type='password' name='password' id='password' placeholder='password'/>
            <input type='submit' name='submit'/>
            </form>

            <br>

            <form action='signup_post' method='POST'>
             <input type='text' name='new_username' id='new_username' placeholder='new username'/>
             <input type='password' name='new_password' id='new_password' placeholder='******'/>
             <input type='submit' name='submit'/>
            </form>
           '''

@app.route('/login_post', methods=['POST'])
def login_post():

    curr_users = get_users()
    email = request.form['username']

    """ Check if user not in userbase """
    if email not in curr_users.keys():
        return 'User not found!'


    if request.form['password'] == curr_users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return redirect(url_for('dashboard'))

    return 'Incorrect user/password!'


@app.route('/dashboard')
@flask_login.login_required
def dashboard():
    return 'Logged in as: ' + flask_login.current_user.id

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@app.route('/signup', methods=["GET"])
def signup_get():
    return redirect(url_for('login'))


@app.route('/signup_post', methods=["POST"])
def signup_post():

    # TODO: Exception handling
    # try:
    new_uname, new_pwd = request.form['new_username'], request.form['new_password']

    # TODO: Add username validation here
    if not new_uname:
        return "New Username Empty"
        return redirect(url_for('dashboard'))

    print("new_uname: {}, new_pwd: {}".format(new_uname, new_pwd))

    add_user(uname=new_uname, pwd=new_pwd)
    print('Signed Up')

    return redirect(url_for('dashboard'))


@login_manager.unauthorized_handler
def unauthorized_handler():
    # return 'Unauthorized'
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0',port=port,threaded=True,debug=True)

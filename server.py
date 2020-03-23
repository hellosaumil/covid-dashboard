import os, re, sys, json
import logging
from flask import Flask, request, render_template, send_file, make_response, jsonify, redirect, url_for
from flask_cors import CORS, cross_origin

from covid_stats import CovidStats

from apscheduler.schedulers.background import BackgroundScheduler

session_dict = dict()
from user_management import load_users, add_user

import flask_login

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

headers = {'Content-Type' : 'application/json'}
app.secret_key = 'super secret string'  # Change this!

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


@app.route('/', methods=["GET"])
@cross_origin()
def dashboardGET():
    return redirect(url_for('dashboard'))

class User(flask_login.UserMixin):
    pass

def get_users():
    return load_users()

def validate_user(uname=None, pwd=None):

    curr_users = get_users()

    """ Check if user not in userbase """
    if uname not in curr_users.keys():
        return False

    if pwd == curr_users[uname]['password']:
        user = User()
        user.id = uname
        flask_login.login_user(user)
        return True

    return False

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
@cross_origin()
def login():

    alert=session_dict.get('alert', None)
    if alert: del session_dict['alert']

    basic_login_form = '''
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

    if not alert or alert == "": return basic_login_form
    else: return '''<script type="text/javascript">alert("{}");</script>'''.format(alert) + basic_login_form

@app.route('/login_post', methods=['POST'])
@cross_origin()
def login_post():

    if validate_user(uname=request.form['username'], pwd=request.form['password']):
        return redirect(url_for('dashboard'))
    else:
        return 'Incorrect user/password!'

@app.route('/logout')
@cross_origin()
def logout():
    flask_login.logout_user()
    # return 'Logged out'
    session_dict["alert"] = "Logged out"
    return redirect(url_for('login'))

@app.route('/signup', methods=["GET"])
@cross_origin()
def signup_get():
    return redirect(url_for('login'))

@app.route('/signup_post', methods=["POST"])
@cross_origin()
def signup_post():

    # TODO: Exception handling
    # try:
    new_uname, new_pwd = request.form['new_username'], request.form['new_password']

    # TODO: Add username validation here
    if not new_uname:
        session_dict["alert"] = "New Username Empty"
        return redirect(url_for('dashboard'))

    curr_users = load_users()
    if new_uname in curr_users.keys():
        print("Username already taken!")
        session_dict["alert"] = "Username already taken!"
        return redirect(url_for('login'))

    print("new_uname: {}, new_pwd: {}".format(new_uname, new_pwd))
    add_callback_result = add_user(uname=new_uname, pwd=new_pwd)

    if validate_user(uname=new_uname, pwd=new_pwd):
        print('Signed Up')
        session_dict["alert"] = add_callback_result
    else:
        print("Signup Failed")
        session_dict["alert"] = "Signup Failed"

    return redirect(url_for('dashboard'))

@login_manager.unauthorized_handler
def unauthorized_handler():
    # return 'Unauthorized'
    return redirect(url_for('login'))


@app.route('/dashboard')
@cross_origin()
@flask_login.login_required
def dashboard():

    alert=session_dict.get('alert', None)
    if alert: del session_dict['alert']

    dashboard_basic_html = "<h2> {} </h2>".format("Logged in as: " + flask_login.current_user.id)

    if not alert or alert == "": return dashboard_basic_html
    else: return '''<script type="text/javascript">alert("{}");</script>'''.format(alert) + dashboard_basic_html

@app.route('/countries', methods=["GET"])
@cross_origin()
def get_countires():
    # return json.dumps({"countries": sorted(list(map(lambda x: x['name'], global_covid.list_countries())))})

    return json.dumps({"countries": global_covid.list_countries()})

@app.route('/country_id/<c_id>', methods=["GET"])
@cross_origin()
def get_county_by_id(c_id):
    return json.dumps( global_covid.country_stat(country_id=int(c_id), refresh=True) )

@app.route('/country/<c_name>', methods=["GET"])
@cross_origin()
def get_county_by_name(c_name):
    return json.dumps( global_covid.country_stat(country_name=c_name, refresh=True) )

def scheduled_job():
    print("\nTimed Execution...")

if __name__ == '__main__':

    global_covid = CovidStats()

    # TODO: Scheduler
    # scheduler = BackgroundScheduler()
    # job = scheduler.add_job(scheduled_job, 'interval', minutes=1//60)
    # scheduler.start()

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0',port=port,threaded=True,debug=True)

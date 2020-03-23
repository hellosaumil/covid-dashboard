import os, re, sys, json
import logging
from flask import Flask, request, render_template, redirect, url_for
from flask_cors import CORS, cross_origin
from apscheduler.schedulers.background import BackgroundScheduler
import flask_login

from covid_stats import CovidStats
import user_management as UAM


session_dict = dict()

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

app = Flask(__name__,
            static_folder="../covid-dashboard-ui/build/static",
            template_folder="../covid-dashboard-ui/build")

cors = CORS(app, support_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'

headers = {'Content-Type' : 'application/json'}
app.secret_key = 'super secret string'  # Change this!

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


get_global = lambda : { **{"id": "0", "country": "Global"}, **global_covid.get_stats(refresh=True)}


@app.route('/covid')
@cross_origin()
@flask_login.login_required
def covid_dashboard():
    return render_template('index.html')

@app.route('/', methods=["GET"])
@cross_origin()
def dashboardGET():
    # return redirect(url_for('dashboard'))
    return redirect(url_for('covid_dashboard'))

class User(flask_login.UserMixin):
    pass

def validate_user(uname=None, pwd=None):

    curr_users = UAM.load_users()

    """ Check if user not in userbase """
    if uname not in curr_users.keys():
        return False

    print(curr_users[uname])

    if pwd == curr_users[uname]['password']:
        user = User()
        user.id = uname
        flask_login.login_user(user)
        return True

    return False

@login_manager.user_loader
def user_loader(email):

    curr_users = UAM.load_users()

    if email not in curr_users.keys():
        return

    user = User()
    user.id = email
    return user

@login_manager.request_loader
def request_loader(request):

    curr_users = UAM.load_users()

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
        # return redirect(url_for('dashboard'))
        return redirect(url_for('covid_dashboard'))
    else:
        session_dict["alert"] = "Incorrect user/password!"
        return redirect(url_for('login'))

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

    curr_users = UAM.load_users()
    if new_uname in curr_users.keys():
        print("Username already taken!")
        session_dict["alert"] = "Username already taken!"
        return redirect(url_for('login'))

    print("new_uname: {}, new_pwd: {}".format(new_uname, new_pwd))
    add_callback_result = UAM.add_user(uname=new_uname, pwd=new_pwd)

    if validate_user(uname=new_uname, pwd=new_pwd):
        print('Signed Up')
        session_dict["alert"] = add_callback_result
    else:
        print("Signup Failed")
        session_dict["alert"] = "Signup Failed"

    # return redirect(url_for('dashboard'))
    return redirect(url_for('covid_dashboard'))

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
    return json.dumps({"countries": global_covid.list_countries()})

@app.route('/country_id/<c_id>', methods=["GET"])
@cross_origin()
def get_county_by_id(c_id):
    return json.dumps( global_covid.country_stat(country_id=int(c_id), refresh=True) )

@app.route('/country/<c_name>', methods=["GET"])
@cross_origin()
def get_county_by_name(c_name):
    return json.dumps( global_covid.country_stat(country_name=c_name, refresh=True) )


@app.route('/user-records', methods=["GET"])
@cross_origin()
# @flask_login.login_required
def get_user_interested_countries():

    # interested_countries = UAM.get_interest_countries(target_uname="saumil")
    interested_countries = UAM.get_interest_countries(target_uname=flask_login.current_user.id)
    return json.dumps({"user_records": [global_covid.country_stat(country) for country in interested_countries] +  [get_global()] })


@app.route('/record', methods=["POST"])
@cross_origin()
# @flask_login.login_required
def set_new_user_country():

    c_name = request.json.get("name", None)

    if not c_name:
        return {"id": -1, "msg": "Invalid Country Name"}

    # UAM.add_user_record(uname="saumil", new_countries=[c_name])
    UAM.add_user_record(uname=flask_login.current_user.id, new_countries=[c_name])

    # interested_countries = UAM.get_interest_countries(target_uname="saumil")
    interested_countries = UAM.get_interest_countries(target_uname=flask_login.current_user.id)
    return json.dumps({"user_records": [global_covid.country_stat(country) for country in interested_countries] +  [get_global()]})


@app.route('/remove-record', methods=["POST"])
@cross_origin()
# @flask_login.login_required
def delete_new_user_country():

    c_name = request.json.get("name", None)

    if not c_name:
        return {"id": -1, "msg": "Invalid Country Name"}

    # UAM.remove_user_record(uname="saumil", remove_countries=[c_name])
    UAM.add_user_record(uname=flask_login.current_user.id, new_countries=[c_name])

    # interested_countries = UAM.get_interest_countries(target_uname="saumil")
    interested_countries = UAM.get_interest_countries(target_uname=flask_login.current_user.id)
    return json.dumps({"user_records": [global_covid.country_stat(country) for country in interested_countries] +  [get_global()]})




def scheduled_job():
    print("\nTimed Execution...")

if __name__ == '__main__':

    global_covid = CovidStats()

    UAM.init_users()
    UAM.init_user_records()

    # TODO: Scheduler
    # scheduler = BackgroundScheduler()
    # job = scheduler.add_job(scheduled_job, 'interval', minutes=1//60)
    # scheduler.start()

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0',port=port,threaded=True,debug=True)

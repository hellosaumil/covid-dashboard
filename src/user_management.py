import os, re, sys, json

USER_DATABASE_PATH = "./data/users_credentials.json"
USER_INTEREST_DATA_PATH = "./data/users_covid_interests.json"

def init_json_file(json_path):
    if not os.path.exists(json_path):
        with open(json_path, "w") as write_file:
            json.dump({}, write_file, indent=4)

def load_json_file(json_path):

    init_json_file(json_path)
    with open(json_path, "r") as read_file:
        return json.load(read_file)

def save_json_file(json_path, data):

    with open(json_path, "w") as write_file:
        return json.dump(data, write_file, indent=4)



def init_users():
    init_json_file(USER_DATABASE_PATH)

def load_users():
    return load_json_file(USER_DATABASE_PATH)

def save_users(users_dict):
    save_json_file(USER_DATABASE_PATH, users_dict)

def add_user(uname=None, pwd=None):

    if not uname or not pwd:
        return "Incorrect uname/password..."

    existing_users = load_users()
    existing_users[uname] = {"password": pwd}

    save_users(existing_users)
    create_new_user_record(uname)

    return "User {} Registered!".format(uname)


def init_user_records():
    init_json_file(USER_INTEREST_DATA_PATH)

def load_user_records():
    return load_json_file(USER_INTEREST_DATA_PATH)

def save_user_records(users_records_dict):
    save_json_file(USER_INTEREST_DATA_PATH, users_records_dict)

def create_new_user_record(uname=None):

    if not uname:
        return "Incorrect uname..."

    existing_records = load_user_records()
    existing_records[uname] = {"countries": []}

    save_user_records(existing_records)
    return "User Record {} Created!".format(uname)

def add_user_record(uname=None, new_countries=[]):

    existing_records = load_user_records()

    ex_user_record = existing_records[uname]
    ex_user_record["countries"] = list(set(ex_user_record.get("countries", []) + new_countries))

    save_user_records(existing_records)
    return "User Record {} Added/Updated!".format(uname)

def remove_user_record(uname=None, remove_countries=[]):

    existing_records = load_user_records()

    ex_user_record = existing_records[uname]
    ex_user_record["countries"] = list(set(ex_user_record.get("countries", [])).difference(remove_countries))

    save_user_records(existing_records)
    return "User Record {} Added/Updated after Removed!".format(uname)

def get_user_records(target_uname):

    existing_records = load_user_records()
    return existing_records[target_uname]

def get_interest_countries(target_uname, user_records=None):
    return get_user_records(target_uname).get("countries", [])

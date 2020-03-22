import os, re, sys, json

USER_DATABASE_PATH = "./data/users_credentials.json"

def load_users():

    with open(USER_DATABASE_PATH, "r") as read_file:
        return json.load(read_file)

def add_user(uname=None, pwd=None):

    if not uname or not pwd:
        return "Incorrect uname/password..."

    existing_users = load_users()
    existing_users[uname] = {"password": pwd}

    save_users(existing_users)
    return "User {} Registered!".format(uname)

def save_users(users_dict):
    with open(USER_DATABASE_PATH, "w") as write_file:
        json.dump(users_dict, write_file, indent=4)

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


from html.parser import HTMLParser
from html.entities import name2codepoint

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Start tag:", tag)
        for attr in attrs:
            print("     attr:", attr)
    def handle_endtag(self, tag):
        print("End tag  :", tag)
    def handle_data(self, data):
        print("Data     :", data)
    def handle_comment(self, data):
        print("Comment  :", data)
    def handle_entityref(self, name):
        c = chr(name2codepoint[name])
        print("Named ent:", c)
    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))
        print("Num ent  :", c)
    def handle_decl(self, data):
        print("Decl     :", data)

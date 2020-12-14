import os
import hashlib
import time
from bottle import route, redirect, request, static_file, run, abort , auth_basic, template, TEMPLATE_PATH
from tinydb import TinyDB, Query

#GLOBAL
DB = TinyDB('image_db.json')
IMG_PATH = '../images/'
SALT = "*34567"
SERVER = "http://localhost:8080"

@route('/')
def home():
    return template('upload.tpl')

@route('/img/<filename>')
def server_static(filename):
    return static_file(filename, root=IMG_PATH)

@route('/show/<filename>')
def server_static(filename):
    url = f"{SERVER}/img/{filename}"
    return f' <a href="{url}">link text</a> <br> <img src="{SERVER}/img/{filename}"> ' 

@route('/db')
def print_db():
    return f"{DB.all()}"
    
@route('/upload/', method='POST') 
def do_upload():
    upload = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    if ext.upper() not in ( '.JPG', '.PNG', '.JPEG',".GIF"):
        return "<h3> File extension not allowed.</h3>"

    #hashlib action:
    m = hashlib.sha256( upload.filename.encode() +SALT.encode() )
    m.digest()
    hash_name = m.hexdigest()

    if not os.path.exists(IMG_PATH):
        os.makedirs(IMG_PATH)
    
    filename = f"{hash_name}{ext}"
    file_path = f"{IMG_PATH}/{filename}"

    #db.insert({'owner': 'public', 'time':"tmp", 'short_url':"show/82e0ea4f",'static_url': "/img/0fa5a0b7de11a5e45d58e61b69010b2677b4dbcb9f30f938e238561982e0ea4f.png"})
    DB.insert({'owner':'public', 'time':"tmp", 'short_url':hash_name[0:5],'static_url':file_path})

    try:
        upload.save(file_path)
    except IOError as e:
        print("file cannot be overwritten, rename and try again",e) #to do handel this better
    #redirect(f'/img/{hash_name}{ext}')
    redirect(f'/show/{filename}')

if __name__ == '__main__':
    run(debug=True, host='localhost', port=8080, reloader=True)




















#https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication # yes, use TSL 2.0
#https://www.nginx.com/blog/securing-urls-secure-link-module-nginx-plus/ #what is the difference between this and hashing the filename?
#https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-subrequest-authentication/ #very cool but complex.. 
#make multiple servers with each there own .htpass file
#hash the file names
#very-optional, add a username/pw system in bottle. try to make this separate from the main code, try adding a request cookie and a db with usernames


#security#
# def signed_in(username,token):
#     if username and token:
#         if username in ACTIVE_USERS: 
#             ACTIVE_USERS[username] = token
#             return True
#     redirect('/login')

# #return true if success, false if fail
# def sign_in(username,password):
#     if username and password: 
#         if username in USERS: 
#             if password == USERS[username]: 
#                 _token = username + password
#                 _token =  hashlib.sha256(_token.encode()).hexdigest()
#                 ACTIVE_USERS[username] = _token
#                 return True
#     return False

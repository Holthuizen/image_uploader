import os
import hashlib
import time
from bottle import route, redirect, request, static_file, run, abort , auth_basic, template

#global
img_path = '../images/'
USERS = {'user':"pw", "aine":'1234'}
ACTIVE_USERS= {}



@route('/')
def home():
    if logged_in(request.query.username):
        return template('upload.tpl',username=request.query.username)
    else: 
        redirect('/login')

@route('/show/<filename>') #http://localhost:8080/show/bff8ec4eda409ee7ffb1d025613e0e1a869d18566eff138240830ede3f2883c1.PNG?username=user
def server_static(filename):
    if not request.query.username or not logged_in(request.query.username):
        redirect('/login?msg= You need to be logged in view images, enter username and pw below')
    return static_file(filename, root=img_path)



@route('/upload/', method="GET")
def get_upload():
    #not a endpoint
    redirect('/')

@route('/upload/', method='POST') 
def do_upload():
    if not request.query.username or not logged_in(request.query.username):
        redirect('/login?msg= You need to be logged in to upload, enter username and pw below')
        
    upload = request.files.get('upload')
    username = request.query.username
    
    name, ext = os.path.splitext(upload.filename)
    if ext.upper() not in ( '.WEBP','.JPG', '.PNG', '.JPEG',".GIF"):
        return "<h3> File extension not allowed.</h3>"

    #hashlib action:
    _name = upload.filename + username
    m = hashlib.sha256()
    m.update(_name.encode())
    m.digest()
    hash_name = m.hexdigest()
    print("hash: ", hash_name)

    if not os.path.exists(img_path):
        os.makedirs(img_path)
    
    file_path = f"{img_path}/{hash_name}{ext}"
    try:
        upload.save(file_path)
    except IOError as e:
        print("file cannot be overwritten, rename and try again",e) #to do handel this better
    redirect(f'/show/{hash_name}{ext}?username={username}')


#security#
def login_required(username):
    if username in ACTIVE_USERS:
        return True
    else:
        redirect('/login?msg=Login required:')

def authenticate_user(username, pw):
    if username not in USERS:
        return False
    correct_pw = USERS[username]
    if pw == correct_pw:
        ACTIVE_USERS[username]= pw 
        return True

def logged_in(username): 
    if username in ACTIVE_USERS:
        return True

def log_out(username):
    if logged_in(username):
        try:
            print(ACTIVE_USERS.pop(username,False))
        except:
            print("sing_out of user {username}, failt}")
            return False
    return True

@route('/login')
def login():
    if request.query.msg:
        return template('login',message=request.query.msg)
    return template('login',message='Login with your Username and Password: ')


@route('/login', method='POST') 
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    authed =  authenticate_user(username,password)
    if authed: 
        redirect(f'/?username={username}')
    else:
        redirect("/login?msg=Incorrect username/password combination, you can try again") #get form

@route('/logout/<username>')
def logout(username):
    log_out(username)
    redirect('/')


if __name__ == '__main__':
    run(debug=True, host='localhost', port=8080, reloader=True)





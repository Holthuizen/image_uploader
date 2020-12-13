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
    if signed_in(request.query.username,request.query.token):
        return template('upload.tpl',username=request.query.username, token=request.query.token)
    else: 
        redirect('/login')

@route('/show/<filename>')
def server_static(filename):
    return static_file(filename, root=img_path)

@route('/upload/', method="GET")
def get_upload():
    #not an endpoint
    redirect('/')

@route('/upload/', method='POST') 
def do_upload():
    if not request.query.username or not signed_in(request.query.username,request.query.token):
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
    redirect(f'/show/{hash_name}{ext}?username={username}&token={request.query.token}')


#security#
def signed_in(username,token):
    if username and token:
        if username in ACTIVE_USERS: 
            ACTIVE_USERS[username] = token
            return True
    redirect('/login')

#return true if success, false if fail
def sign_in(username,password):
    if username and password: 
        if username in USERS: 
            if password == USERS[username]: 
                _token = username + password
                _token =  hashlib.sha256(_token.encode()).hexdigest()
                ACTIVE_USERS[username] = _token
                return True
    return False
        


@route('/login')
def login():
    if request.query.msg:
        return template('login',message=request.query.msg)
    return template('login',message='Login with your Username and Password: ')
    

@route('/login', method='POST') 
def do_login():
    if sign_in(request.forms.get('username'),request.forms.get('password')):
        redirect(f"/?username={request.forms.get('username')}&token={ACTIVE_USERS[request.forms.get('username')]}")
    else:
        redirect("/login?msg=Incorrect username/password combination, you can try again") #get form

    

if __name__ == '__main__':
    run(debug=True, host='localhost', port=8080, reloader=True)

#https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication # yes, use TSL 2.0
#https://www.nginx.com/blog/securing-urls-secure-link-module-nginx-plus/ #what is the difference between this and hashing the filename?
#https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-subrequest-authentication/ #very cool but complex.. 

#make multiple servers with each there own .htpass file
#hash the file names
#very-optional, add a username/pw system in bottle. try to make this separate from the main code, try adding a request cookie and a db with usernames






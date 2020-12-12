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

@route('/show/<filename>') #http://localhost:8080/show/bff8ec4eda409ee7ffb1d025613e0e1a869d18566eff138240830ede3f2883c1.PNG?username=user
def server_static(filename):
    if not signed_in(request.query.username,request.query.token):
        redirect('/login?msg= You need to be logged in view images, enter username and pw below')
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

#return token if succes, false if fail
def sign_in(username,password):
    if username and password: 
        if username in USERS: 
            if password == USERS[username]: 
                _token = username + password
                _token =  hashlib.sha256(_token.encode()).hexdigest()
                ACTIVE_USERS[username] = _token
                return username, _token
    return False
        


@route('/login')
def login():
    if request.query.msg:
        return template('login',message=request.query.msg)
    return template('login',message='Login with your Username and Password: ')
    

@route('/login', method='POST') 
def do_login():
    
    username, token = sign_in(request.forms.get('username'),request.forms.get('password'))
    if token : 
        print(username,token )
        redirect(f'/?username={username}&token={token}')
    else:
        redirect("/login?msg=Incorrect username/password combination, you can try again") #get form



@route('/logout/<username>')
def logout(username):
    log_out(username)
    redirect('/')


    

if __name__ == '__main__':
    run(debug=True, host='localhost', port=8080, reloader=True)





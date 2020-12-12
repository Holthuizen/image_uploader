import os
from bottle import route, redirect, request, static_file, run, abort , auth_basic, template

#global
img_path = '../images/'
USERS = {'user':"pw", "aine":'1234'}
ACTIVE_USERS= {}



@route('/')
def home():
    if loged_in(request.query.username):
        return template('upload.tpl',username=request.query.username)
    else: 
        redirect('/login')

@route('/show/<category>/<filename>')
def server_static(filename, category):
    save_path = img_path+category
    return static_file(filename, root=save_path)


@route('/upload/', method="GET")
def get_upload():
    redirect('/')

@route('/upload/', method='POST')
def do_upload():
    if not request.query.username:
        redirect("/login")
    if not loged_in(request.query.username):
        redirect('/login?msg= You need to be loged in to upload, enter username and pw below')
        
    category = request.forms.get('category')
    upload = request.files.get('upload')
    
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.png', '.jpg', '.jpeg', '.JPG', '.PNG', '.JPEG', ".gif",".GIF"):
        return "<h3>File extension not allowed.</h3>"


    #make dir
    save_path = f"{img_path}{category}"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    file_path = f"{save_path}/{upload.filename}"
    try:
        upload.save(file_path)
    except IOError as e:
        print("file cannot be overwritten, rename and try again",e) #to do handel this better
    redirect(f'/show/{category}/{name}{ext}')

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

def loged_in(username): 
    if username in ACTIVE_USERS:
        return True

def log_out(username):
    if loged_in(username):
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
    run(debug=True, host='0.0.0.0', port=8080, reloader=True)





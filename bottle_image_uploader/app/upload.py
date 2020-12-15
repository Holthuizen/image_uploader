import os
import hashlib
import json
from bottle import route, redirect, request, static_file, run, abort , auth_basic, template, TEMPLATE_PATH
from tinydb import TinyDB, Query, where

#GLOBAL
DB = TinyDB('image_db.json')
IMG_PATH = '../images/'
SALT = "*34567"
SERVER = "http://localhost:8080"

@route('/')
def home():
    return template('upload.tpl')

#http://localhost:8080/show/729227-8.png

@route('/download/<filename>')
def download(filename):
    return static_file(filename, root=IMG_PATH, download=filename[-10:])

@route('/img/<filename>')
def server_static(filename):
    return static_file(filename, root=IMG_PATH)

@route('/show/<short_url>')
def server_static(short_url):
    
    data = DB.search(where('short_url') == short_url)
    if data: 
        data = data[0]
        filename = data['filename']
        category = data['category']
        #print("debug: ", data['filename'] )
        full_url = f"{SERVER}/img/{filename}"
        copy_url = f"{SERVER}/show/{short_url}"
        download_url = f"{SERVER}/download/{filename}"
        delete_url = f"{SERVER}/delete/{short_url}"
        
        return template('show.tpl',category=category, url=full_url, short_url=copy_url, download_url = download_url, delete_url = delete_url )
    return f'<h2>img url not found</h2>' 

@route('/delete/<short_url>')
def delete(short_url): 
    if DB.contains(where('short_url') == short_url):   
        data =  DB.search(where('short_url') == short_url)
        data = data[0]
        filename = data['filename']
        file_path = f"{IMG_PATH}/{filename}"
        os.remove(file_path) 
        DB.remove(where('short_url') == short_url)
        redirect('/')
    else: 
        return '<h2>URL/File not found </h2>'





@route('/category/<category>')
def category(category):
    collection = DB.search(where('category')==category)
    for item in collection: 
        print(item)



@route('/db')
def print_db():
    return f"{DB.all()}"
    
@route('/upload/', method='POST') 
def do_upload():
    category = request.forms.get('category')
    upload = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    ext = ext.lower()
    if ext.upper() not in ( '.JPG', '.PNG', '.JPEG',".GIF"):
        return "<h3> File extension not allowed.</h3>"

    #hashlib action:
    m = hashlib.sha256( upload.filename.encode() +SALT.encode() )
    m.digest()
    hash_name = m.hexdigest()


    
    #create unique filename
    index = str( len(DB) ) #auto incremeting
    filename = f"{hash_name}{ext}"
    short_url = f"{hash_name[0:6]}-{index}{ext}"
    file_path = f"{IMG_PATH}/{filename}"
    
    #db entry
    find = Query()
    if not DB.contains(find.filename == filename): #this is almost always True, just to be sure
        DB.insert({'owner':'public','category':category,'short_url':short_url,'filename':filename})
    else: 
        print("file allready in db")
    
    #save file
    if not os.path.exists(IMG_PATH):
        os.makedirs(IMG_PATH)
    try:
        upload.save(file_path)
    except IOError as e:
        print("file cannot be overwritten, rename and try again",e) #to do handel this better
    #redirect(f'/show/{filename}')
    redirect(f'/show/{short_url}')


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

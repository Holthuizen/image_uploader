import os
import hashlib
import json
from bottle import route, redirect, request, static_file, run, abort , auth_basic, template, TEMPLATE_PATH
from tinydb import TinyDB, where

#GLOBAL
DB = TinyDB('image_db.json')
IMG_PATH = '../images/'
SALT = b"*34567"
SERVER = "http://localhost:8080"
#SERVER = "http://imgupl.ddns.net"

@route('/')
def home():
    if request.query.msg:
        return template('upload.tpl', list_url = f"{SERVER}/list", msg = request.query.msg )
    return template('upload.tpl', list_url = f"{SERVER}/list", msg="")

@route('/download/<filename>')
def download(filename):
    return static_file(filename, root=IMG_PATH, download=filename[-10:])

@route('/img/<filename>')
def server_static(filename):
    return static_file(filename, root=IMG_PATH)

@route('/show/<short_url>')
def server_static(short_url):
    data = DB.search(where('short_url') == short_url)
    ''' if short url point to data in db '''
    if data[0]: 
        data = data[0]
        filename = data['filename']
        category = data['category']

        return template(
            'show.tpl', server = SERVER,
            category=category,
            category_url=f"{SERVER}/category/{category}",
            url=f"{SERVER}/img/{filename}",
            short_url=f"{SERVER}/show/{short_url}",
            download_url = f"{SERVER}/download/{filename}", 
            delete_url = f"{SERVER}/delete/{short_url}" 
        )
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
    return '<h2>URL/File not found </h2>'


@route('/list')
def list_categories(): 
    categories = [r['category'] for r in DB]
    return template('category_list', server=SERVER, collection = set(categories))


@route('/category/<category>')
def category(category):
    collection = DB.search(where('category')==category)
    list1 = []
    for data in collection: 
        filename = data['filename']
        short_url = data['short_url']
        category = data['category']
        full_url = f"{SERVER}/img/{filename}"
        copy_url = f"{SERVER}/show/{short_url}"
        download_url = f"{SERVER}/download/{filename}"
        delete_url = f"{SERVER}/delete/{short_url}"
        list1.append({'filename':filename, 'category':category, 'full_url':full_url, 'copy_url':copy_url, 'download_url':download_url, 'delete_url': delete_url})
    return template('category', server=SERVER,collection = list1)


''' get data from form
    required: 
    category <string> 
    file <string> supported types : webp, jpeg, png, bmp
    file get stored on server with a hashed name sha256 + a constant salt.

'''
@route('/upload/', method='POST') 
def do_upload():
    category = request.forms.get('category')
    upload = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    
    if not category: 
        redirect('/?msg=Category cannot be empty')
    
    ext = ext.lower()
    if ext.upper() not in ( '.WEBP', '.JPG', '.PNG', '.JPEG','.GIF', '.BMP'):
        return "<h3> File extension not allowed.</h3>"

    #hashlib action:
    m = hashlib.sha256( upload.filename.encode() + SALT)
    m.digest()
    hash_name = m.hexdigest()

    #create unique filename
    filename = f"{hash_name}{ext}"
    ''' if not already in db, add entry ''' 
    if not DB.contains(where('filename') == filename):
        index = str( len(DB) ) #auto incremeting
        short_url = f"{hash_name[0:6]}-{index}{ext}"
        file_path = f"{IMG_PATH}/{filename}"

        DB.insert({'owner':'public','category':category,'short_url':short_url,'filename':filename})
        #save file
        if not os.path.exists(IMG_PATH):
            os.makedirs(IMG_PATH)
        try:
            upload.save(file_path)
        except IOError as e:
            redirect(f'/?msg=file allready exists got to: /show/{short_url}')
        redirect(f'/show/{short_url}')
    else: 
         data = DB.search(where('filename') == filename)
         data = data[0]
         short_url = data['short_url']
         redirect(f'/show/{short_url}')
    

#for debugging, dangerous route 
@route('/db')
def print_db():
    return f"{DB.all()}"


if __name__ == '__main__':
    run(debug=True, host='localhost', port=8080, reloader=True)





# added suport for bmp and webp 
# max file size now 24MB
# 














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

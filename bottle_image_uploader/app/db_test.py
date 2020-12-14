from tinydb import TinyDB, Query

db = TinyDB('public.json')
# db.insert({'type': 'apple', 'count': 7})
# db.insert({'type': 'peach', 'count': 3})
db.insert({'owner': 'public', 'time':"tmp", 'short_url':"show/82e0ea4f",'static_url': "/img/0fa5a0b7de11a5e45d58e61b69010b2677b4dbcb9f30f938e238561982e0ea4f.png"})
for item in db: 
    print(item)


import json
import numpy as np
import mysql.connector
import sqlite3

class Geek:
    def __init__(self, id = 0, name=''):
         self._id = id
         self._name = name
      
    # getter method
    def get_id(self):
        return self._id
      
    # setter method
    def set_id(self, x):
        self._id = x

    def get_name(self):
        return self._name
      
    # setter method
    def set_name(self, x):
        self._name = x

raj = Geek()
raj.set_id(21)
raj.set_name("bac")
people = raj.__dict__
people
print(raj.__dict__)
with open("people.json", "a") as fout:
    o = json.dumps(raj.__dict__)
    json.dump(raj.__dict__, fout, indent=4, separators=(",",":"))
people.setdefault(18, 'nam')
print(people)

mydb = mysql.connector.connect(
  host="localhost",
  port= '3306',
  user="root",
  password= '11041975Bac',
  database='demo_database'
)

print(mydb)

conn=sqlite3.connect("FaceBaseNew.db")
cursor=conn.execute("SELECT * FROM People WHERE ID="+str(1))
profile=None
for row in cursor:
    profile=row
conn.close()
print(profile)
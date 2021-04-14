import json
import unittest
import sqlite3
import os
import requests

def read_cache(CACHE_FNAME):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    CACHE_FNAME = dir_path + '/' + "cache_dogs.json"
    try:
        cache_file = open(CACHE_FNAME, 'r', encoding="utf-8") # Try to read the data from the file
        cache_contents = cache_file.read()  # If it's there, get it into a string
        CACHE_DICTION = json.loads(cache_contents) # And then load it into a dictionary
        cache_file.close() # Close the file, we're good, we got the data in a dictionary.
        return CACHE_DICTION
    except:
        CACHE_DICTION = {}
        return CACHE_DICTION

def write_cache(CACHE_FNAME, CACHE_DICT):
    CACHE_FNAME="cache_dogs.json"
    cache_file = open(CACHE_FNAME, 'w', encoding="utf-8")
    name=json.dumps(CACHE_DICT)
    cache_file.write(name)
    cache_file.close()

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

#1.Dog API

def create_request_url(breed, page):
    base_url="https://api.thedogapi.com/v1/breeds?attach_breed={}&limit=25&page={}"
    request_url=base_url.format(breed, page)
    r=requests.get(request_url)
    data=r.text
    lst=json.loads(data)
    name_lst=[]
    for i in lst:
        name_lst.append(i['name'])
    #print(name_lst)
    life_span=[]
    for i in lst:
        life_span.append(i['life_span'])
    #print(life_span)
    temperament=[]
    for i in lst:
        temperament.append(i['temperament'])
    #print(temperament)
    final=list(zip(name_lst,life_span,temperament))
    #print(final)
    return final

def print_dog():
    dog_lst=[]
    first=create_request_url(1,1)
    #print(first)
    dog_lst.append(first)
    second=create_request_url(2,2)
    #print(second)
    dog_lst.append(second)
    third=create_request_url(3,3)
    #print(third)
    dog_lst.append(third)
    fourth=create_request_url(4,4)
    #print(fourth)
    dog_lst.append(fourth)
    return dog_lst

def add_dogs_from_json(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Dogs (id INTEGER PRIMARY KEY, 'name' TEXT, 'life_span' TEXT, 'temperament' TEXT)")
    dog_lst=print_dog()
    #print(dog_lst)
    count=1
    for lst in dog_lst:
        for tup in lst:
            #print(tup[0])
            cur.execute("INSERT INTO Dogs(id, name, life_span, temperament) VALUES (?,?,?,?)", (count, tup[0], tup[1], tup[2]))
            count+=1
    conn.commit()

def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('dogs.db')
    add_dogs_from_json(cur, conn)

if __name__ == "__main__":
    main()
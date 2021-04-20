import json
import unittest
import sqlite3
import os
import requests

def read_cache(CACHE_FNAME):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    CACHE_FNAME = dir_path + '/' + "cache_petfinder.json"
    try:
        # Try to read the data from the file
        cache_file = open(CACHE_FNAME, 'r', encoding="utf-8")
        cache_contents = cache_file.read()  # If it's there, get it into a string
        # And then load it into a dictionary
        CACHE_DICTION = json.loads(cache_contents)
        # Close the file, we're good, we got the data in a dictionary.
        cache_file.close()
        return CACHE_DICTION
    except:
        CACHE_DICTION = {}
        return CACHE_DICTION

def write_cache(CACHE_FNAME, CACHE_DICT):
    CACHE_FNAME = "cache_petfinder.json"
    cache_file = open(CACHE_FNAME, 'w', encoding="utf-8")
    name = json.dumps(CACHE_DICT)
    cache_file.write(name)
    cache_file.close()

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

#curl -d "grant_type=client_credentials&client_id=xGlDDR1SOlgWhvQ1kwzGhJHIu2iQzB92DEAv0D5cGy0ufhgxs5&client_secret=xBAAKuwemHGPdAPxiEzcXKscq8fJD6istTPzjLOj" https://api.petfinder.com/v2/oauth2/token

def petfinder_create_request_url(cur, conn, access_token):
    base_url = "https://api.petfinder.com/v2/types/dog/breeds?limit=1"
    r = requests.get(base_url, headers={"Authorization": "Bearer " + access_token})
    data = r.text
    d = json.loads(data)
    dog_lst = []
    for i in d:
        new_lst=d[i]
    # print(new_lst)
        for one in new_lst:
        #print(one)
            for name in one.keys():
                if name=='name':
                    dog_lst.append(one[name])
    #print(dog_lst)
    return dog_lst

def petfinder_database(cur, conn, access_token):
    cur.execute("SELECT breed FROM Dogs")
    breed_lst = cur.fetchall()
    #print(breed_lst)
    cur.execute("CREATE TABLE IF NOT EXISTS Petfinder (num INTEGER PRIMARY KEY, 'breed' TEXT, 'city' TEXT, 'state' TEXT, 'country' TEXT)")
    dog_lst=petfinder_create_request_url(cur, conn, access_token)
    #print(dog_lst)
    name_lst=[]
    city_lst=[]
    state_lst=[]
    country_lst=[]
    #weather_lst=
    for i in breed_lst:
        #print(i)
        for x in i:
            #print(x)
            if x in dog_lst:
                #print(x)
                base_url="https://api.petfinder.com/v2/animals?breed={}&limit=1"
                request_url=base_url.format(x)
                r=requests.get(request_url, headers={"Authorization": "Bearer " + access_token})
                data=r.text
                data_dict=json.loads(data)
                #print(data_dict)
                for index in range(len(data_dict['animals'])):
                    name_lst.append(data_dict['animals'][index]['breeds']['primary'])
                    city_lst.append(data_dict['animals'][index]['contact']['address']['city'])
                    state_lst.append(data_dict['animals'][index]['contact']['address']['state'])
                    country_lst.append(data_dict['animals'][index]['contact']['address']['country'])
    #print(name_lst)
    #print(city_lst)

    for i in range(len(name_lst)):
        cur.execute("INSERT INTO Petfinder (num, breed, city, state, country) VALUES (?,?,?,?,?)",(i+1, name_lst[i], city_lst[i], state_lst[i], country_lst[i]))
        cur.execute("SELECT * FROM Petfinder JOIN Dogs WHERE Petfinder.breed = Dogs.breed")
    conn.commit()
        #print(data_dict)
    
            #print(i[x])
            #print(lst)

def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('dogs.db')
    access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJ4R2xERFIxU09sZ1dodlExa3d6R2hKSEl1MmlRekI5MkRFQXYwRDVjR3kwdWZoZ3hzNSIsImp0aSI6ImZhNTRhNmNkNGQzZWI1MjdjMmEzY2RmODUyZGJhZmFjZTdhNTM4NzdiMmNmMDlhZGNjMDQ2ODQ1NmFkNTE2YThhYmY3ZjIxOGI3YjUyM2RiIiwiaWF0IjoxNjE4ODg1MzkxLCJuYmYiOjE2MTg4ODUzOTEsImV4cCI6MTYxODg4ODk5MSwic3ViIjoiIiwic2NvcGVzIjpbXX0.SUgwKbm9XT3XJFNww3WVc7FdrT1X8sh3FprM4ycpyb3PwMuEJfVcjZcUqGF9OPa0SVIIWBjtaAyg59_sQPA2dkox62NG8r6fYEo1F8_7B2XEkKcSXAOGIR9VvZ5W6pRfhJshdxGnCYwZrVsUM_lXcgVuvtSSWB4vbA-phk-mQkIZ-711QzEuDObqq_qscTiTJvgvSw-ykSVKKlwYQ6phYW29UsCg7nIjsun9esb3ugTxJ3Q4QgewMNJKN-vIVpkCGo_BEXEDiOHJco0bHaPmCkAcZGkJHBaZa6bpcIuH5UZ5tqTcKKhSwIcYvERvIHOFM77_Xe02AWGyECqlSQJYnA"
    petfinder_database(cur, conn, access_token)
    petfinder_create_request_url(cur, conn, access_token)

if __name__ == "__main__":
    main()
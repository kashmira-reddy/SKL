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

#curl -d "grant_type=client_credentials&client_id=9Eg5BvX7HjlsB5jLqk23V8Nraj4AiRJOpVxEUjsYswcGYx19AV&client_secret=CxGRH6Mc6nQdqvjwd4PzZcyzE2e0kXOe9iuPEv9k" https://api.petfinder.com/v2/oauth2/token

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
    new_breed_lst=[]
    for x in breed_lst:
        new_breed_lst.append(x[0])
    #print(new_breed_lst)
    cur.execute("DROP TABLE IF EXISTS Petfinder")
    cur.execute("CREATE TABLE IF NOT EXISTS Petfinder (num INTEGER PRIMARY KEY, 'breed' TEXT, 'city' TEXT, 'state' TEXT, 'country' TEXT)")
    dog_lst=petfinder_create_request_url(cur, conn, access_token)
    #print(dog_lst)
    name_lst=[]
    city_lst=[]
    state_lst=[]
    country_lst=[]
    for i in dog_lst:
        #print(i)
        if i in new_breed_lst:
            #print(i)
            base_url="https://api.petfinder.com/v2/animals?breed={}&limit=1"
            request_url=base_url.format(i)
            r=requests.get(request_url, headers={"Authorization": "Bearer " + access_token})
            data=r.text
            data_dict=json.loads(data)
            #print(data_dict['animals'])
            for index in range(len(data_dict['animals'])):
                #print(index)
                if data_dict['animals'][index]['breeds']['primary']==i:
                    name_lst.append(data_dict['animals'][index]['breeds']['primary'])
                else:
                    name_lst.append(data_dict['animals'][index]['breeds']['secondary'])
                city_lst.append(data_dict['animals'][index]['contact']['address']['city'])
                state_lst.append(data_dict['animals'][index]['contact']['address']['state'])
                country_lst.append(data_dict['animals'][index]['contact']['address']['country'])

    #print(name_lst)
    #print(city_lst)

    cur.execute("SELECT MAX (num) FROM Petfinder")
    starting_idx=cur.fetchone()[0]
    if starting_idx==None:
        starting_idx=0
    for i in range(starting_idx, starting_idx+25):
        cur.execute("INSERT INTO Petfinder (breed, city, state, country) VALUES (?,?,?,?)",(name_lst[i], city_lst[i], state_lst[i], country_lst[i]))
        cur.execute("SELECT * FROM Petfinder JOIN Dogs WHERE Petfinder.breed = Dogs.breed")
    conn.commit()

    # for i in range(len(name_lst)):
    #     cur.execute("INSERT INTO Petfinder (breed, city, state, country) VALUES (?,?,?,?)",(name_lst[i], city_lst[i], state_lst[i], country_lst[i]))
    #     cur.execute("SELECT * FROM Petfinder JOIN Dogs WHERE Petfinder.breed = Dogs.breed")
    # conn.commit()
        #print(data_dict)
    
    #         #print(i[x])
    #         #print(lst)

def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('dogs.db')
    access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5RWc1QnZYN0hqbHNCNWpMcWsyM1Y4TnJhajRBaVJKT3BWeEVVanNZc3djR1l4MTlBViIsImp0aSI6ImVmODZkYTJjZGQ3NTZmOTU1YjU2YzdhODRiNzRiNWI0ZWYyZWViZTcyM2JkMGRiYzJjMzgzZTUyZjAwNjAyYmU3YzU1MzgyZjAyN2M3YjQ5IiwiaWF0IjoxNjE5MzcwNTI5LCJuYmYiOjE2MTkzNzA1MjksImV4cCI6MTYxOTM3NDEyOSwic3ViIjoiIiwic2NvcGVzIjpbXX0.gobzGQnrISti7Qdtdv0gM-3I4Z94nAYoldt5xTCpbwr1YSJ0x-jwDOzDSkXsyMy34Z1F_DHDTLAE95LV-Uo0WM9o4TgSjllE2ZxdFMdbPGraan2j-kshQ5_j4A-r-9kwR4yZQkwT_igzS9dF90S_UH3S9QvQgQQpwR2jiTAlXf_OqMNdRcRao0_9NuUesOtGwnDIAD7Str_0F7DQaNK5lKJWSVSc5M9qyjR7PAAsjldSgAJWfLiTm42g3NRxKMN2Rgdap0JbUaE1iMB588bFbAKg_hhuNuio8ihvhw6nfz93G2WIG3G_gXwqd37gru459OZ4_zSlJp31X3EidQ8_4A"
    petfinder_database(cur, conn, access_token)
    petfinder_create_request_url(cur, conn, access_token)

if __name__ == "__main__":
    main()
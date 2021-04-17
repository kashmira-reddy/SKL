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

# curl -d "grant_type=client_credentials&client_id=B5mDdOEMFNYqbWB7wkulyfldxDv3c21AylkZrs2LnbK6E7SvFF&client_secret=p7oEGqhddlotsXRl1HeEZgrrJ3nYr47wAUZvsQwm" https://api.petfinder.com/v2/oauth2/token

def create_request_url(cur, conn, access_token):
    base_url = "https://api.petfinder.com/v2/types/dog/breeds?limit=25"
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
        
def database(cur, conn, access_token):
    cur.execute("SELECT breed FROM Dogs")
    breed_lst = cur.fetchall()
    #print(breed_lst)
    cur.execute("CREATE TABLE IF NOT EXISTS Petfinder (id INTEGER PRIMARY KEY, 'breed' TEXT, 'location' TEXT)")
    dog_lst=create_request_url(cur, conn, access_token)
    #print(dog_lst)
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
                lst=json.loads(data)
                #print(lst)
        #     cur.execute("SELECT Petfinder.id JOIN Dogs AND Petfinder WHERE Petfinder.id = Dogs.id AND Dogs.breed = ?", (i, ))
        #     dogId = cur.fetchall()

        #     insert location data into row and petfinder where petfinder.id = dog.id
    print(lst)
    return lst

def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('dogs.db')
    access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJCNW1EZE9FTUZOWXFiV0I3d2t1bHlmbGR4RHYzYzIxQXlsa1pyczJMbmJLNkU3U3ZGRiIsImp0aSI6ImFlMTk4MDM3ZmFlZjNjMjAyY2U4OWY5OTQyZDdmZjIwMTFiOThkOWU5NTNjYjJiNGFhMGVlZjc1ZGJkZmM4NTZkM2Q4ZjNlZmRlNTc3YjMwIiwiaWF0IjoxNjE4Njk0MTkzLCJuYmYiOjE2MTg2OTQxOTMsImV4cCI6MTYxODY5Nzc5Mywic3ViIjoiIiwic2NvcGVzIjpbXX0.tUegyN3BrxlLbyZJUOM8qZ6bgC0fuAY6nachf26E-wMs1YkonQ3oLU4fiiBK3Tv-PnPGlxjwdZLGO6i7dgwRBh1CmbqhDANKseau82DGvCQAVGDEYrbHRiqde6jtjSRmGkp43_9YwcIXkGkItWT0aY1L5Sbqn_pBvLVE0EY90hZFGoIyQyqpMBjPn-wB2ljGnCpn4yVEqWwqWQ4PeYXoAN6-n7QpHHkrxPY8CQEAcY7uBYVT6W64mATJ3UDBoLWEPgXSeGd896DzxLgj3Xwyj2SIUI3mXVWdr6SStY8IjHlAwkDLcxtHPMxOQffdJMv_Hz-r3dEkt0b5kZDiXr_Q0w"
    database(cur, conn, access_token)
    create_request_url(cur, conn, access_token)

if __name__ == "__main__":
    main()
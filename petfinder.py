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

#curl -d "grant_type=client_credentials&client_id=xGlDDR1SOlgWhvQ1kwzGhJHIu2iQzB92DEAv0D5cGy0ufhgxs5&client_secret=Lb6VYGdVAjPTuTYKFE9DRduioX1JYKyXCb0fxRK1" https://api.petfinder.com/v2/oauth2/token

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
    access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJ4R2xERFIxU09sZ1dodlExa3d6R2hKSEl1MmlRekI5MkRFQXYwRDVjR3kwdWZoZ3hzNSIsImp0aSI6IjdmYmQ4YmVkYTRlOTJkOTUxMWVhODIxMzE2NDIwMjM3MzRkZmQ1ZjY3NTEyMGEwMmE4MTM1MWFjNWJmNTA1MzAwYTYyZWU5Yzc2M2JhNWVjIiwiaWF0IjoxNjE4OTMyODIzLCJuYmYiOjE2MTg5MzI4MjMsImV4cCI6MTYxODkzNjQyMywic3ViIjoiIiwic2NvcGVzIjpbXX0.Ddz_LsE9EOpPdVhfjGVjc91yoGV31z7FtAzxVu8et2A6Kx68Tp2-IyewiNXKkmyGtyy-9td6JHfwLT2eozdyMtW77Rny4prGTPvKtXXkJJbtmAQP9Y5WReJW-u1oMcbenQ3vs2RVkOxOBOWx8APbsruYkFCWnnZVmdH9_fC-6wN3TX6EuRy9QPnWbYTq5i2a-o0DVBeoLzt5lCdKdz0ASpdrbSkVYvYYyo3TumdtCf2KNlq7amauoZ0w6CXQcsEoZlZ-IxEAjWwCyB6O_7itXYOkthb09R2kqZhr8IHm9aFuXjuc5arBBGfzKW57AsVWhJFHIaPWk8qFF78U46AcQg"
    petfinder_database(cur, conn, access_token)
    petfinder_create_request_url(cur, conn, access_token)

if __name__ == "__main__":
    main()
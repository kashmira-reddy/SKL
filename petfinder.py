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
                print(x)
                #print(i)
                base_url="https://api.petfinder.com/v2/animals?breed={}&limit=1"
                request_url=base_url.format(x)
                r=requests.get(request_url, headers={"Authorization": "Bearer " + access_token})
                data=r.text
                data_dict=json.loads(data)
                print(data_dict)
                #print(lst)
            #cur.execute("INSERT INTO Petfinder (id,breed) VALUES (?,?,?)",(x, i[x], )) #add location
            cur.execute("SELECT Petfinder.id FROM Petfinder JOIN Dogs WHERE Petfinder.id = Dogs.id AND Dogs.breed = ?", (str(i), ))
    return cur.fetchall()
        #     insert location data into row and petfinder where petfinder.id = dog.id
    #print(data_dict)
    #return data_dict

   




def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('dogs.db')
    access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5RWc1QnZYN0hqbHNCNWpMcWsyM1Y4TnJhajRBaVJKT3BWeEVVanNZc3djR1l4MTlBViIsImp0aSI6IjkwYzE1NmE2OTQ0ZTZhYjhkNDVjNzYwNGIyNDFhODVlZDZiYWRlNTFlMTkxNDQ0YzhkNGJkNjQ1ZGU5ZDc1NmExZTdiOTQyZmRiZDRjZTc0IiwiaWF0IjoxNjE4Njk3MDYxLCJuYmYiOjE2MTg2OTcwNjEsImV4cCI6MTYxODcwMDY2MSwic3ViIjoiIiwic2NvcGVzIjpbXX0.tZAoY9quET-pXQnUGHceDgTkHltJcfJWWebsR7xiSgnvAdGwWFey2HGbx7cMsDcF2gw1LtNhOuUF-UHXxWbORD0dGCZXFJq5P9l84JQbQaDKkFWoBaYwmRSrmzmOex2DXKvLU1m6sBsFPochvJmBFsfAHBe-mTCpLHMAdgT8eeJj-wKM_I9wVKLH5TwFMlan1QMK0slq_8BcK1vuinm9SBR9L0hpaMh7wFWLf5unG09pTSw_ZNLfgr8xmoTGi3q-6H6TvR9Beg2MIljpGCD-Ktif7iv_vuWvIhjNcWZh-EkTLxsBqph54dHQZp3QqAqPElpLrm4TB4ARGccm2BQ-uQ"
    database(cur, conn, access_token)
    create_request_url(cur, conn, access_token)


if __name__ == "__main__":
    main()







# import json
# import unittest
# import sqlite3
# import os
# import requests

# def read_cache(CACHE_FNAME):
#     dir_path = os.path.dirname(os.path.realpath(__file__))
#     CACHE_FNAME = dir_path + '/' + "cache_petfinder.json"
#     try:
#         cache_file = open(CACHE_FNAME, 'r', encoding="utf-8") # Try to read the data from the file
#         cache_contents = cache_file.read()  # If it's there, get it into a string
#         CACHE_DICTION = json.loads(cache_contents) # And then load it into a dictionary
#         cache_file.close() # Close the file, we're good, we got the data in a dictionary.
#         return CACHE_DICTION
#     except:
#         CACHE_DICTION = {}
#         return CACHE_DICTION

# def write_cache(CACHE_FNAME, CACHE_DICT):
#     CACHE_FNAME="cache_petfinder.json"
#     cache_file = open(CACHE_FNAME, 'w', encoding="utf-8")
#     name=json.dumps(CACHE_DICT)
#     cache_file.write(name)
#     cache_file.close()

# def setUpDatabase(db_name):
#     path = os.path.dirname(os.path.abspath(__file__))
#     conn = sqlite3.connect(path+'/'+db_name)
#     cur = conn.cursor()
#     return cur, conn

# # key="B5mDdOEMFNYqbWB7wkulyfldxDv3c21AylkZrs2LnbK6E7SvFF"
# # secret="3q8b6OiXvC9ypRTd0Jr56tOVDAfQmf5KgeJ4bsAd"

# #access_token="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJCNW1EZE9FTUZOWXFiV0I3d2t1bHlmbGR4RHYzYzIxQXlsa1pyczJMbmJLNkU3U3ZGRiIsImp0aSI6Ijk4YTYzYzVjY2NhZThiYTI5ZTVjZTBkY2NiYzZlYzBhYzFjYzE1ZWZmYmFlOWRlYmY3NmQ2NGEyOWFkMmJlMTM0MmZlOTc3MTVlMDkxN2UzIiwiaWF0IjoxNjE4NDk5NDc0LCJuYmYiOjE2MTg0OTk0NzQsImV4cCI6MTYxODUwMzA3NCwic3ViIjoiIiwic2NvcGVzIjpbXX0.jKzhZdQCZfekjqay8FS6STvG6HB2TRgPckFiKT68Diab42J1CpvA_CzAeWYzjtLSVzqx_EJo-wMCklK6TaikOyrkp_m_1vnPOTC2XWVi5VOulJlWAw4C7ThzPaxDp_E8zCT-JIr-sTX8Lpol54Xpqc9Ciqz3nq5I8OpEaa6sUYh6r-8iyNRe6iuOQXXw_w5trDYh9EVkcgPCjvOYJHBBMKe5AlH1HbaTruY_B5ve_Kc_LsOnLQH3rlx7_tT8cj2nXk8UcxeucfnChEJxdS3OkVMxYcyDeF2UbzHUX1f8T_Ncsto1sjzyZosZw3QCxaHnzDSMqdLYN8xCJ_RQ-dz9qg"

# def database(cur, conn, access_token):
#     base_url="https://api.petfinder.com/v2/animals?limit=25"
#     #params = {"breed": breed, "location": location}
#     #r=requests.get(base_url, headers={"Authorization": "Bearer " + access_token}, params=params)
    
#     cur.execute("SELECT breed FROM Dogs")
#     lst2 = cur.fetchall()
#     cur.execute("CREATE TABLE IF NOT EXISTS Petfinder (id INTEGER PRIMARY KEY, 'breed' TEXT, 'location' TEXT)")
#     for i in lst2:
#         params = {"breed": i}
#         # "location": location}
#         r=requests.get(base_url, headers={"Authorization": "Bearer " + access_token}, params=params)
#         data=r.text
#         lst=json.loads(data)
        
#         cur.execute("SELECT Petfinder.id JOIN Dogs AND Petfinder WHERE Petfinder.id = Dogs.id AND Dogs.breed = ?", (i, ))
#         dogId = cur.fetchall()
        
#         # insert location data into row and petfinder where petfinder.id = dog.id
#     print(lst)
#     return lst
    


# def main():
#     # SETUP DATABASE AND TABLE
#     cur, conn = setUpDatabase('dogs.db')
#     access_token="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJCNW1EZE9FTUZOWXFiV0I3d2t1bHlmbGR4RHYzYzIxQXlsa1pyczJMbmJLNkU3U3ZGRiIsImp0aSI6Ijk4YTYzYzVjY2NhZThiYTI5ZTVjZTBkY2NiYzZlYzBhYzFjYzE1ZWZmYmFlOWRlYmY3NmQ2NGEyOWFkMmJlMTM0MmZlOTc3MTVlMDkxN2UzIiwiaWF0IjoxNjE4NDk5NDc0LCJuYmYiOjE2MTg0OTk0NzQsImV4cCI6MTYxODUwMzA3NCwic3ViIjoiIiwic2NvcGVzIjpbXX0.jKzhZdQCZfekjqay8FS6STvG6HB2TRgPckFiKT68Diab42J1CpvA_CzAeWYzjtLSVzqx_EJo-wMCklK6TaikOyrkp_m_1vnPOTC2XWVi5VOulJlWAw4C7ThzPaxDp_E8zCT-JIr-sTX8Lpol54Xpqc9Ciqz3nq5I8OpEaa6sUYh6r-8iyNRe6iuOQXXw_w5trDYh9EVkcgPCjvOYJHBBMKe5AlH1HbaTruY_B5ve_Kc_LsOnLQH3rlx7_tT8cj2nXk8UcxeucfnChEJxdS3OkVMxYcyDeF2UbzHUX1f8T_Ncsto1sjzyZosZw3QCxaHnzDSMqdLYN8xCJ_RQ-dz9qg"
#     database(cur, conn, access_token)

# if __name__ == "__main__":
#     main()
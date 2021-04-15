import json
import unittest
import sqlite3
import os
import requests

def read_cache(CACHE_FNAME):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    CACHE_FNAME = dir_path + '/' + "cache_petfinder.json"
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
    CACHE_FNAME="cache_petfinder.json"
    cache_file = open(CACHE_FNAME, 'w', encoding="utf-8")
    name=json.dumps(CACHE_DICT)
    cache_file.write(name)
    cache_file.close()

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

# key="B5mDdOEMFNYqbWB7wkulyfldxDv3c21AylkZrs2LnbK6E7SvFF"
# secret="3q8b6OiXvC9ypRTd0Jr56tOVDAfQmf5KgeJ4bsAd"

#access_token="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJCNW1EZE9FTUZOWXFiV0I3d2t1bHlmbGR4RHYzYzIxQXlsa1pyczJMbmJLNkU3U3ZGRiIsImp0aSI6Ijk4YTYzYzVjY2NhZThiYTI5ZTVjZTBkY2NiYzZlYzBhYzFjYzE1ZWZmYmFlOWRlYmY3NmQ2NGEyOWFkMmJlMTM0MmZlOTc3MTVlMDkxN2UzIiwiaWF0IjoxNjE4NDk5NDc0LCJuYmYiOjE2MTg0OTk0NzQsImV4cCI6MTYxODUwMzA3NCwic3ViIjoiIiwic2NvcGVzIjpbXX0.jKzhZdQCZfekjqay8FS6STvG6HB2TRgPckFiKT68Diab42J1CpvA_CzAeWYzjtLSVzqx_EJo-wMCklK6TaikOyrkp_m_1vnPOTC2XWVi5VOulJlWAw4C7ThzPaxDp_E8zCT-JIr-sTX8Lpol54Xpqc9Ciqz3nq5I8OpEaa6sUYh6r-8iyNRe6iuOQXXw_w5trDYh9EVkcgPCjvOYJHBBMKe5AlH1HbaTruY_B5ve_Kc_LsOnLQH3rlx7_tT8cj2nXk8UcxeucfnChEJxdS3OkVMxYcyDeF2UbzHUX1f8T_Ncsto1sjzyZosZw3QCxaHnzDSMqdLYN8xCJ_RQ-dz9qg"

def database(cur, conn, access_token):
    base_url="https://api.petfinder.com/v2/animals?limit=25"
    #params = {"breed": breed, "location": location}
    #r=requests.get(base_url, headers={"Authorization": "Bearer " + access_token}, params=params)
    
    cur.execute("SELECT breed FROM Dogs")
    lst2 = cur.fetchall()
    cur.execute("CREATE TABLE IF NOT EXISTS Petfinder (id INTEGER PRIMARY KEY, 'breed' TEXT, 'location' TEXT)")
    for i in lst2:
        params = {"breed": i}
        # "location": location}
        r=requests.get(base_url, headers={"Authorization": "Bearer " + access_token}, params=params)
        data=r.text
        lst=json.loads(data)
        
        cur.execute("SELECT Petfinder.id JOIN Dogs AND Petfinder WHERE Petfinder.id = Dogs.id AND Dogs.breed = ?", (i, ))
        dogId = cur.fetchall()
        
        # insert location data into row and petfinder where petfinder.id = dog.id
    print(lst)
    return lst
    


def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('dogs.db')
    access_token="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJCNW1EZE9FTUZOWXFiV0I3d2t1bHlmbGR4RHYzYzIxQXlsa1pyczJMbmJLNkU3U3ZGRiIsImp0aSI6Ijk4YTYzYzVjY2NhZThiYTI5ZTVjZTBkY2NiYzZlYzBhYzFjYzE1ZWZmYmFlOWRlYmY3NmQ2NGEyOWFkMmJlMTM0MmZlOTc3MTVlMDkxN2UzIiwiaWF0IjoxNjE4NDk5NDc0LCJuYmYiOjE2MTg0OTk0NzQsImV4cCI6MTYxODUwMzA3NCwic3ViIjoiIiwic2NvcGVzIjpbXX0.jKzhZdQCZfekjqay8FS6STvG6HB2TRgPckFiKT68Diab42J1CpvA_CzAeWYzjtLSVzqx_EJo-wMCklK6TaikOyrkp_m_1vnPOTC2XWVi5VOulJlWAw4C7ThzPaxDp_E8zCT-JIr-sTX8Lpol54Xpqc9Ciqz3nq5I8OpEaa6sUYh6r-8iyNRe6iuOQXXw_w5trDYh9EVkcgPCjvOYJHBBMKe5AlH1HbaTruY_B5ve_Kc_LsOnLQH3rlx7_tT8cj2nXk8UcxeucfnChEJxdS3OkVMxYcyDeF2UbzHUX1f8T_Ncsto1sjzyZosZw3QCxaHnzDSMqdLYN8xCJ_RQ-dz9qg"
    database(cur, conn, access_token)

if __name__ == "__main__":
    main()
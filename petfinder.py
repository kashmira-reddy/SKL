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

#curl -d "grant_type=client_credentials&client_id=B5mDdOEMFNYqbWB7wkulyfldxDv3c21AylkZrs2LnbK6E7SvFF&client_secret=Y9vdaRqu4dJNpqXfkX2W0FEQKC5jzzT9hz77Tn7F" https://api.petfinder.com/v2/oauth2/token





def create_request_url(cur, conn, access_token):
    base_url = "https://api.petfinder.com/v2/types/dog/breeds?limit=1"
    r = requests.get(base_url, headers={"Authorization": "Bearer " + access_token})
    data = r.text
    d = json.loads(data)
    dog_lst = []
    count = 0
    while count < 25:
        for i in d:
            new_lst=d[i]
        # print(new_lst)
            for one in new_lst:
            #print(one)
                for name in one.keys():
                    if name=='name':
                        dog_lst.append(one[name])
                        count+=1
    #print(dog_lst)
    return dog_lst
        
def database(cur, conn, access_token):
    cur.execute("SELECT breed FROM Dogs")
    breed_lst = cur.fetchall()
    #print(breed_lst)
    cur.execute("CREATE TABLE IF NOT EXISTS Petfinder (num INTEGER PRIMARY KEY, 'breed' TEXT, 'city' TEXT)")
    dog_lst=create_request_url(cur, conn, access_token)
    #print(dog_lst)
    name_lst=[]
    city_lst=[]
    for i in breed_lst:
        #print(i)
        for x in i:
            #print(x)
            if x in dog_lst:
                #print(x)
                #print(i)
                base_url="https://api.petfinder.com/v2/animals?breed={}&limit=1"
                request_url=base_url.format(x)
                r=requests.get(request_url, headers={"Authorization": "Bearer " + access_token})
                data=r.text
                
                data_dict=json.loads(data)
                #print(data_dict)
            
                for index in range(len(data_dict['animals'])):
                
                    name_lst.append(data_dict['animals'][index]['breeds']['primary'])
                    city_lst.append(data_dict['animals'][index]['contact']['address']['city'])
    #print(name_lst)
    print(city_lst)
    for i in range(len(name_lst)):
        cur.execute("INSERT INTO Petfinder (num, breed, city) VALUES (?,?,?)",(i+1, name_lst[i], city_lst[i])) #add location #iterate over doglist again
                    # #print(name_lst)
        cur.execute("SELECT * FROM Petfinder JOIN Dogs WHERE Petfinder.breed = Dogs.breed")
    conn.commit()
        #print(data_dict)
    
            #print(i[x])
            #print(lst)
    
    # name_lst=[]
    # for i in range(len(data_dict['animals'])):
    #     name_lst.append(data_dict['animals'][i]['breeds']['primary'])
    #print(name_lst)
    # print(name_lst)
    # latitude=[]
    # for i in data_dict:
    #     latitude.append(i['latitude'])
    # #print(life_span)
    # longitude=[]
    # for i in data_dict:
    #     longitude.append(i['longitude'])
    # #print(temperament)
    # final=list(zip(name_lst,latitude,longitude))
    # #print(final)
    

    # return final
        #     insert location data into row and petfinder where petfinder.id = dog.id
    #print(data_dict)
    #return data_dict

#dog table: breed, id, height, weight, temperament
#petfinder table: we are getting breed, latitude, longitude, id
#location table: city, state, country based on coordinates

#calculation: how many of each dog breed in each country


   




def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('dogs.db')
    access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJCNW1EZE9FTUZOWXFiV0I3d2t1bHlmbGR4RHYzYzIxQXlsa1pyczJMbmJLNkU3U3ZGRiIsImp0aSI6ImRmYTgzOWE0ODFiODUyZjU2MTI4OTJjOGRkZTA5YzRmYWY3MjJiOTc0ZWY5ODA2ODgyZGJlZGNmNTQ0YTZkZmEwY2JjMzk5YTIyMDdlMjVjIiwiaWF0IjoxNjE4ODU1NzA0LCJuYmYiOjE2MTg4NTU3MDQsImV4cCI6MTYxODg1OTMwNCwic3ViIjoiIiwic2NvcGVzIjpbXX0.P9ecWig-YXsCN931BISBNXL0yipg1bkferbVGdMtto7Y-vd0kEc91LqRnhsQvYwC7QFeqZAiguKdahoqCZV5ErqLydOpODTvC_40Ul3_wBeQpqzvKMM9fbKVk5Hm7ezWmKF8fmjkCZAOpH8fWyAw_peI79CbOdWOfS6J-lS1BKo5PGSkUnsd-cOtc3dzj19sA-BVlL_yUzpvVMxDi0xN1Cb92GpM9lG1mEcpU2BBXaun5hJ9Ni7yE3bRyLDcaA3wcZnSaTXflcLJwVWyFqn0-mod0ZFwn799dBhX7tEDpdMN8WnuLlo_ERexBGKDEtTN95g0GeI_N0jSqOoN8bHkGg"
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
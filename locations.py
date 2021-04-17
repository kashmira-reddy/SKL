import json
import unittest
import sqlite3
import os
import requests

def read_cache(CACHE_FNAME):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    CACHE_FNAME = dir_path + '/' + "cache_locations.json"
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
    CACHE_FNAME="cache_locations.json"
    cache_file = open(CACHE_FNAME, 'w', encoding="utf-8")
    name=json.dumps(CACHE_DICT)
    cache_file.write(name)
    cache_file.close()

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


def database(cur, conn):

    # url = "https://wft-geo-db.p.rapidapi.com/v1/geo/countries"

    # headers = {
    #     'x-rapidapi-key': "87f9585f5amshdbd854af653b797p1eda27jsnc90391356883",
    #     'x-rapidapi-host': "wft-geo-db.p.rapidapi.com"
    # }

    # response = requests.request("GET", url, headers=headers)

    # print(response.text)

    # url = "https://wft-geo-db.p.rapidapi.com/v1/geo/adminDivisions"

    # querystring = {"countryIds":"US"}

    # headers = {
    #     'x-rapidapi-key': "87f9585f5amshdbd854af653b797p1eda27jsnc90391356883",
    #     'x-rapidapi-host': "wft-geo-db.p.rapidapi.com"
    # }

    # response = requests.request("GET", url, headers=headers, params=querystring)

    #print(response.text)

    

    
    # url = "https://wft-geo-db.p.rapidapi.com/v1/geo/countries/US/regions"

    # headers = {
    #     'x-rapidapi-key': "87f9585f5amshdbd854af653b797p1eda27jsnc90391356883",
    #     'x-rapidapi-host': "wft-geo-db.p.rapidapi.com"
    # }

    # response = requests.request("GET", url, headers=headers)

    #print(response.text)
    # url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities/Q65/locatedIn"

    # headers = {
    #     'x-rapidapi-key': "87f9585f5amshdbd854af653b797p1eda27jsnc90391356883",
    #     'x-rapidapi-host': "wft-geo-db.p.rapidapi.com"
    # }
    # url = "https://andruxnet-world-cities-v1.p.rapidapi.com/"

    # querystring = {"searchby":"city"}

    # headers = {
    #     'x-rapidapi-key': "87f9585f5amshdbd854af653b797p1eda27jsnc90391356883",
    #     'x-rapidapi-host': "andruxnet-world-cities-v1.p.rapidapi.com"
    # }

    # response = requests.request("GET", url, headers=headers, params=querystring)

    # print(response.text)

    # url = "https://countries-cities.p.rapidapi.com/location/city/nearby"

    # querystring = {"latitude":"55.11","longitude":"37.02","radius":"25","min_population":"99","max_population":"10000"}

    # headers = {
    #     'x-rapidapi-key': "87f9585f5amshdbd854af653b797p1eda27jsnc90391356883",
    #     'x-rapidapi-host': "countries-cities.p.rapidapi.com"
    # }

    # response = requests.request("GET", url, headers=headers, params=querystring)

    # print(response.text)  

    url = "https://wft-geo-db.p.rapidapi.com/v1/geo/adminDivisions"

    headers = {
        'x-rapidapi-key': "87f9585f5amshdbd854af653b797p1eda27jsnc90391356883",
        'x-rapidapi-host': "wft-geo-db.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)

    print(response.text)
    # counter=0
    # # while counter != 10:
    # response = requests.request("GET", url, headers=headers)
        # counter+=1

    print(response.text)
    data=response.text
    data_dict=json.loads(data)
    county_lst=[]
    print(data_dict)
    for i in data_dict:
        county_lst.append(i['latitude'])
    print(county_lst)
    state_lst=[]
    for i in data_dict:
        state_lst.append(i[0])
    #print(life_span)
    country_lst=[]
    for i in data_dict:
        country_lst.append(i[0])
    #print(temperament)
    final=list(zip(county_lst,state_lst,country_lst))
    #print(final)
    return final









    # # base_url="api.geonames.org/postalCodeSearch?key="

    # # cur.execute("SELECT breed FROM Dogs")
    # lst2 = cur.fetchall()
    # cur.execute("CREATE TABLE IF NOT EXISTS Petfinder (id INTEGER PRIMARY KEY, 'breed' TEXT, 'location' TEXT)")
    # for i in lst2:
    #     params = {"breed": i}
    #     # "location": location}
    #     r=requests.get(base_url, headers={"Authorization": "Bearer " + access_token}, params=params)
    #     data=r.text
    #     lst=json.loads(data)
        
    #     cur.execute("SELECT Petfinder.id JOIN Dogs AND Petfinder WHERE Petfinder.id = Dogs.id AND Dogs.breed = ?", (i, ))
    #     dogId = cur.fetchall()
        
    #     # insert location data into row and petfinder where petfinder.id = dog.id
    # print(lst)
    # return lst
    

def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('dogs.db')
    database(cur, conn)

if __name__ == "__main__":
    main()
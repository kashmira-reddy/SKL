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

def weather_create_request_url(cur, conn):
    cur.execute('SELECT City, State, Country FROM Petfinder')
    x=cur.fetchall()
    #print(x)
    cur.execute("CREATE TABLE IF NOT EXISTS Weather (num2 INTEGER PRIMARY KEY, 'city' TEXT, 'state' TEXT, 'country' TEXT, 'weather' TEXT)")
    
    # might not need city, state, country - use id instead
    # which weather data to collect?
    # loop through first 25 - len of table (count)=0 start at length; increment count; break - repeat

    for tup in x:
        base_url = f"http://api.openweathermap.org/data/2.5/weather?q={tup[0]},{tup[1]},{tup[2]}&appid=e6367458ffd6fac896cd01a8ec82131c" 
        r = requests.get(base_url)
        data = r.text
        d = json.loads(data)
    print(d)
        # for i in d:
        #     new_lst=d[i]
        #     print(new_lst)
    #     for name in new_lst.keys():
    #         if name=='name':
    #             weather_lst.append(i[name])
    # print(weather_lst)
    # return weather_lst
    for i in range(len(x)):
        cur.execute("INSERT INTO Weather (num2, city, state, country, weather) VALUES (?,?,?,?,?)",(i+1, city_lst[i], state_lst[i], country_lst[i], weather_lst[i]))
        cur.execute("SELECT * FROM Weather JOIN Petfinder WHERE Weather.city = Petfinder.city AND Weather.state = Petfinder.state")
    conn.commit()

def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('dogs.db')
    weather_create_request_url(cur, conn)

if __name__ == "__main__":
    main()
import json
import unittest
import sqlite3
import os
import requests

def read_cache(CACHE_FNAME):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    CACHE_FNAME = dir_path + '/' + "cache_weather.json"
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
    CACHE_FNAME = "cache_weather.json"
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
    #cur.execute("CREATE TABLE IF NOT EXISTS Weather (num2 INTEGER PRIMARY KEY, 'city' TEXT, 'state' TEXT, 'country' TEXT, 'weather' TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS Weather (num2 INTEGER PRIMARY KEY, 'weather' TEXT, 'temp' TEXT, 'humidity' TEXT)")

    # might not need city, state, country - use id instead
    # loop through first 25 - len of table (count)=0 start at length; increment count; break - repeat
    # what is the 25 limit?
    # what exactly are we supposed to select and calculate? do we need a new table?
    
    weather_lst=[]
    temp_lst=[]
    humidity_lst=[]
    d = []
    for tup in x:
        base_url = f"http://api.openweathermap.org/data/2.5/weather?q={tup[0]},{tup[1]},{tup[2]}&units=imperial&appid=e6367458ffd6fac896cd01a8ec82131c" 
        r = requests.get(base_url)
        data = r.text
        d.append(json.loads(data))
    #print(d)
    
    for i in d:
        #print(i)
        weather=i.get('weather', 0)
        if weather==0:
            weather_lst.append('None')
        else:
            weather_lst.append(i['weather'][0]['main'])
    #print(weather_lst)
        temp=i.get('main', 0)
        if temp==0:
            temp_lst.append('None')
        else:
            temp_lst.append(i['main']['feels_like'])
    #print(temp_lst)
        humidity=i.get('main', 0)
        if humidity==0:
            humidity_lst.append('None')
        else:
            humidity_lst.append(i['main']['humidity'])
    #print(humidity_lst)

    cur.execute("SELECT MAX (num2) FROM Weather")
    starting_idx=cur.fetchone()[0]
    if starting_idx==None:
        starting_idx=0
    for i in range(starting_idx, starting_idx+25):
        cur.execute("INSERT INTO Weather (weather, temp, humidity) VALUES (?,?,?)",(weather_lst[i], temp_lst[i], humidity_lst[i]))
        cur.execute("SELECT * FROM Weather JOIN Petfinder WHERE Weather.num2 = Petfinder.num")
    conn.commit()

def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('dogs.db')
    weather_create_request_url(cur, conn)

if __name__ == "__main__":
    main()
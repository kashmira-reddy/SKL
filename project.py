import json
import unittest
import os
import requests

def read_cache(CACHE_FNAME):
    """
    This function reads from the JSON cache file and returns a dictionary from the cache data.
    If the file doesn’t exist, it returns an empty dictionary.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    CACHE_FNAME = dir_path + '/' + "cache_dogs.json"
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
    """
    This function encodes the cache dictionary (CACHE_DICT) into JSON format and
    writes the JSON to the cache file (CACHE_FNAME) to save the search results.
    """
    CACHE_FNAME="cache_dogs.json"
    cache_file = open(CACHE_FNAME, 'w', encoding="utf-8")
    name=json.dumps(CACHE_DICT)
    cache_file.write(name)
    cache_file.close()

API_KEY = "c2f60506-7838-48ae-a824-97ddeae1d5fd"



def create_request_url(breed):
    base_url="https://api.thedogapi.com/v1/breeds/search?q={}"
    request_url=base_url.format(breed)
    r=requests.get(request_url)
    data=r.text
    lst=json.loads(data)
    
    name_lst=[]
    name_lst.append(lst[0]['name'])
    # print(lst[0]['name'])
    life_span=[]
    life_span.append(lst[0]["life_span"])
    #print(life_span)
    temperament=[]
    temperament.append()
    return lst

print(create_request_url("Bloodhound"))
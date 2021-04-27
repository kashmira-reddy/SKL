import json
import unittest
import sqlite3
import os
import requests
import matplotlib
import matplotlib.pyplot as plt

def read_cache(CACHE_FNAME):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    CACHE_FNAME = dir_path + '/' + "data_process.json"
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
    CACHE_FNAME = "data_process.json"
    cache_file = open(CACHE_FNAME, 'w', encoding="utf-8")
    name = json.dumps(CACHE_DICT)
    cache_file.write(name)
    cache_file.close()

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

'''#1 Average Lifespan of Dog Breeds by State'''

def life_span_by_state(cur, conn):
    cur.execute("SELECT life_span FROM Dogs JOIN Petfinder WHERE Petfinder.breed = Dogs.breed")
    life_span=cur.fetchall()
    life_span_lst=[]
    for i in life_span:
        life_span_lst.append(i[0])
    #print(life_span_lst)
    cur.execute("SELECT state FROM Petfinder JOIN Dogs WHERE Dogs.breed = Petfinder.breed")
    state=cur.fetchall()
    state_lst=[]
    for i in state:
        state_lst.append(i[0])
    #print(state_lst)
    combo=list(zip(life_span_lst, state_lst))
    #print(combo)
    dict1={}
    for i in combo:
        years=i[0]
        state=i[1]
        if state not in dict1:
            x=[]
            x.append(years)
            dict1[state]=x
            #print(dict1)
        else:
            dict1[state].append(years)
    #print(dict1)
    
    count_lst=[]
    for i in dict1.values():
        #print(i)
        count=0
        for j in i:
            count+=float(j[:2])
        avg=count/len(i)
        count_lst.append(avg)
    #print(count_lst)
    round_count=[]
    for i in count_lst:
        x=round(i,2)
        round_count.append(x)
    #print(round_count)
    
    state2=[]
    for item in dict1:
        state2.append(item)
    #print(state2)
    combo2=list(zip(state2, round_count))
    data1=dict(combo2)
    #print(data1)
    return data1

def life_span_by_state_data_viz(cur,conn):
    data1=life_span_by_state(cur, conn)
    state=[]
    avg_life=[]
    for i in data1:
        state.append(i)
        avg_life.append(data1[i])
    plt.bar(state, avg_life, color=['red','darkblue'])
    plt.xlabel('States')
    plt.ylabel('Average Lifespan in Years')
    plt.title('Average Lifespan of Dog Breeds per State')
    plt.show()

'''#2 Number of Cities with Clouds and Clear Weather Conditions'''

def cities_with_clouds_or_clear(cur, conn):
    cur.execute("SELECT city FROM Petfinder JOIN Weather WHERE Weather.num2 = Petfinder.num")
    cities=cur.fetchall()
    cities_lst=[]
    for i in cities:
        cities_lst.append(i[0])
    #print(cities_lst)
    cur.execute("SELECT weather FROM Weather JOIN Petfinder WHERE Petfinder.num = Weather.num2")
    weather=cur.fetchall()
    weather_lst=[]
    for i in weather:
        weather_lst.append(i[0])
    #print(weather_lst)
    combo=list(zip(cities_lst, weather_lst))
    #print(combo)

    cloud_cities=[]
    for i in combo:
        city=i[0]
        cloud=i[1]
        if cloud=="Clouds":
            cloud_cities.append(city)
    #print(cloud_cities)
    num1=len(cloud_cities)
    #print(num)

    clear_cities=[]
    for i in combo:
        city=i[0]
        clear=i[1]
        if clear=="Clear":
            clear_cities.append(city)
    #print(cloud_cities)
    num2=len(clear_cities)

    #print(num)
    data2={}
    data2['Clouds']=num1
    data2['Clear']=num2
    #print(data)
    return data2

def cities_with_clouds_or_clear_data_viz(cur, conn):
    data2=cities_with_clouds_or_clear(cur, conn)
    weather=[]
    cities_num=[]
    for i in data2:
        weather.append(i)
        cities_num.append(data2[i])
    plt.bar(weather, cities_num,color=['lime','fuchsia'])
    plt.xlabel('Weather Condition')
    plt.ylabel('Number of Cities')
    plt.title('Number of Cities with Clouds and Clear Weather Conditions')
    plt.show()

'''#3 Average Weight of Dog Breeds per State'''

def weight_by_state(cur, conn):
    cur.execute("SELECT weight FROM Dogs JOIN Petfinder WHERE Petfinder.breed = Dogs.breed")
    weight=cur.fetchall()
    weight_lst=[]
    for i in weight:
        weight_lst.append(i[0])
    #print(weight_lst)
    cur.execute("SELECT state FROM Petfinder JOIN Dogs WHERE Dogs.breed = Petfinder.breed")
    state=cur.fetchall()
    state_lst=[]
    for i in state:
        state_lst.append(i[0])
    #print(state_lst)
    combo=list(zip(weight_lst, state_lst))
    #print(combo)
    dict1={}
    for i in combo:
        years=i[0]
        state=i[1]
        if state not in dict1:
            x=[]
            x.append(years)
            dict1[state]=x
            #print(dict1)
        else:
            dict1[state].append(years)
    #print(dict1)
    
    count_lst=[]
    for i in dict1.values():
        #print(i)
        count=0
        for j in i:
            if j=='up - 18':
                count+=18
            else:
                if j[:3].__contains__('-'):
                    count+=float(j[:2])
                else:
                    count+=float(j[:3])
        avg=count/len(i)
        count_lst.append(avg)
    #print(count_lst)
    round_count=[]
    for i in count_lst:
        x=round(i,2)
        round_count.append(x)
    #print(round_count)
    
    state2=[]
    for item in dict1:
        state2.append(item)
    combo2=list(zip(state2, round_count))
    data3=dict(combo2)
    #print(data3)
    return data3

def weight_by_state_data_viz(cur,conn):
    data3=weight_by_state(cur, conn)
    state=[]
    weight=[]
    for i in data3:
        state.append(i)
        weight.append(data3[i])
    plt.bar(state, weight, color=['yellow','navy'])
    plt.xlabel('States')
    plt.ylabel('Average Weight in Pounds')
    plt.title('Average Weight of Dog Breeds per State')
    plt.show()

'''#4 Average Height of Dog Breeds per State'''

def height_by_state(cur, conn):
    cur.execute("SELECT height FROM Dogs JOIN Petfinder WHERE Petfinder.breed = Dogs.breed")
    height=cur.fetchall()
    height_lst=[]
    for i in height:
        height_lst.append(i[0])
    #print(weight_lst)
    cur.execute("SELECT state FROM Petfinder JOIN Dogs WHERE Dogs.breed = Petfinder.breed")
    state=cur.fetchall()
    state_lst=[]
    for i in state:
        state_lst.append(i[0])
    #print(state_lst)
    combo=list(zip(height_lst, state_lst))
    #print(combo)
    dict1={}
    for i in combo:
        height2=i[0]
        state=i[1]
        if state not in dict1:
            x=[]
            x.append(height2)
            dict1[state]=x
            #print(dict1)
        else:
            dict1[state].append(height2)
    #print(dict1)
    
    count_lst=[]
    for i in dict1.values():
        #print(i)
        count=0
        for j in i:
            #print(j)
            x=j.replace('-',' ')
            count+=float(x[:4])
        avg=count/len(i)
        count_lst.append(avg)
    #print(count_lst)
    round_count=[]
    for i in count_lst:
        x=round(i,2)
        round_count.append(x)
    #print(round_count)
    
    state2=[]
    for item in dict1:
        state2.append(item)
    combo2=list(zip(state2, round_count))
    data4=dict(combo2)
    #print(data4)
    return data4

def height_by_state_data_viz(cur,conn):
    data4=height_by_state(cur, conn)
    state=[]
    height=[]
    for i in data4:
        state.append(i)
        height.append(data4[i])
    fig, ax = plt.subplots()
    ax.plot(state, height, '-c')
    ax.set_xlabel('States')
    ax.set_ylabel('Average Height in Feet')
    ax.set_title('Average Height of Dog Breeds per State')
    ax.grid()
    plt.show()   

def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('dogs.db')
    
    data1_processed=life_span_by_state(cur, conn)
    #print(data1_processed)
    life_span_by_state_data_viz(cur, conn)
    
    data2_processed=cities_with_clouds_or_clear(cur, conn)
    #print(data2_processed)
    cities_with_clouds_or_clear_data_viz(cur, conn)
    
    data3_processed=weight_by_state(cur, conn)
    #print(data3_processed)
    weight_by_state_data_viz(cur,conn)
    
    data4_processed=height_by_state(cur, conn)
    #print(data4_processed)
    height_by_state_data_viz(cur,conn)

    # with open('output.txt', 'w') as outfile:
    #         temp_list = []
    #         temp_list.append(data1_processed)
    #         temp_list.append(data2_processed)
    #         temp_list.append(data3_processed)
    #         temp_list.append(data4_processed)
    #         json.dump(temp_list, outfile)

    with open('data_process.txt', 'w') as outfile:
        print("1.Average Lifespan of Dog Breeds by State:", file=outfile)
        print(data1_processed, file=outfile)
        print("2.Number of Cities with Clouds and Clear Weather Conditions:", file=outfile)
        print(data2_processed, file=outfile)
        print("3.Average Weight of Dog Breeds per State:", file=outfile)
        print(data3_processed, file=outfile)
        print("4.Average Height of Dog Breeds per State:", file=outfile)
        print(data4_processed, file=outfile)

if __name__ == "__main__":
    main()


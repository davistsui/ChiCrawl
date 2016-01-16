#original code for search algorithm
#finds best bar within walking distance radius that fulfills user preferences
#repeats search using that bar as the starting location
#set intersection of db and dictionary inspired by PA2

from math import radians, cos, sin, asin, sqrt
import sqlite3
import json
import re
import os

#query the yelp sql database
def search_sql(args, lon, lat):
    terms = args.keys()
    connection = sqlite3.connect('data/bars3.db')
    connection.create_function("distance", 4, distance_between)
    c = connection.cursor()
    results = make_query(c, args, lon, lat)
    return results

def make_query(c, args, lon, lat):
    #make query if user does not care about price
    if "price" not in args.keys():
        s = 'SELECT name, longitude, latitude, weighted_rank, distance(' + str(lon) + ', ' + str(lat) + ', longitude, latitude) AS walking_distance FROM bars WHERE walking_distance < ? GROUP BY name'
        bars = c.execute(s, (args.get("distance"),)).fetchall()
        return bars

    #make query if user has price preference
    else:
        s = 'SELECT name, longitude, latitude, weighted_rank, distance(' + str(lon) + ', ' + str(lat) + ', longitude, latitude) AS walking_distance FROM bars WHERE walking_distance < ? AND price < ? GROUP BY name'  
        bars = c.execute(s, (args.get("distance"),args.get("price"))).fetchall()
        return bars

#Haversine equation; Google maps will handle the actual directions, 
#this is a quicker way to get an estimate of walking distance
def distance_between(lon1, lat1, lon2, lat2):

    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    lon_dist = lon2-lon1
    lat_dist = lat2-lat1
    a = sin(lat_dist/2)**2 + cos(lat1)*cos(lat2)*sin(lon_dist/2)**2
    c = 2*asin(sqrt(a))

    km = 6367*c
    mile = km*0.621371
    return mile

#search Foursquare dictionary
def search_dict(terms):
    menu_dict = json.load(open("data/foursquare.json"))
    words = re.findall("[a-zA-Z]\w*", terms)
    w = []
    for word in words:
        w.append(word.lower())
    words = w
    menu_set = set()
    for word in words:
        results = menu_dict.get(word)
        #if there are no results for a search term, ignore it
        if not results:
            continue
        if menu_set:
            menu_set = menu_set & set(results)
        else:
            menu_set = set(results)
            
    return menu_set       

#Find bars that match the user search terms
def search_terms(user_input, name_sql_results, sql_results, bars_visited):
    terms = user_input.get("terms")

    #if the user searches for specific drinks, search foursquare dict and
    #perform set intersection on SQL and dictionary results, remove bars visited
    if terms:
        menu_results = search_dict(terms)
        join_results = set(name_sql_results) & menu_results
        join_results = join_results - set(bars_visited)
    
    #if no search terms, just remove the bars already visited from sql results
    else:
        join_results = set(name_sql_results) - set(bars_visited)

    #retrieve rest of SQL data for results
    rv = []
    for result in list(join_results):
        for sql_result in sql_results:
            if result == sql_result[0]:
                rv.append(sql_result)
    return rv
     

#reorganize list of bars by weighted rank
def sort_bars_by_wr(bars):
    ranked_bars = sorted(bars, key=lambda tup: tup[3], reverse=True)
    return ranked_bars

#searches SQL db and dictionary, returns results ordered by weighted rank
def get_bars(user_input, lon, lat, rv):
    sql_results = search_sql(user_input, lon, lat)
    name_sql_results = [x[0] for x in sql_results]
    bars = search_terms(user_input, name_sql_results, sql_results, rv)
    if not bars:
        return None
    sorted_bars = sort_bars_by_wr(bars) 
    return sorted_bars[0]

#Greedy search algorithm
def main(user_input, lat, lon):
    rv = []
    bars_visited = []

    #performs search for num_bars
    #changes lat, lon for search to be the location of that last bar
    for i in range(user_input.get("num_bars")):
        bar = get_bars(user_input, lon, lat, bars_visited)
        #if there is no result corresponding to search results
        if bar == None:
            return None
        rv.append(bar)
        bars_visited.append(bar[0])
        lon = bar[1]
        lat = bar[2]  
    return rv


    




#takes relevent information on bars scraped from yelp
#and stores it in a sql database

import json
import sqlite3
import glob

#iterates through each bar in json file
def load_json(fn):
    data = json.load(open(fn))
    bars = data.get("businesses")
    keys = bars[0].keys()
    for bar in bars:
        bar_info = get_bar_info(bar)
        #must have at least 5 reviews to be listed
        if bar_info[2] < 5:
            continue
        write_to_db(bar_info)


#pulls needed data for each bar, returns as list
def get_bar_info(bar):
    name = bar.get('name').encode('ascii', 'ignore')
    rating = bar.get('rating')
    num_reviews = bar.get('review_count')
    latitude = bar.get('location').get('coordinate').get('latitude')
    longitude = bar.get('location').get('coordinate').get('longitude')
    address = bar.get('location').get('display_address')[0].encode('ascii', 'ignore')
    bar_info = [name, rating, num_reviews, latitude, longitude, address]   
    return bar_info

#inserts data for a bar into the database
def write_to_db(bar_info):
    connection = sqlite3.connect('../data/bars3.db')
    c = connection.cursor()
    s = "INSERT OR IGNORE INTO bars (name, rating, num_reviews, latitude, longitude, address) VALUES (?,?,?,?,?,?)"
    c.execute(s, bar_info)
    connection.commit()
    connection.close()

if __name__ == "__main__":
    bar_files = glob.glob("bar_zip/*.json")
    for bar_file in bar_files:
        load_json(bar_file)

import csv
import os
import json

RES_DIR = os.path.join(os.path.dirname(__file__), '..', 'res')

def read_col(filename):
    with open(filename) as f:
        datareader = csv.reader(f)
        col = []
        [col.append(row[0]) for row in datareader]
    return col

def load_col(filename, col=0):
    with open(filename) as f:
        col = zip(*csv.reader(f))[0]
        return list(col)

def get_coor(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    lat = data['Lincoln Park']['location']['latitude']
    lon = data['Lincoln Park']['location']['longitude']
    return [lat, lon]


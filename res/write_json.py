import json

data = {
    'Hyde Park': 
        {'location': {'latitude': 41.79267, 'longitude': -87.59146}},
    'West Loop':
        {'location': {'latitude': 41.88245, 'longitude': -87.64467}},
    'Wicker Park':
        {'location': {'latitude': 41.90880, 'longitude': -87.679598}},
    'Logan Square':
        {'location': {'latitude': 41.92312, 'longitude': -87.70929}},
    'Lincoln Park': 
        {'location': {'latitude': 41.92143, 'longitude': -87.65130}}
}

with open('neighbor_coord.json', 'w') as f:
    json.dump(data, f)


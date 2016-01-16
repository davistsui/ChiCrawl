# uses the foursquare api
# uses bars3.db, the sqlite3 database scraped from the yelp api
# eventually stores a python dictionary in JSON with each word in menu/tag/phrase
# as the key and the list of corresponding restaurants as the value
import sqlite3
import foursquare
import json


# client id and secret needed to access the foursquare api
client = foursquare.Foursquare(
		client_id = 'JZ0P123UOI1WX2UA5GBKJ5R15EG5SXPJPQI43QBW12IX1BBT',
		client_secret = 'PFPZXOCWBJZULOP4KNPLX2USVTL34PPI1EVH15SIIC4QSZQQ'
		)


# this function reads the bars3.db sqlite3 data from yelp and
# returns a list of triple tuples with the following format:
# (name, latitude, longitude)
def get_venue_info():
	db = sqlite3.connect('bars3.db')
	c = db.cursor()
	# GROUP BY name makes sure that the bars in the list are unique
	s = 'SELECT name, latitude, longitude FROM bars GROUP BY name'
	venue_info_list = c.execute(s).fetchall()

	return venue_info_list


# returns a list of venue ids
def get_venue_id(venue_info_list):
	venue_id_list = []
	for bar in venue_info_list:
		name = bar[0]
		ll = str(bar[1]) + ',' + str(bar[2])
		# bar_info includes a list of 30 venues in the nearby area of the
		# specified lat and lon
		area_info = client.venues.search(params = {'name': name, 'll': ll})
		venue_id = ''
		# need to run through the list of 30 venues to find the one we want
		for venue in area_info['venues']:
			# used in instead of == here to prevent not matching
			# names with additional phrases in 4square vs. yelp
			if (venue['name'] in name) or (name in venue['name']):
				venue_id = venue['id']
				venue_id_list.append(venue_id)
				break
		# unable to find a matching venue id, append an empty id
		# this happens, only 919/1207 bars have a unique venue id
		if venue_id == '':
			venue_id_list.append(venue_id)

	return venue_id_list


# returns a list of individual words on the menu
# if the menu doesn't exist, then it will return ['']
def extract_menu(venue_id):
	venue_menu = client.venues.menu(venue_id)
	words = ''
	menus = venue_menu['menu']['menus']
	if menus.has_key('items'):
		for x in menus['items'][0]['entries']['items']:
			for y in x['entries']['items']:
				words = words + y['name'] + ' '	
	# cuts the last space, which is unnecessary
	words = words[:-1]
	# every character in the menu is in lower case
	words = words.lower()
	words = words.split()
	# if the menu doesn't exist
	if len(words) == 0:
		words.append('')

	return words


# returns a list of words in tags
def extract_tags(venue):
	venue_list = venue['venue']
	if 'tags' not in venue_list.keys():
		return ['']
	else:
		return venue_list['tags']


# returns a list of words in phrases
def extract_phrases(venue):
	venue_list = venue['venue']
	if 'phrases' not in venue_list.keys():
		return ['']

	phrase_list = venue_list['phrases']

	result = ''
	for p in phrase_list:
		result += p['phrase'] + ' '

	result = result.lower()
	result = result.split()
	if len(result) == 0:
		result = ['']
	return result


# returns a python dictionary with each word as a key and
# a list of restaurants as the key
def get_dict(venue_info_list, venue_id_list):
	result = {}
	i = 0
	for venue_id in venue_id_list:
		# it is possible to not be able to retrieve a venue id
		# skip in this case
		if venue_id == '':
			continue

		name = venue_info_list[i][0]

		venue = client.venues(venue_id)
		# take the union of words with set
		keywords = list(set(extract_menu(venue_id) + extract_tags(venue) +
							extract_phrases(venue)))

		for word in keywords:
			if result.has_key(word):
				if name not in result[word]:
					result[word].append(name)
			else:
				result[word] = [name]
		i+=1
	# this gets rid of the "" key
	del result[""]
	
	return result


def main():
	venue_info_list = get_venue_info()
	venue_id_list = get_venue_id(venue_info_list)
	d = get_dict(venue_info_list, venue_id_list)

	with open('foursquare.json', 'wb') as fp:
		json.dump(d, fp)


if __name__ == '__main__':
	main()

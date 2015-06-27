from pulsar import provider

icon = provider.ADDON.getAddonInfo('icon')

def search(query):
	url_search = "https://getstrike.net/api/v2/torrents/search/?phrase=%s+720" % (query)
	provider.log.info(url_search)
	response = provider.GET(url_search)
	results=[]
	if str(response.data) != '':
		items = provider.parse_json(response.data)
		nbrTorrents = items['results']
		for torrent in range(0, nbrTorrents):
			hash = items['torrents'][torrent]['torrent_hash']
			name = items['torrents'][torrent]['torrent_title']
			link = items['torrents'][torrent]['magnet_uri']
			magnet = link
			accept = True
			if name.find("720") == -1:
				accept = False
			if name.find('SPANISH') >= 0:
				accept = False
			if name.find("French") >= 0:
				accept = False
			if name.find("VOSTFR") >= 0:
				accept = False
			if accept:
				results.append({'name': name, 'uri': magnet, 'info_hash': hash})
	return results
		
def search_episode(info):
	title = info['title'].encode('utf-8') + ' S%02dE%02d' % (info['season'],info['episode'])
	provider.notify(message='Searching: ' + title +'...', header=None, time=1500, image=icon)
	return search(title)

def search_movie(info):
	title = info['title'].encode('utf-8') + ' %s' % (info['year'])
	provider.notify(message='Searching: ' + title +'...', header=None, time=1500, image=icon)
	return search(title)

#This registers your module for use
provider.register(search, search_movie, search_episode)

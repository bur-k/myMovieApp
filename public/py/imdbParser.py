import os, json, requests
from bs4 import BeautifulSoup

inputfile = "imdbLinks.txt"
outputfile = "imdbParserOutput.txt"
i=0

def getTitleIdAndYear(_html):
	meta = _html.find('meta', property='og:title')
	title = str(meta['content'][:-7])
	id = url[20:37]
	year = str(meta['content'][-5:-1])
	return (title.replace("'","''"), id, year)
	
def getPoster(_html):
	div = _html.find('div', class_='poster')
	img = (div.a.img['src'])
	return img[:img.find('_V1_')+4]+'.jpg'	
	
def getDirectors(_html):
	div = _html.find('div', class_='credit_summary_item')
	directors = div.text.split('(')[0]
	if ',' in directors:
		directors = directors[12:-1]
	else:
		directors = directors[11:-1]
	return directors

def getCasts(_html):
	table = _html.find('table', class_='cast_list')
	imgs = table.select('tr td a img')
	casts = _html.find_all('td', class_='character')
	castList = []
	for i in range(0, len(casts)):
		cast = {'fullname': imgs[i]['title'].replace("'","''"), 'role': casts[i].text.splitlines()[1].strip().replace("'","''").split(' /')[0], 'photo': '', 'imdbid':imgs[i].parent['href'][:16]}
		if 'loadlate' in imgs[i].attrs:
			cast['photo'] = imgs[i]['loadlate'][:imgs[i]['loadlate'].find('_V1_')+4]+'.jpg'
		else:
			cast['photo'] = 'https://m.media-amazon.com/images/G/01/IMDbPro/images/default_name._V142442227_UY289_CR46,0,196,289_.png'
		castList.append(cast)
	return castList
	
def getRuntimeAndBudget(_html):
	times = _html.find_all('time')
	runtime = str(times[1].contents[0])
	h3 = _html.find('h3', class_='subheading')
	budget = h3.find_next_siblings()[0].text.strip().splitlines()[0][7:]
	return (budget, runtime)
		
def getReleaseDateAndRating(_html):
	rating = _html.find('span', itemprop="ratingValue").text
	a = _html.find('a', title="See more release dates")
	releaseDate = a.text.strip().split('(')[0][:-1]
	return (rating, releaseDate)		

def getPhotos(_html):
	divs = _html.find_all('div', class_='mediastrip')
	photoList = ()
	for a in divs[0].contents:
		if a.name == 'a' and len(photoList) < 4:
			img = a.img['loadlate']
			photoList+=(img[:img.find('_V1_')+4]+'.jpg', )
	return photoList
	
def getVideos(_html):
	prev = 'https://www.imdb.com/videoembed/'
	videos = _html.find('div', class_='mediastrip_big').select('a')
	video = prev+videos[0].img['viconst']
	return video
	
def getGenres(_html):
	divs = _html.find_all('div', class_='see-more inline canwrap')
	genres = divs[1]
	genre = ''
	for i in genres:
		if i.name == 'a':
			genre+=', '+i.text.strip()	
	return genre[2:]
			
def getPlot(_html):
	plotMin = _html.find('div', class_='summary_text').text.strip()
	plot = _html.find('div', class_='inline canwrap').p.span.text.strip()
	return (plotMin.replace("'","''"), plot.replace("'","''"))
	
def getMovieData(_url):
	with requests.get(_url) as r:
		html = BeautifulSoup(r.text, 'html.parser')
	(title, id, year) = getTitleIdAndYear(html) # title, id, year
	global i
	i=i+1
	print(str(i)+'. '+title)
	(budget, runtime) = getRuntimeAndBudget(html) # runtime, budget
	(rating, releasedate) = getReleaseDateAndRating(html) # release date, rating
	poster = getPoster(html) # poster
	directors = getDirectors(html) # directors
	genre = getGenres(html) # genres
	(plotMin, plot) = getPlot(html) # plot
	photoList = getPhotos(html) # movie photos
	video = getVideos(html) # movie trailer
	castList = getCasts(html) # casts name, photo, id, role
	movie = {'title': title, 'movieid': id, 'year': year, 'budget': budget, 'runtime': runtime, 'rating': rating, 'poster': poster, 'directors': directors, 'releasedate': releasedate, 'genre': genre, 'plots': [{'min': plotMin},{'all': plot}], 'photos': photoList, 'trailer': video, 'cast': castList, 'price': '19.90'}
	return movie
	
def json2db(_movies):
	fout = open(outputfile, "w")
	for m in _movies:
		movieInsertQuery = 'insert into movies (title, imdbmid, year, budget, runtime, rating, poster, directors, releasedate, genre, plotmin, plot, photo1, photo2, photo3, trailer, price) values(\''+m['title']+'\', \''+m['movieid']+'\', \''+m['year']+'\', \''+m['budget']+'\', \''+m['runtime']+'\', \''+m['rating']+'\', \''+m['poster']+'\', \''+m['directors']+'\', \''+m['releasedate']+'\', \''+m['genre']+'\', \''+m['plots'][0]['min']+'\', \''+m['plots'][1]['all']+'\', \''+m['photos'][0]+'\', \''+m['photos'][1]+'\', \''+m['photos'][2]+'\', \''+m['trailer']+'\', \''+m['price']+'\');'
		fout.write(movieInsertQuery)
		for c in m['cast']:
			castInsertQuery = 'insert into casts (imdbcid, fullname, photo) select \''+c['imdbid']+'\', \''+c['fullname']+'\', \''+c['photo']+'\' where not exists(select imdbcid from casts where imdbcid=\''+c['imdbid']+'\');\n'
			movieCastInsertQuery = 'insert into movie_casts (mid, role, cid) select currval(\'movies_id_seq\'), \''+c['role']+'\', id from casts where imdbcid=\''+c['imdbid']+'\';\n'
			fout.write(castInsertQuery)
			fout.write(movieCastInsertQuery)
	
if __name__ == "__main__":
	if os.path.exists(outputfile):
		os.remove(outputfile)
	fin = open(inputfile, "r")
	
	movies = []
	for url in fin:
		movies.append(getMovieData(url.strip()))
	json2db(movies)
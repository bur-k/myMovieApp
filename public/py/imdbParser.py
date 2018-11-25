import os, json, requests
from bs4 import BeautifulSoup

inputfile = "imdbLinks.txt"
outputfile = "imdbParserOutput.txt"

def getTitleIdAndYear(_html):
	meta = _html.find('meta', property='og:title')
	title = str(meta['content'][:-7])
	id = url[20:37]
	year = str(meta['content'][-5:-1])
	return (title.replace("'",""), id, year)

def getCasts(_html):
	table = _html.find('table', class_='cast_list')
	imgs = table.select('tr td a img')
	casts = _html.find_all('td', class_='character')
	castList = []
	for i in range(0, len(casts)):
		if 'loadlate' in imgs[i].attrs:
			cast = {'fullname': imgs[i]['title'].replace("'",""), 'role': casts[i].text.splitlines()[1].strip().replace("'",""), 'photo': imgs[i]['loadlate'][:imgs[i]['loadlate'].find('_V1_')+4]+'.jpg', 'imdbid':imgs[i].parent['href'][:16]}
			castList.append(cast)
		else:
			cast = {'fullname': imgs[i]['title'].replace("'",""), 'role': casts[i].text.splitlines()[1].strip().replace("'",""), 'photo': 'https://m.media-amazon.com/images/G/01/IMDbPro/images/default_name._V142442227_UY289_CR46,0,196,289_.png', 'imdbid':imgs[i].parent['href'][:16]}
			castList.append(cast)
	return castList
	
def getRuntimeAndBudget(_html):
	times = _html.find_all('time')
	runtime = str(times[1].contents[0])
	divs = _html.find_all('div', 'txt-block')
	budget = divs[10].contents[2].strip()[:-1]
	return (budget, runtime)
		
def getReleaseDateAndRating(_html):
	spans = _html.find_all('span', 'attribute')
	rating = _html.find('span', itemprop="ratingValue").text
	releaseDate = str(spans[1].contents[0])
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
	return (plotMin.replace("'",""), plot.replace("'",""))
	
def getMovieData(_url):
	with requests.get(_url) as r:
		html = BeautifulSoup(r.text, 'html.parser')
	(title, id, year) = getTitleIdAndYear(html) # title, id, year
	print(title)
	(budget, runtime) = getRuntimeAndBudget(html) # runtime, budget
	(rating, releasedate) = getReleaseDateAndRating(html) # release date, rating
	genre = getGenres(html) # genres
	(plotMin, plot) = getPlot(html) # plot
	photoList = getPhotos(html) # movie photos
	video = getVideos(html) # movie trailer
	castList = getCasts(html) # casts name, photo, id, role
	movie = {'title': title, 'movieid': id, 'year': year, 'budget': budget, 'runtime': runtime, 'rating': rating, 'releasedate': releasedate, 'genre': genre, 'plots': [{'min': plotMin},{'all': plot}], 'photos': photoList, 'trailer': video, 'cast': castList}
	return movie
	
def json2db(_movies):
	fout = open(outputfile, "w")
	for m in _movies:
		movieInsertQuery = 'insert into movies (title, imdbmid, year, budget, runtime, rating,  releasedate, genre, plotmin, plot, photo1, photo2, photo3, trailer) values(\''+m['title']+'\', \''+m['movieid']+'\', \''+m['year']+'\', \''+m['budget']+'\', \''+m['runtime']+'\', \''+m['rating']+'\', \''+m['releasedate']+'\', \''+m['genre']+'\', \''+m['plots'][0]['min']+'\', \''+m['plots'][1]['all']+'\', \''+m['photos'][0]+'\', \''+m['photos'][1]+'\', \''+m['photos'][2]+'\', \''+m['trailer']+'\');'
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
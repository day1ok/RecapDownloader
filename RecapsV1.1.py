import time
from datetime import date, timedelta
import urllib2
from bs4 import BeautifulSoup
import re
import requests
import os

teamNameList = ['ana', 'ari', 'atl', 'bal', 'bos', 'cha', 'chn', 'cin', 'cle', 'col', 'det', 'hou', 'kca', 'lan', 'mia', 'mil', 'min', 'nya', 'nyn', 'oak', 'phi', 'pit', 'sdn', 'sea', 'sfn', 'sln', 'tba', 'tex', 'tor', 'was']

lineNumbers =[]
unparsedDownloadLinks = []
downloadLinks = []
seen = set()

cur_date = date.today()
start_date = cur_date
cur_date = cur_date-timedelta(days=1)

filePath = cur_date.strftime("%Y%m%d")
fileName = cur_date.strftime("%Y%m%d")+ '.txt'


#K:\Drive\Electronics Project\Python

def download_file(url):
    local_filename = filePath + '/' + url.split('/')[-2]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename + '.mp4', 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename

if not os.path.exists(filePath):
    os.makedirs(filePath)
#main
for team in teamNameList:
	url = ('http://honus-1064.appspot.com/?team='+ '%s' + '&date=' + cur_date.strftime("%Y%m%d")) % team 
	content = urllib2.urlopen(url)

	with open(os.path.join(filePath +'/'+ fileName),'a') as f:
		f.write(content.read())
		
lookup = 'Recap'

with open(filePath + '/' + fileName) as myFile:
	for num, line in enumerate(myFile, 1):
		if lookup in line:
			lineNumbers.append(num)

links = open(filePath + '/' + fileName).readlines()

for num in lineNumbers:
	#print links[num]
	soup = BeautifulSoup(links[num], "lxml")
	for tag in soup.findAll('a', href=True):
		unparsedDownloadLinks.append(tag['href'])

for x in unparsedDownloadLinks:
	if x not in seen:
		downloadLinks.append(x)
		seen.add(x)

for link in downloadLinks:
	download_file(link)


from BeautifulSoup import BeautifulSoup
from datetime import datetime
from googlemaps import GoogleMaps
import re
import urllib2

now = datetime.now()
#API key from blakeswanson.com
GMAPS = GoogleMaps('ABQIAAAAUWHRJGluxwxTNxzAAB2m_RTi_Pt_gz5MV-nrMRwKTuzjlX3-yxTRL6qrr4zoeewtmNmpi7E2ex1llQ')

def main():
  #oct 13th
  getBlotterData('http://www.pnwlocalnews.com/east_king/kir/news/131651253.html')
  #oct 6th
  #getBlotterData('http://www.pnwlocalnews.com/east_king/kir/news/130392973.html')
  #sept 29th
  #getBlotterData('http://www.pnwlocalnews.com/east_king/kir/news/130748293.html')
  #sept 22nd
  #getBlotterData('http://www.pnwlocalnews.com/east_king/kir/news/130748293.html')
  #sept 15th
  #getBlotterData('http://www.pnwlocalnews.com/east_king/kir/news/129903718.html')
  #sept 7th
  #getBlotterData('http://www.pnwlocalnews.com/east_king/kir/news/129418608.html')


def getBlotterData(url):
  page = urllib2.urlopen(url)
  soup = BeautifulSoup(page)  
  #gets body of blotter info
  storyBody = soup.find("div", {"id": "storyBody"})
  pList = str(storyBody)
  #split on all paragraphs
  pList = re.compile('<p>|<p class="..">').split(pList)

  for item in pList[:]:
    #clean up html markup
    item = item.replace('</p>,', '')
    item = re.sub(r'(<[^>]+>)', '', item)
    #finds date
    dayMatch = re.search(r'^[A-Z]\w{1,3}\.\s\d+', item)
    if dayMatch:	  
      date = grabDate(dayMatch.group())
    
    #finds crime, time and address (all in same paragraph)
    crimeMatch = re.search('^.+?:', item)
    if crimeMatch:
      crime = crimeMatch.group()
      item = item.replace(crime + ' ', '')    
      crime = crime.replace(':', '')
      time, item = getTime(item)
      address, description = getAddress(item)
      lat, lng = GMAPS.address_to_latlng(address)


      if crime != 'So keep your comments':
        record = {'datetime': datetime.strptime(date + ', ' + str(now.year) + ' ' + time, '%b. %d, %Y %I:%M %p'), 'crime': crime, 'address': address, 'lat': lat, 'lng': lng, 'description': description}
        print record['datetime']
        print record['crime']
        print record['address']
        print record['lat']
        print record['lng']
        print record['description']
        
        #c.execute("insert into kirklandCrimes ")   

def grabDate(date):
	monthCheck = re.search(r'^\D+?\.', date)
	#makes sure the month abreviation is only 3 characters long
	if (len(monthCheck.group()) >= 5):
		date = date.replace(monthCheck.group(), monthCheck.group()[0:3] + '.')
	return date

def getTime(item):
   if (item[0:4] == 'Noon'):
     item = item.replace(item[0:4], '12:00 p.m.')    
   timeMatch = re.search(r'^\d+?:\d{2}.[ap]\.m\.|\d.[ap]\.[m]\.|\d{2}.[ap]\.[m]\.', item)
   if timeMatch:
      time = timeMatch.group()
      item = item.replace(time + ', ', '')
      time = time.replace('.', '')
      #checks for time similar to 1 pm and fixes it to 1:00 pm
      timeCheck = re.search('^\d\ |^\d\d\ ', time)
      if timeCheck:
        timeCheck = timeCheck.group()
        timeCheck = timeCheck.replace(' ', '')
        time = time.replace(timeCheck, timeCheck + ':00')
      return time, item

def getAddress(item):
  if item:
    if (item[0:8] == 'downtown'):
      item = item.replace('downtown', 'Main Street');
    addressMatch = re.search('^.*(N\.E\.|NE|N\.W\.|NW|S\.W\.|SW|S\.E\.|SE|N\.|S\.|E\.|W\.|Street\.|St\.|Court\.|Ave\.|Avenue\.|Way\.|Lane\.|Place\.|Dr\.|Drive\.|Center\.|South\.|East\.|West\.|South\.|Plaza\.)', item[0:50])
    if addressMatch:
      address = addressMatch.group()
      description = item.replace(address + ' ', '')
      address = address + ', Kirkland WA'
    else:
      address = 'No address'
    return address, description

if __name__ == '__main__':
  main()

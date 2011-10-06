import urllib2
from BeautifulSoup import BeautifulSoup
from googlemaps import GoogleMaps
import re
from datetime import datetime


def getBlotterData(url):
  #declare variables
  crime, date, time, address, description = ('',)*5
  now = datetime.now()
  #API key from blakeswanson.com
  gmaps = GoogleMaps('ABQIAAAAUWHRJGluxwxTNxzAAB2m_RTi_Pt_gz5MV-nrMRwKTuzjlX3-yxTRL6qrr4zoeewtmNmpi7E2ex1llQ')
  #open URL
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
    item = re.sub('(<[^>]+>)', '', item)
    
    #finds date 
    dayMatch = re.search('^[A-Z]\w+\.\s\d+', item)
    if dayMatch:
      date = dayMatch.group()
      #if len(re.search('^\D+?\.'), date)
      #makes sure the month abreviation is only 3 characters long
      monthCheck = re.search('^\D+?\.', date)
      if (len(monthCheck.group()) >= 5):
        date = date.replace(monthCheck.group(), monthCheck.group()[0:3] + '.')

    #finds crime, time and address (all in same paragraph)
    crimeMatch = re.search('^.+?:', item)
    if crimeMatch:
      crime = crimeMatch.group()
      item = item.replace(crime + ' ', '')    
      crime = crime.replace(':', '')

      #finds time
      if (item[0:4] == 'Noon'):
        item = item.replace(item[0:4], '12:00 p.m.')
      
      timeMatch = re.search('^\d+?:\d{2}.[ap]\.[m]\.|\d.[ap]\.[m]\.|\d{2}.[ap]\.[m]\.', item)
      if timeMatch:
        time = timeMatch.group()
        item = item.replace(time + ', ', '')
        time = time.replace('.', '')
        #checks for time like 1 pm and fixes it
        timeCheck = re.search('^\d\ |^\d\d\ ', time)
        if timeCheck:
          timeCheck = timeCheck.group()
          timeCheck = timeCheck.replace(' ', '')
          time = time.replace(timeCheck, timeCheck + ':00')
          
        #if noonCheck:
         
        
      #finds address
      if (item[0:8] == 'downtown'):
        item = item.replace('downtown', 'Main Street');
      addressMatch = re.search('^.*(N\.E\.|NE|N\.W\.|NW|S\.W\.|SW|S\.E\.|SE|N\.|S\.|E\.|W\.|Street\.|St\.|Court\.|Ave\.|Avenue\.|Way\.|Lane\.|Place\.|Dr\.|Drive\.|Center\.|South\.|East\.|West\.|South\.)', item[0:50])
      if addressMatch:
        address = addressMatch.group()
        description = item.replace(address + ' ', '')
        address = address + ', Kirkland WA'
        lat, lng = gmaps.address_to_latlng(address)
      else:
        address = 'No address'

      
      
      if crime != 'So keep your comments':
        
        dict = {}
        dict['datetime'] = datetime.strptime(date + ', ' + str(now.year) + ' ' + time, '%b. %d, %Y %I:%M %p')
        dict['crime'] = crime
        dict['address'] = address
        dict['lat'] = lat
        dict['lng'] = lng
        dict['description'] = description
        print dict['datetime']
        print dict['crime']
        print dict['address']
        print dict['lat']
        print dict['lng']
        print dict['description']
        
        #c.execute("insert into kirklandCrimes ")   
    
#sept 29th
getBlotterData('http://www.pnwlocalnews.com/east_king/kir/news/130748293.html')

#sept 22nd
#getBlotterData('http://www.pnwlocalnews.com/east_king/kir/news/130748293.html')

#sept 15th
#getBlotterData('http://www.pnwlocalnews.com/east_king/kir/news/129903718.html')

#sept 7th
#getBlotterData('http://www.pnwlocalnews.com/east_king/kir/news/129418608.html')


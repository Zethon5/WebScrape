from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import time

print('What do you want to search?')
UserSearch = input()
UserSearch = UserSearch.replace(' ','+')

print('Would you like to show all relevant results?')
rResults = input()

if rResults.lower() == 'no':
    print('Only showing specified results.')
else:
    print('Showing all relevant results.')


OC_cars = 'https://orangecounty.craigslist.org/search/cta?query='+ UserSearch+'&sort=date'
uClient = uReq(OC_cars)
page_HTML = uClient.read()
uClient.close()
page_soup=soup(page_HTML, 'html.parser')
results = 1
chevy = 0
NotChevy = 0

for cars in page_soup.findAll('li',{'class':'result-row'}):

#-------------------------------------------------------------------FIND THE CAR
    try:
        headline = cars.find('a',{'class':'result-title hdrlnk'})
        headline = headline.text
    except:
        headline = 'No Headline found.'

#------------------------------------------------------------------FIND THE COST
    try:
        cost = cars.find('span',{'class':'result-price'})
        cost = cost.text

    except:
        cost = 'Cost not found.'

#----------------------------------------------------------------RESULTS DISPLAY

    if rResults.lower() == 'no':
        if UserSearch.lower() in headline.lower():
            print(str(results) + ' : ' + cost + ' : ' + headline)
            results +=1

    else:
        print(str(results) + ' : ' + cost + ' : ' + headline)
        results +=1
    #    chevy +=1
    #else:
    #    NotChevy += 1
    time.sleep(.1)
    if results == 11:
        break

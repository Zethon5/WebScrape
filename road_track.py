from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import time
import csv
import pandas as pd

#---------------------------------------------------------------------------------------------Websites to be parsed

rtCars = 'https://www.roadandtrack.com/new-cars/'
rtFD = 'https://www.roadandtrack.com/new-cars/first-drives/'
rtRT = 'https://www.roadandtrack.com/new-cars/road-tests/'
rtLT = 'https://www.roadandtrack.com/long-term-tests/'
rtRC = 'https://www.roadandtrack.com/new-cars/car-comparison-tests/'
rtFC = 'https://www.roadandtrack.com/new-cars/future-cars/'
rtTech = 'https://www.roadandtrack.com/new-cars/car-technology/'

Websites = [rtCars, rtFD, rtRT, rtLT, rtRC, rtFC, rtTech]

#-----------------------------------------------------------------------------------------------------------------
Search = ''

while Search.lower() != 'no':
    CarFind = 0
    #------------------------------------------------------------------------------Allow user to enter terms to find
    UserSearch = input('What would you like to search?')
    SearchTerms = UserSearch.split()
  
    #------------------------------------------------------------------------------------For Each Website from above
    for Website in Websites:
        uClient = uReq(Website)
        page_HTML = uClient.read()
        uClient.close()
        page_soup=soup(page_HTML, 'html.parser')

        #--------------------------------------------------------------------------For Every Article on the Website
        for Cars in page_soup.findAll('div',{'class':'full-item'}):
            col_names = ['title']
            data = pd.read_csv('titles.csv', names = col_names)
            data.set_index('title', inplace = True)
            headline = Cars.find('div',{'class':'full-item-content'})
            headline = Cars.find('a',{'class':'full-item-title item-title'})
            link = headline.get('href')
            headline = headline.text[2:-1]
            #-----------------------------------------------------------------------Search Article for wanted term.
            for Term in SearchTerms:
                if (Term.lower() in headline.lower()) and (headline not in data.index):
                    print('')
                    print(headline)
                    print(rtCars + link)
                    CarFind +=1
                    with open('titles.csv','a') as df: 
                        writer = csv.writer(df)
                        writer.writerow([headline])
                                            
    if CarFind == 0:
        print('')
        print('No New Articles Found.')
    Search = input('Would you like to search more?')

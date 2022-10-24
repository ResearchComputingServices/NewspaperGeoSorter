from operator import contains
from sqlite3 import paramstyle
from unittest import skip
import requests
from bs4 import BeautifulSoup
from scraperUtil import *


for state in stateNamesList:
    parsedWebPage = ParseWebpage(w3NewsBaseURL + state)
    allH3Sections = parsedWebPage.find_all('h3')

    print('Searching in ' + state + '...', end = '')
    
    outputFile = open(w3NewsOutputDir+state+'.csv','w')
    counter = 0
    for h3Section in allH3Sections:
        
        allH3Links = h3Section.find_all('a',href=True)

        for link in allH3Links:
            outputFile.write(link.string + ' : '+ link['href']+'\n')
            counter += 1

    print ('DONE!....Found: ', counter)

    outputFile.close()
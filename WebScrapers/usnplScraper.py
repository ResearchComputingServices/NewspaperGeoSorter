from operator import contains
from sqlite3 import paramstyle
from unittest import skip
import requests
from bs4 import BeautifulSoup

from scraperUtil import *

for stateName in stateNamesList:

    url = usnplBaseURL + stateNamesDict[stateName]
    parsedWebPage = ParseWebpage(url)
    mainTable = parsedWebPage.find_all('table')
    
    if not len(mainTable) == 1:
        print('ERROR: Too many tables found...', end='')
        input()
    else:
        allTableRows = mainTable[0].find_all('tr')
        outputFile = open(usnplOutputDir+stateName+'.csv','w')

        paperCounter = 0
        for aRow in allTableRows:
            linksInRow = aRow.find_all('a', href=True)
            if len(linksInRow) >= 2:
                paperCounter += 1
                outputFile.write(linksInRow[0].string+","+linksInRow[1]['href']+'\n')

        outputFile.close()

        print(url, ' : ', paperCounter)




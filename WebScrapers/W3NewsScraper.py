from operator import contains
from sqlite3 import paramstyle
from unittest import skip
import requests
from bs4 import BeautifulSoup

stateNamesList = [  'Alabama', 'Alaska', 'Arkansas', 'AmericanSamoa', 'Arizona',
                'California', 'Colorado', 'Connecticut', 'district-of-columbia', 'Delaware',
                'Florida', 'Georgia', 'Guam', 'Hawaii', 'Iowa', 'Idaho', 'Illinois', 'Indiana',
                'Kansas', 'Kentucky', 'Louisiana', 'Massachusetts', 'Maryland', 'Maine', 'Michigan',
                'Minnesota', 'Missouri', 'Mississippi', 'Montana', 'North-Carolina', 'North-Dakota',
                'Nebraska', 'New-Hampshire', 'New-Jersey', 'New-Mexico', 'Nevada', 'New-York', 'Ohio',
                'Oklahoma', 'Oregon', 'Pennsylvania', 'PuertoRico', 'Rhode-Island', 'South-Carolina',
                'South-Dakota', 'Tennessee', 'Texas', 'Utah', 'Virginia', 'VirginIslands', 'Vermont',
                'Washington', 'Wisconsin', 'West-Virginia', 'Wyoming']

baseURL = 'https://www.w3newspapers.com/usa/'

outputDir = './W3News_Output/'

# This function takes in a URL and returns a BeautifulSoup parsed object
def ParseWebpage(webpageURL):

    webPage = requests.get(webpageURL)
    webPageParsed = BeautifulSoup(webPage.content, 'html.parser')

    return webPageParsed


for state in stateNamesList:
    parsedWebPage = ParseWebpage(baseURL + state)
    allH3Sections = parsedWebPage.find_all('h3')

    print('Searching in ' + state + '...', end = '')
    
    outputFile = open(outputDir+state+'.csv','w')
    counter = 0
    for h3Section in allH3Sections:
        
        allH3Links = h3Section.find_all('a',href=True)

        for link in allH3Links:
            outputFile.write(link.string + ' : '+ link['href']+'\n')
            counter += 1

    print ('DONE!....Found: ', counter)

    outputFile.close()
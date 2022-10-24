from operator import contains
from sqlite3 import paramstyle
from unittest import skip
import requests
from bs4 import BeautifulSoup

stateNamesList = [  'Alabama', 'Alaska', 'Arkansas', 'American_Samoa', 'Arizona',
                'California', 'Colorado', 'Connecticut', 'Washington,_D.C.', 'Delaware',
                'Florida', 'Georgia_(U.S._state)', 'Guam', 'Hawaii', 'Iowa', 'Idaho', 'Illinois', 'Indiana',
                'Kansas', 'Kentucky', 'Louisiana', 'Massachusetts', 'Maryland', 'Maine', 'Michigan',
                'Minnesota', 'Missouri', 'Mississippi', 'Montana', 'North_Carolina', 'North_Dakota',
                'Nebraska', 'New_Hampshire', 'New_Jersey', 'New_Mexico', 'Nevada', 'New_York', 'Ohio',
                'Oklahoma', 'Oregon', 'Pennsylvania', 'Puerto_Rico', 'Rhode_Island', 'South_Carolina',
                'South_Dakota', 'Tennessee', 'Texas', 'Utah', 'Virginia', 'the_United_States_Virgin_Islands', 'Vermont',
                'Washington_(state)', 'Wisconsin', 'West_Virginia', 'Wyoming']

stateNamesDict = {  'Alabama' : 'AL', 
                    'Alaska' : 'AK', 
                    'Arkansas' : 'AR', 
                    'American_Samoa' : 'AS', 
                    'Arizona' : 'AZ',
                    'California' : 'CA', 
                    'Colorado' : 'CO', 
                    'Connecticut' : 'CT', 
                    'Washington,_D.C.' : 'DC', 
                    'Delaware' : 'DE',
                    'Florida' : 'FL', 
                    'Georgia_(U.S._state)' : 'GA', 
                    'Guam' : 'GU', 
                    'Hawaii' : 'HI', 
                    'Iowa' : 'IA', 
                    'Idaho' : 'ID', 
                    'Illinois' : 'IL', 
                    'Indiana' : 'IN',
                    'Kansas' : 'KS', 
                    'Kentucky' : 'KY', 
                    'Louisiana' : 'LA', 
                    'Massachusetts' : 'MA', 
                    'Maryland' : 'MD', 
                    'Maine' : 'ME', 
                    'Michigan' : 'MI',
                    'Minnesota' : 'MN', 
                    'Missouri' : 'MO', 
                    'Mississippi' : 'MS', 
                    'Montana' : 'MT', 
                    'North_Carolina' : 'NC', 
                    'North_Dakota' : 'ND',
                    'Nebraska' : 'NE', 
                    'New_Hampshire' : 'NH', 
                    'New_Jersey' : 'NJ', 
                    'New_Mexico' : 'NM', 
                    'Nevada' : 'NV', 
                    'New_York' : 'NY', 
                    'Ohio' : 'OH',
                    'Oklahoma' : 'OK', 
                    'Oregon' : 'OR', 
                    'Pennsylvania' : 'PA', 
                    'Puerto_Rico' : 'PR', 
                    'Rhode_Island' : 'RI', 
                    'South_Carolina' : 'SC',
                    'South_Dakota' : 'SD', 
                    'Tennessee' : 'TN', 
                    'Texas' : 'TX', 
                    'Utah' : 'UT', 
                    'Virginia' : 'VA', 
                    'the_United_States_Virgin_Islands' : 'VI', 
                    'Vermont' : 'VT',
                    'Washington_(state)' : 'WA', 
                    'Wisconsin' : 'WI', 
                    'West_Virginia' : 'WV', 
                    'Wyoming': 'WY'}


baseURL = 'https://www.usnpl.com/search/state?state='

outputDir = './USNPL_Output/'

# This function takes in a URL and returns a BeautifulSoup parsed object
def ParseWebpage(webpageURL):

    webPage = requests.get(webpageURL)
    webPageParsed = BeautifulSoup(webPage.content, 'html.parser')

    return webPageParsed


for stateName in stateNamesList:

    url = baseURL + stateNamesDict[stateName]
    parsedWebPage = ParseWebpage(url)
    mainTable = parsedWebPage.find_all('table')
    
    if not len(mainTable) == 1:
        print('ERROR: Too many tables found...', end='')
        input()
    else:
        allTableRows = mainTable[0].find_all('tr')
        outputFile = open(outputDir+stateName+'.csv','w')

        paperCounter = 0
        for aRow in allTableRows:
            linksInRow = aRow.find_all('a', href=True)
            if len(linksInRow) >= 2:
                paperCounter += 1
                outputFile.write(linksInRow[0].string+","+linksInRow[1]['href']+'\n')

        outputFile.close()

        print(url, ' : ', paperCounter)




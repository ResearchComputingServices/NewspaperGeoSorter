from operator import contains
from sqlite3 import paramstyle
from unittest import skip
import requests
from bs4 import BeautifulSoup

from scraperUtil import *

"""
Helper Functions
"""
# This function takes in the wiki URL for a newspaper and searchs the infobox located
# in the top right corner for the newspapers URL and returns it.
def HandleNewsPaperWiki(newsPaperWikiURL):
    fullNewspaperWikiURL = wikiBaseURL+newsPaperWikiURL
    newspaperWebPageParsed = ParseWebpage(fullNewspaperWikiURL)

    newspaperURL = 'URL Not Found'
   
    # Get the infocard element which contains the newspapers URL in the final row
    infoCardElement = newspaperWebPageParsed.find('table', class_='infobox vcard')

    if(infoCardElement is not None):

        urlRow = infoCardElement.find('th',string='Website')
        if urlRow is not None:
            urlRow = urlRow.find_parent()
            newspaperURL = urlRow.find('a', href=True)
            
            if newspaperURL is not None:
                newspaperURL = newspaperURL['href']
            else:
                newspaperURL = urlRow.find('td').string
        else:
            newspaperURL = "No URL Found in infobox"

    return newspaperURL
    
# This function looks at the first column of the row and determines how to access the newspaper URL
def HandleTableCell(row):
    # the data we are interested in is in the first column of the row
    tableCell = row.findChild()

    # These are the two peice of data we are trying to find
    newspaperURL = ''
    newspaperName = ''

    if tableCell is not None:
        newspaperLink = tableCell.find('a',href=True)

        newspaperName = tableCell.text

        if newspaperLink is None:
            newspaperURL = 'No URL Found'

            if newspaperName is not None:
                newspaperName = newspaperName.strip()
            else:
               newspaperName = tableCell.find('i').string.strip()
        else:
            if '/wiki' in newspaperLink['href']:
                newspaperURL = HandleNewsPaperWiki(newspaperLink['href'])
            elif('https' in newspaperLink['href'] ):
                newspaperURL = newspaperLink['href']
            elif('redlink'in newspaperLink['href']):
                newspaperURL = 'Dead Wiki Link'
            else:
                newspaperURL = 'Unhandled' 

    pair = [newspaperName.strip(), newspaperURL]

    return pair

# This function is one of two helper functions that searchs a webpage element
# for newspaper URLs (internal or external)
def HandleTable(tableElement):

    listOfPairs = []

    tbody = tableElement.find('tbody')
    tableRows = tbody.find_all('tr')

    # loop over all the rows in the table except the first one [1:] because it is the header row
    for row in tableRows[1:]:
        pair = HandleTableCell(row)
        listOfPairs.append(pair)

    return listOfPairs

# This is a quick helper function that searchs a string to see if it contains a string listed in skipWords
def ContainsSkipWord(checkString):    
    
    if checkString is not None:
        for word in skipWords:
            if word in checkString:
                return True
        
    return False

# This function is the other helper function for extracting newspaper URLS from a webpage element
# in this case it is search unordered lists
def HandleUnorderedList(uListElement):

    listOfPairs = []

    listItems = uListElement.find_all('li')

    for listItem in listItems:
        # Each list item contains 2 elements, one for the LOCATION and one for the 
        # newspaper name. However, they are not always in the same order so we need 
        # to check both
        listPair = listItem.findChildren()

        # search each link for any of the skipWords
        for child in listPair:

            if not ContainsSkipWord(child.string):
                newspaperName = child.text
                newspaperURL = ''
            
                newspaperLink = child.find('a',href=True)
                if newspaperLink is not None:
                    newspaperName = child.text

                    if '/wiki' in newspaperLink['href']:
                        newspaperURL = HandleNewsPaperWiki(newspaperLink['href'])
                    elif('https' in newspaperLink['href'] ):
                        newspaperURL = newspaperLink['href']
                    elif('redlink'in newspaperLink['href']):
                        newspaperURL = 'Dead Wiki Link'
                    else:
                        newspaperURL = 'Unhandled' 
                else:
                    newspaperURL = 'No URL Found'
  
                    if newspaperName is not None:
                        newspaperName = newspaperName.strip()

                pair = [newspaperName.strip(), newspaperURL]
                listOfPairs.append(pair)

                break

    return listOfPairs

# This function writes the URLs and paper names to a CSV file
def WriteToFile(state, listOfPairs):

    filename = '/'+ state + '.csv'
    file = open(wikiResultsDirectory+filename,"w")

    for pair in listOfPairs:
        outputLine = pair[0] + ',' + pair[1] + '\n'
        file.write(outputLine)

    file.close()

# This function analyzes the results from a state and counts
# how many URLs were successfully found
def CheckResults(listOfPairs):

    numberOfURLsFound = 0
    
    for pair in listOfPairs:
        found = True
        for term in failedTerms:
            if pair[1] == term:
                found = False
                break

        if found:
            numberOfURLsFound = numberOfURLsFound + 1
    
    return numberOfURLsFound

"""
The actual code starts here
"""

for state in stateNames:
    listOfPairs = []

    stateURL = baseStateNewsPapersURL + state

    # This block of code retrieves the table on the state newspapers website
    stateWebpageContentsParsed = ParseWebpage(stateURL)

    # Look for all the <h2> tags
    sectionHeaders = stateWebpageContentsParsed.find_all('h2')

    # We want to find headers which match the headers in ther targetHeaders list.
    # The text we are trying to match is contained in the 'span' tag of the headers
    noTargetHeadersFound = True
    for header in sectionHeaders:
        isTarget = False
        currentSpanID = ''
        foundHeader = ''

        spans = header.find_all('span', id=True)

        #print(header)

        for span in spans:
            currentSpanID = span['id']           

            #print(currentSpanID)

            # Here we loop over all the target headers and compare to the current span id
            # to determine if we should search this section for newspapers
            for targetHeader in targetHeaders:
                if(currentSpanID == targetHeader):
                    isTarget = True
                    foundHeader = targetHeader
                    noTargetHeadersFound = False
                    #print('FOUND')

        # If the header matches a target header we then need to determine if the section
        # contains a Table or an unodered list.
        if isTarget:
            nextSibling = header

            newspaperDataElementFound = False
            iAttempts = 1
            newListOfPairs = []
            while ~newspaperDataElementFound and iAttempts <= numberOfAttempts:
                nextSibling = nextSibling.find_next_sibling()

                if(nextSibling.name == 'table' ):
                    #print('TABLE FOUND')
                    newListOfPairs = HandleTable(nextSibling)
                    break
                elif(nextSibling.name == 'ul'):
                    #print('ULIST FOUND')
                    newListOfPairs = HandleUnorderedList(nextSibling)
                    break
                
                iAttempts += 1

            listOfPairs.extend(newListOfPairs)

    # Output the results
    print(state, " : ", len(listOfPairs) , ' (', CheckResults(listOfPairs),')')
    WriteToFile(state,listOfPairs)



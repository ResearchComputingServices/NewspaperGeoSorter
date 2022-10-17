import os
import sys

from time import sleep
from Util import *
from RawDataHandler import *

#########################################################
# Add a URL to the dictionary:
# we need to check if the URL already exists and if it 
# does we need to append to the value instead of just
# overwriting it
#########################################################

def AddURL2Dict(dict,url,state):

    # Construct the appropriate alternate URL    
    alternateURL = ''
    if not 'www.' in url:
        # add www to URL
        alternateURL = 'www.'+url
    else:
        # remove www from URL
        alternateURL = url[4:]

    if url in dict:
        if not state in dict[url]:
            dict[url] = dict[url] + ',' + state
    else:
        dict[url] = state

    if alternateURL in dict:
        if not state in dict[alternateURL]:
            dict[alternateURL] = dict[alternateURL] + ',' + state
    else:
        dict[alternateURL] = state
    
    return dict


#########################################################
# Load all the state sorted newspapers into a dictionary
# key = paperURL
# value = state
#########################################################

def GetDictionaryOfStatePapers():
    statePaperFiles = os.listdir(statePaperFilesLocation)

    dictionaryOfStatePapers = {}

    for filename in statePaperFiles:

         # the value in the dictionary is the stateName
        value = filename.split('.')[0]
        
        with open(statePaperFilesLocation + filename,'r') as openfileobject:
            for line in openfileobject:
                pair = line.split(',')
                if len(pair) == 2:
                    if not pair[1].strip() in ignoreList:

                        # Clean up the URL
                        url = pair[1].strip()
                        if 'http://' in url:
                            url = url[7:]
                        if 'https://' in url:
                            url = url[8:]
                        if url[-1] == '/':
                            url = url[:-1]
     
                        dictionaryOfStatePapers = AddURL2Dict(dictionaryOfStatePapers, url, value)

    return dictionaryOfStatePapers

######################################################
# this function updates the results stats
######################################################
def UpdateResults(state, dictResults):

    stateSplit = state.split(',')

    if len(stateSplit) == 1:
        if state in dictResults:
            dictResults[state] += 1
        else:
            dictResults[state] = 1
    else:
        for state in stateSplit:
            if state in dictResults:
                dictResults[state] += 1
            else:
                dictResults[state] = 1

######################################################
# this function does the actual sorting
######################################################

def SortArticlesInFile(year, month, filename, dictStatePapers, dictToIgnore, dictResults, debugFlag = False):
  
    # Get the data from the file data in a list of lists
    fullDataFrame = GetDataFrame(year, month, filename)

    # split the "meta data" from the article
    metaDataList, articleDictionary = SplitDataFrame(fullDataFrame)

    # Loop over the article meta data
    for row in metaDataList:

        # get the last item from the row which is the base URL
        url = row[-1]
     
        resultString = 'NOT FOUND'   
        found = False

        # the ignore list grows as more and more URLs are found to come from papers outside the USA
        if url not in dictToIgnore:
            
            if url in dictStatePapers:
                # this will return a comma seperated list of state names
                state = dictStatePapers[url]

                # update the list of results
                UpdateResults(state, dictResults)

                resultString = state
                
                found = True
                
        # if not found add this URL to the ignore list
        # storing it as a dictionary where the value is the number of times this URL is found
        if not found:
            if url in dictToIgnore:
                dictToIgnore[url] += 1
            else:
                dictToIgnore[url] = 1
        
        # Append the row with the resultString which is either a state name or 'NOT FOUND'
        row.append(resultString)

    # this is only needed for debugging
    if debugFlag:
        for row in metaDataList:
            DisplayRow(row)
            if row[-1] == 'NOT FOUND':
                input()

    # This function splits articles with multiple states into seperate rows
    metaDataList = HandleMultiStateEntries(metaDataList)

    # Save the data to the appropriate place in the directory structure
    SaveSortedArticles(year,month,metaDataList,articleDictionary)

######################################################
# This is where the main code starts
#####################################################

# Get a dictionary object where the KEY is a state and the VALUE is a list of newspaper URLs
dictStatePapers = GetDictionaryOfStatePapers()    
dictToIgnore = {}   # list of ignored URLS and counts number of times each is found
dictResults = {}    # counts the number of articles from each state

# Make sure that the command line args are present
if len(sys.argv) == 2:
    [year,month] = sys.argv[1].split(',')
else:
    print('ERROR: invalid command line args: ', sys.argv)
    exit(0)

print("Starting Job: ", month ,' / ', year)

currentDirectory = dataLocationBase+year+'/'+month+'/CSV/'
listOfFiles = listdir_nohidden(currentDirectory)

for filename in listOfFiles:
    # this is where all the magic happens
    SortArticlesInFile(year,month,filename, dictStatePapers, dictToIgnore, dictResults, False)

reprotsFileName = resultsOutputDirectory+'Reports/'+year+'_'+month+'_Report.txt'

ReportSortedDict(reprotsFileName,dictResults,100)
ReportForiegnTLDs(dictToIgnore,reprotsFileName)
ReportSortedDict(reprotsFileName,dictToIgnore,500)

print("DONE Job: ", month ,' / ', year)
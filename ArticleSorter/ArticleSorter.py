import os
import sys

import Util
from time import sleep
from RawDataHandler import *

######################################################
# this function does the actual sorting
######################################################

def SortArticlesInFile(year, month, filename, dictStatePapers, dictToIgnore, dictResults, debugFlag = False):
  
    # Get the data from the file data in a list of lists
    fullDataFrame = GetDataFrame(year, month, filename)

    # split the "meta data" from the article
    metaDataList, articleDictionary = Util.SplitDataFrame(fullDataFrame)

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
                Util.UpdateResults(state, dictResults)

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
            Util.DisplayRow(row)
            if row[-1] == 'NOT FOUND':
                input()

    # This function splits articles with multiple states into seperate rows
    metaDataList = Util.HandleMultiStateEntries(metaDataList)

    # Save the data to the appropriate place in the directory structure
    Util.SaveSortedArticles(year,month,metaDataList,articleDictionary)

######################################################
# This is where the main code starts
#####################################################

# Local testing command line call.
# python3 ArticleSorter.py 2016,September /home/nickshiell/storage/TestSet/ /home/nickshiell/storage/TestSet/SortedByState/ ../StateNewsPaperFiles/Combined/

# Make sure that the command line args are present
if len(sys.argv) == 5:
    [year,month] = sys.argv[1].split(',')
    Util.dataLocationBase = sys.argv[2]
    Util.resultsOutputDirectory = sys.argv[3]
    Util.statePaperFilesLocation = sys.argv[4]
else:
    print('ERROR: invalid command line args: ', sys.argv)
    print('Syntax Expected: ArticleSorter YEAR,MONTH INPUT_DIR OUTPUT_DIR NEWSPAPER_DIR')
    exit(0)

print("Starting Job: ", month ,' / ', year)
print("Input Data: ", Util.dataLocationBase)
print("Newspaper Data: ", Util.statePaperFilesLocation)
print("Output Data: ", Util.resultsOutputDirectory)

# Get a dictionary object where the KEY is a state and the VALUE is a list of newspaper URLs
dictStatePapers = Util.GetDictionaryOfStatePapers()    
dictToIgnore = {}   # list of ignored URLS and counts number of times each is found
dictResults = {}    # counts the number of articles from each state

currentDirectory = Util.dataLocationBase+year+'/'+month+'/CSV/'
listOfFiles = Util.listdir_nohidden(currentDirectory)

for filename in listOfFiles:
    # this is where all the magic happens
    SortArticlesInFile(year,month,filename, dictStatePapers, dictToIgnore, dictResults, False)

reprotsFileName = Util.resultsOutputDirectory+'Reports/'+year+'_'+month+'_Report.txt'

Util.ReportSortedDict(reprotsFileName,dictResults,100)
Util.ReportForiegnTLDs(dictToIgnore,reprotsFileName)
Util.ReportSortedDict(reprotsFileName,dictToIgnore,500)

print("DONE Job: ", month ,' / ', year)
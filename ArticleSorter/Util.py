import os
import operator
from pathlib import Path

########################################################################
# Common data
#######################################################################

dateStampWildcard = '20??-??-??T??:??:??Z'

monthList = [   'January', 'February', 'March', 'April', 
                'May', 'June', 'July', 'August', 
                'September', 'October', 'November', 'December'] 

statePaperFilesLocation = '../StateNewsPaperFiles/Combined/'

# Location of the data set
#dataLocationBase = '/Volumes/BaChu$/CC-NEWS-EN/'           # this is the location of the data when I run the code locally
dataLocationBase = '/home/nickshiell/storage/CC-NEWS-EN/'   # This is the production run location when on the VM
#dataLocationBase = '/home/nickshiell/storage/TestSet/DebugSet/'     # This is the test run location when on the VM
#dataLocationBase = '/home/nickshiell/storage/TestSet/'     # This is the test run location when on the VM

# This folder will contain files all the output
resultsOutputDirectory = '/home/nickshiell/storage/SortedByState/'
#resultsOutputDirectory = '/home/nickshiell/storage/TestSet/DebugSortedByState/'


# URL to ignore when loading state newspaper lists
ignoreList = [  'URL Not Found', 
                'Dead Wiki Link',
                'No URL Found',
                'No URL Found in infobox',
                'Unhandled',
                'MISSING']

# TLDs to keep
keepTLDList = ['com','net','org','edu','me']

########################################################################
# Function that returns a list of all none hidden objects in directory
#######################################################################

def listdir_nohidden(directory):

    listOfContents= []

    if os.path.exists(directory):

        listOfContents = os.listdir(directory)

        for item in listOfContents:
            if item.startswith('.'):
                listOfContents.remove(item)

    return listOfContents

########################################################################
# Function that returns a months number equivalent
#######################################################################

def MonthWordToNumber(monthWord):

    monthNumber = '-1'

    counter = 1
    for m in monthList:
        if m.lower() == monthWord.lower():
            monthNumber = str(counter)
            break
        else:
            counter += 1

    return monthNumber 

########################################################################
# Function that nicely displays a data row as a column
#######################################################################

def DisplayRow(row, maxLength = 750):
    print(len(row))

    for item in row:
        if len(item) < maxLength:
            print(item.strip(), '\t ***')
        else:
            print('ARTICLE\t ***')

########################################################################
# Function that nicely displays a sorted dictionary
#######################################################################
def DisplaySortedDict(aDict, nDisplay = 1000, reverse = True):
    sortedDict = sorted(aDict.items(), key=operator.itemgetter(1))
    
    if reverse:
        sortedDict.reverse()
    
    counter = 0
    for pair in sortedDict:
        print(pair[0], ' :  ', pair[1])

        if counter < nDisplay:
            counter += 1
        else:
            break

########################################################################
# Function that prints a sorted dictionary to the file name pass to it
#######################################################################
def ReportSortedDict(outputFileName, aDict, nDisplay = 1000, reverse = True):
  
    outputFile = open(outputFileName,'a+')
    
    sortedDict = sorted(aDict.items(), key=operator.itemgetter(1))
    
    if reverse:
        sortedDict.reverse()
    
    counter = 0
    for pair in sortedDict:
        outputFile.write(str(pair[0])+ ' :  '+ str(pair[1])+'\n')

        if counter < nDisplay:
            counter += 1
        else:
            break

    outputFile.close()

######################################################
# This function counts how many foriegn articles are
# contained in the list and keeps track of where they
# are from (ex. .de .jp .co.uk)
######################################################
def ReportForiegnTLDs(dictToIgnore,outputFileName):
    
    outputFile = open(outputFileName,'a+')

    dictOfForiegnTLDs = {}
    value = 0

    for key in dictToIgnore:
        
        tokenKey = key.split('.')

        curTLD = tokenKey[-1].strip()

        if not curTLD in keepTLDList:
            value += dictToIgnore[key]

            if not curTLD in dictOfForiegnTLDs:
                dictOfForiegnTLDs[curTLD] = dictToIgnore[key]
            else:
                dictOfForiegnTLDs[curTLD] += dictToIgnore[key]
    
    outputFile.write('# of Foriegn Articles: ' + str(value) + '\n')


    for tld in dictOfForiegnTLDs:
        outputFile.write(tld+ ' : '+ str(dictOfForiegnTLDs[tld])+'\n')

    outputFile.close()

########################################################################
# Function that nicely displays a dictionary
#######################################################################
def DisplayDict(aDict, nDisplay = 10000000):
    counter = 0
    for key in aDict:
        print(key, ' :  ', aDict[key])

        if counter < nDisplay:
            counter += 1
        else:
            break

########################################################################
# Splits the data frame in two parts [UID,Article] & [UID, the rest]
#######################################################################
def SplitDataFrame(fullDataFrame):
    metaDataList = []
    articleDictionary = {}

    for item in fullDataFrame:
        date = item[0]
        fullURL = item[1]
        length = item[2]
        title = item[3]
        article = item[4]
        UID = item[5]
        baseURL = item[6]

        articleDictionary[UID] = article

        metaDataList.append([date,fullURL,length,title,UID,baseURL])

    return metaDataList, articleDictionary

######################################################
# writes the data to a sorted folder structure...
# /state/year/month/FILES
######################################################
def HandleMultiStateEntries(metaDataList):
    
    newMetaDataList = []

    for row in metaDataList:
        # the assigned state is the last entry in the row
        stateEntry = row[-1]

        stateEntrySplit = stateEntry.split(',')

        # if there is more than one state listed need to make a seperate line
        if len(stateEntrySplit) > 1:           
            for state in stateEntrySplit:
                newRow = row
                newRow[-1] = state
                newMetaDataList.append(newRow.copy())

        else:
            newMetaDataList.append(row)

    return newMetaDataList
    
######################################################
# writes the data to a sorted folder structure...
# /state/year/month/FILES
######################################################
def SaveSortedArticles(year,month,metaDataList,articleDictionary):  

    # sort the metaDataList by the state name (last column)
    metaDataList.sort(key=lambda x: x[-1])    

    sortedDataDirectory = resultsOutputDirectory + 'States'

    # create an file object
    outputFile = open(sortedDataDirectory+'/empty.dat','w+')
    outputFile.close()

    nRows = len(metaDataList)
    iRow = 0
    while iRow < nRows:
        curRow = metaDataList[iRow]
        currentStateName = curRow[-1]

        # open the file if it has been closed
        if outputFile.closed:
            outputFileLocation = sortedDataDirectory + '/' + currentStateName + '/' + year + '/' + month + '/'
            
            # create the folder if it doesnt exist
            Path(outputFileLocation).mkdir(parents=True, exist_ok=True)

            outputFilename = currentStateName + '_' + year + '_' + month + '.csv'
            outputFile = open(outputFileLocation + outputFilename, 'a+')

        # write what we want to the file
        date = curRow[0].strip()
        fullURL = curRow[1].strip()
        length = curRow[2].strip()
        title = curRow[3].strip()
        UID = curRow[4].strip()
        #article = 'ARTICLE'
        article = articleDictionary[UID].strip()
        outputStr = date+','+fullURL+','+length+','+title+','+article+'\n'
        outputFile.write(outputStr)              
        
        # check if the next row has the same state name as the current one
        # if not close the file
        if iRow+1 < nRows:
            nextRow = metaDataList[iRow+1]
            if not nextRow[-1] == curRow[-1]:
                outputFile.close()
        else:
            outputFile.close()

        iRow += 1

######################################################
# this function saves the results to a file
######################################################

def SaveResultsToFile(dataFrame, maxLength = 750):
    print('Writing to file...')

    # sort the dataFrame by the state name (last column)
    dataFrame.sort(key=lambda x: x[-1])    

    outputFile = open(resultsOutputDirectory+'empty.dat','w+')
    outputFile.close()

    nRows = len(dataFrame)
    iRow = 0
    while iRow < nRows-1:
        curRow = dataFrame[iRow]
        nextRow = dataFrame[iRow+1]

        # open the file if it has been closed
        if outputFile.closed:
            outputFilename = curRow[-1]+'.csv'
            outputFile = open(resultsOutputDirectory + outputFilename, 'a+')

        # write what we want to the file
        outputStr = ''
        rowLength = len(curRow)
        itemCounter = 0
        while itemCounter < rowLength-1:
            item = curRow[itemCounter]
            if len(item) < maxLength:
                outputStr += item.strip() + ','
            itemCounter += 1
        
        #for item in curRow: 
        #    if len(item) < maxLength:
        #        outputStr += item.strip() + ','
        #    else:
        #        outputStr += ('ARTICLE,')    
    
        outputFile.write(outputStr[:-1]+'\n')

        if not nextRow[-1] == curRow[-1]:
            outputFile.close()

        iRow += 1



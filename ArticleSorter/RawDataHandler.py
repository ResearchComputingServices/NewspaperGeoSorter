#import pandas
import os
import re
import fnmatch

from Util import *

from curses.ascii import isspace
from urllib.parse import urlsplit, urlunsplit
import hashlib

########################################################################
# Function that looks through all the rows to make sure there are no 
# errors. If there are it tried to fix them
#######################################################################
def SanitizeDataRows(dataRows, year, month):
                          
    iRow = 0
    while iRow < len(dataRows)-1:
        curRow = dataRows[iRow]
        nextRow = dataRows[iRow+1]
        
        # check that the nextRow starts with a datestamp if not the data is corrupted and we need to merge the rows
        nextRowTokenized = nextRow.split(',')
       
        filtered = fnmatch.filter(nextRowTokenized[:2], dateStampWildcard)
       
        if len(filtered) == 0:
            dataRows[iRow] = curRow+nextRow
            dataRows.remove(nextRow)
            iRow -= 2         
        
        iRow += 1

    # remove any empty rows
    for row in dataRows:
        if row.isspace():
            dataRows.remove(row)

    return dataRows

########################################################################
# Function that looks through row to make sure it contains only 5 elements
# if there are more than 5 there were commas in the title
#######################################################################
def SanitizeRow(row):
    cleanedRow = []

    nElements = len(row)

    if not nElements == 5:
        # merge elements together
        row[3 : nElements-1] = [''.join(row[3 : nElements-1])]

    cleanedRow = row

    return cleanedRow

########################################################################
# Function that 
#######################################################################

def GetDataFrame(year, month, filename, debugFlag = False):
    
    # Open the file for reading and store it as one big string
    inputFileLocation = dataLocationBase + year + '/' + month + '/CSV/' + filename   
    inputFile = open(inputFileLocation,'r')
    
    dataRows = inputFile.readlines()

    dataRows = SanitizeDataRows(dataRows,year,month)

    # break up the lines into tokens seperated by commas and store in a list of lists
    dataFrame = []
    for row in dataRows:
        tokenizedRow = row.split(',')
        cleanedRow = SanitizeRow(tokenizedRow)
        dataFrame.append(cleanedRow)

    # Add the uniqueID based on the hash of the title to the end of each row in the dataFrame
    for row in dataFrame:
        uniqueID = hashlib.md5(row[3].encode('utf-8')).hexdigest()
        row.append(uniqueID)

    # Add the base URL to the end of each row in the dataFrame 
    for row in dataFrame:
        splitURL = urlsplit(row[1])
        row.append(splitURL.netloc)

    if debugFlag:
        for row in dataFrame:
            DisplayRow(row)
            if not len(row) == 6:
                input()

        print('DONE-SKI')
        input()
   
    return dataFrame

#################################################################################################################################
# Test code starts here
#################################################################################################################################
"""
listOfYearDirs = listdir_nohidden(dataLocationBase)

for year in listOfYearDirs:
    listOfMonthDirs = listdir_nohidden(dataLocationBase+year)

    for month in listOfMonthDirs:

        currentDirectory = dataLocationBase+year+'/'+month+'/CSV/'

        listOfFiles = listdir_nohidden(currentDirectory)

        for filename in listOfFiles:

            currentDataFrame = GetDataFrame(year, month, filename)

            for row in currentDataFrame:
                DisplayRow(row)
            input()
"""
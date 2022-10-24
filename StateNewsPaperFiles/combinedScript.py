import os

usnplDir = './fromUSNPL/'
combinedDir = './Combined/'
outputDir = "./Final/"

#######################################################################
# Function that returns a list of all none hidden objects in directory
#######################################################################

def listdir_nohidden(directory):
    listOfContents = os.listdir(directory)

    for item in listOfContents:
        if item.startswith('.'):
            listOfContents.remove(item)

    return listOfContents

#######################################################################
# Function that read a two column csv file and returns a list of pairs
#######################################################################
def GetListOfPairs(filename):
    inputFile = open(filename, 'r')
    
    linesInFile = inputFile.readlines()

    listOfPairs = []

    for line in linesInFile:
        pair = line.split(',')

        if len(pair) == 2:
            listOfPairs.append(pair)
        else:
            print("ERROR: not a pair")
            print(pair)
            input()

    return listOfPairs

#######################################################################
# Main code starst here
#######################################################################

usnplFileList = listdir_nohidden(usnplDir)
combinedFileList = listdir_nohidden(combinedDir)

for filename in combinedFileList:
    print(filename,end='')

    combinedList = []

    if not filename in usnplFileList:
        print('FILENAME NOT FOUND: ' , filename)
        input()
    else:
        source1List = GetListOfPairs(usnplDir+filename)
        source2List = GetListOfPairs(combinedDir+filename)

        print(' ',len(source2List),end='')

        for pair1 in source1List:
            
            found = False
            for pair2 in source2List:
                if pair1[0] == pair2[0]:    
                    found = True
                    break
            
            if not found:
                source2List.append(pair1)
    
    outputFile = open(outputDir+filename,'w')
    for pair in source2List:
        outputFile.write(pair[0]+','+pair[1])
    outputFile.close()
    
    print(' ',len(source2List))

    
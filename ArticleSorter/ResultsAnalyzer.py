from Util import *

############################################################

def GetURLList(filename):
    
    listOfURLs = []
    
    inputFile = open(statePaperFilesLocation + filename)
    lines = inputFile.readlines()

    for line in lines:
        pair = line.split(',')
        
        if len(pair) == 2:
            url = pair[1]
            if not url.strip() == 'MISSING':
                listOfURLs.append(url.strip())                      
        else:
            print("ERROR: ", filename)
            print(pair)
            input()
            
    inputFile.close()
    
    return listOfURLs

############################################################

statePaperFiles = os.listdir(statePaperFilesLocation)

listOfLists = []
listOfStates = []
listOfDuplicates = []

for filename in statePaperFiles:
    list = GetURLList(filename)
    listOfStates.append(filename)
    listOfLists.append(list)
    
nList = len(listOfLists)
iCounter = 0

while iCounter < nList:
    targetList = listOfLists[iCounter]
    
    for targetItem in targetList:
        jCounter = iCounter+1
        while jCounter < nList:
            curList = listOfLists[jCounter]
            
            for curItem in curList:
                if targetItem == curItem:
                    print(targetItem,'\tFound in both: ', listOfStates[iCounter],'\t',listOfStates[jCounter])
                
                    if targetItem not in listOfDuplicates:
                        listOfDuplicates.append(targetItem)
            
            jCounter +=1    
    
    iCounter += 1

print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
for targetItem in listOfDuplicates:
    print(targetItem)
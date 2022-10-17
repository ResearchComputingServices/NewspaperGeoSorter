from Util import *

statePaperFiles = os.listdir(statePaperFilesLocation)

print('State,Total #, # Found,# Not Found')
for filename in statePaperFiles:
    inputFile = open(statePaperFilesLocation + filename)
    lines = inputFile.readlines()

    urlNotFound = 0
    urlFound = 0
    totalNumberPapers = len(lines)
    for line in lines:
        pair = line.split(',')

        if len(pair) == 2:
            if pair[1].strip() in ignoreList:
                urlNotFound += 1
            else:
                urlFound += 1
        else:
            print("ERROR: ", filename)
            print(pair)
            input()

    print(filename.split('.')[0], ',', totalNumberPapers, ',', urlFound, ',', urlNotFound)



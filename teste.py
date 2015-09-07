from app import *
from operator import itemgetter
content= """
    @import url(../../lib/font/league-gothic/league-gothic.css);
    @import url(https://fonts.googleapis.com/css?family=Lato:400,700,400italic,700italic);
    /**
     * League theme for reveal.js.
     *
     * This was the default theme pre-3.0.0.
     *
     * Copyright (C) 2011-2012 Hakim El Hattab, http://hakim.se
     */
    /*********************************************
     * GLOBAL STYLES
     *********************************************/
    body {
      background: #1c1e20;
      background: -moz-radial-gradient(center, circle cover, #555a5f 0%, #1c1e20 100%);
      background: -webkit-gradient(radial, center center, 0px, center center, 100%, color-stop(0%, #555a5f), color-stop(100%, #1c1e20));
      background: -webkit-radial-gradient(center, circle cover, #555a5f 0%, #1c1e20 100%);
      background: -o-radial-gradient(center, circle cover, #555a5f 0%, #1c1e20 100%);
      background: -ms-radial-gradient(center, circle cover, #555a5f 0%, #1c1e20 100%);
      background: radial-gradient(center, circle cover, #555a5f 0%, #1c1e20 100%);
      background-color: #2b2b2b; }

    .reveal {
      font-family: 'Lato', sans-serif;
      font-size: 36px;
      font-weight: normal;
      color: #eee; }

    ::selection {
      color: #fff;
      background: #FF5E99;
      text-shadow: none; }

    .reveal .slides > section, .reveal .slides > section > section {
      line-height: 1.3;
      font-weight: inherit; }

    /*********************************************
     * HEADERS
     *********************************************/

    """

def getSpaceList(row):
    counter = 0
    spaceMap = []
    for char in row:
        if char == ' ':
            spaceMap.append(True)
        else:
            spaceMap.append(False)
        counter += 1
    return spaceMap

def getRangeCutLine(row, charLimit):
    numChar = len(row)
    limiter = range(0, numChar, charLimit)
    if limiter[-1] != numChar:
        limiter.append(numChar)
    return limiter

def calcCutRow(row, spaceRange,spaceList,margin):
    delimiterList = []
    counter = 0
    rag = range(len(spaceRange)-1) 
    for i in rag:
        start = spaceRange[i]
        end = spaceRange[i+1]
        for sl in spaceList[start:end]:
            if sl == True and counter in (getMargin(start, margin) +  getMargin(end, margin)):
                delimiterList.append(counter)
            counter += 1
    return delimiterList


def calcBetterPosition(problablyPositions, spaceRange,rowSize):
    del spaceRange[0]
    del spaceRange[-1]
    distanceList = {}
    result = []
    result.append(0)
    counter = 0
    for r in spaceRange:
        for i in problablyPositions:
            calc = i-r
            if(calc < 0 ):
                calc = calc*-1
            distanceList[calc] = i
        #    print(r,i,calc)
        #print('----')
        betterPosition = distanceList[sorted(distanceList.keys())[0]]
        #print(betterPosition)
        if betterPosition in range(r-5,r+5):
            result.append(betterPosition)
        else:
            result.append(r)

        distanceList = {}
    result.append(rowSize)
    return result

def sliceRowByLimiter(row, limiter):
    times = len(limiter) -1
    result = []
    for t in range(times):
        result.append(row[limiter[t]:limiter[t+1]])
    return result
def getMargin(pointer, margin):
    return (range((pointer - margin),(pointer + margin + 1),1))



content = """@im port url(../../lib/font/league-gothic/league-gothic.css);
@i mport url(https://fonts.googleapis.com/css?family=Lato:400,700,400italic,700italic);
'. reveal .slides > section, .reveal .slides > section > sectionsdfsdreveals l i d sssectionsectionasdreveal .slides > section, .reveal .slides > sectionsecti onr evea lslidess > section > section {"""

def redimensionContent(rows,lineSize):
    newRows = []
    for row in rows:
        spaceList = getSpaceList(row)
        spaceRange = getRangeCutLine(row, lineSize)
        problablyPositions = calcCutRow(row,spaceRange,spaceList,5)
        finalRange = calcBetterPosition(problablyPositions, spaceRange,len(row))
        result = sliceRowByLimiter(row,finalRange)
        newRows.extend(result)
    return newRows

print(redimensionContent(content.splitlines(), 80))

#spaceList = getSpaceList(row)
#spaceRange = getRangeCutLine(row, 80)
#problablyPositions = calcCutRow(row,spaceRange,spaceList,5)
#finalRange = calcBetterPosition(problablyPositions, spaceRange,len(row))
#result = sliceRowByLimiter(row,finalRange)
#print(finalRange)

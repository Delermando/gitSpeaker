import sys
class Content(object):

    def rows(self, content, rowsNumber, charLimit):
        rows = content.splitlines()
        #rows =self.redimensionContent(content.splitlines(), charLimit)
        contentRowsNumber = len(rows)

        contentRange = self.createCutMap(rows,rowsNumber, contentRowsNumber)
        return self.groupRows(rows, contentRange, rowsNumber)

    def createCutMap(self, rows, rowsNumber, contentRowsNumber):
        deliterList = []
        contentRange = self.getSlideRange(rowsNumber, contentRowsNumber)
        breakList = self.getBreakContent(rows)
        deliterList = self.calcCutContentD(rowsNumber, contentRange, breakList, 2)

        if len(deliterList) != 0:
            deliterList[0] = 0
            deliterList.append(contentRowsNumber)
            return deliterList
        else:
            return (0,contentRowsNumber)

    def redimensionContent(self,rows,lineSize):
        newRows = []
        result = []
        for row in rows:
            spaceList = self.getSpaceList(row)
            spaceRange = self.getRangeCutLine(row, lineSize)
            problablyPositions = self.calcCutRow(row,spaceRange,spaceList,5)
            if len(spaceRange) != 0:
                finalRange = self.calcBetterPosition(problablyPositions, spaceRange,len(row))
                result = self.sliceRowByLimiter(row,finalRange)
                #print(result)
            newRows = newRows + result
        return newRows


    def sliceRowByLimiter(self, row, limiter):
        times = len(limiter) -1
        result = []
        for t in range(times):
            result.append(row[limiter[t]:limiter[t+1]])
        return result

    def calcBetterPosition(self, problablyPositions, spaceRange,rowSize):
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

    def calcCutRow(self,row, spaceRange,spaceList,margin):
        delimiterList = []
        counter = 0
        rag = range(len(spaceRange)-1) 
        for i in rag:
            start = spaceRange[i]
            end = spaceRange[i+1]
            for sl in spaceList[start:end]:
                if sl == True and counter in (self.getMargin(start, margin) +  self.getMargin(end, margin)):
                    delimiterList.append(counter)
                counter += 1
        return delimiterList


    def getRangeCutLine(self,row, charLimit):
        numChar = len(row)
        limiter = range(0, numChar, charLimit)
        if len(limiter) != 0:
            if limiter[-1] != numChar:
                limiter.append(numChar)
        return limiter

    def getSpaceList(self,row):
        counter = 0
        spaceMap = []
        for char in row:
            if char == ' ':
                spaceMap.append(True)
            else:
                spaceMap.append(False)
            counter += 1
        return spaceMap


    def calcCutContentD(self, rowsNumber, contentRange, breakList, margin):
        delimiterList = []
        counter = 0
        for start in contentRange:
            end = start + rowsNumber

            for bl in breakList[start:end]:
                if bl == True and counter in (self.getMargin(start, margin) +  self.getMargin(end, margin)):
                    delimiterList.append(counter)
                counter += 1
        return delimiterList

    def getMargin(self, pointer, margin):
        return (range((pointer - margin),(pointer + margin + 1),1))

    def getSlideRange(self, rowsNumber, contentRowsNumber):
        if rowsNumber <= contentRowsNumber:
            return range(0, contentRowsNumber, int(rowsNumber))
        else:
            return [0]

    def getBreakContent(self,rows):
        counter = 0
        breakMap = []
        for row in rows:
            if row == '' or (len(row) == row.count(' ')):
                breakMap.append(True)
            else:
                breakMap.append(False)

            counter += 1
        return breakMap



    def groupRows(self, rows, contentRange, rowsNumber):
        groups = []
        group = ''
        times = len(contentRange) - 1
        for t in range(times):
            for r in range(contentRange[t],contentRange[t+1],1):
                group += rows[r] + '\n'
            groups.append(group)
            group = ''
        return groups


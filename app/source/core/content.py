class Content(object):

    def rowsMdFiles(self, rows, rowsNumber, contentRowsNumber):    
        contentRange = self.getSlideRange(rowsNumber, contentRowsNumber)
        contentRange.append(contentRowsNumber)
        listContent = self.groupRows(rows, contentRange)        
        listContent = self.setUncloseMark('```','```', listContent)
        #listContent = self.setUncloseMark("/*---","---*/", listContent)
        #listContent = self.closeBacktick('```','```js\n ','```', listContent)
        return listContent

    def setUncloseMark(self,markBegin, markEnd, listContent):
        result = []
        counter = 0

        for content in listContent:
            for ct in content.splitlines():
                    ct = ct.replace(" ","")
                    if "```" in ct and len(ct) >= 4:
                        mark = ct+"\n"


            if content.count(markBegin) == 0:
                result.append(content)
            elif content.count(markBegin) % 2 == 0:
                for ct in content.splitlines():
                    ct = ct.replace(" ","")
                    if "```" in ct:
                        if len(ct) >= 4:
                            result.append(content)
                        else:
                            result.append(mark+content+markEnd)
                        break
            else:
                for ct in content.splitlines():
                    ct = ct.replace(" ","")
                    if "```" in ct:
                        if len(ct) >= 4:
                            result.append(content+markEnd)
                        else:
                            result.append(mark+content)
                        break
            a = []
            for r in result:
                 a.append(r.replace("```bash\n```", ""))
        return a;

    def closeBacktick(self,markSearch, markBegin, markEnd, listContent):
        result = []
        counter = 0
        for content in listContent:
            if content.count(markSearch) == 1:
                result.append(content + markEnd)
                listContent[counter] = markBegin + listContent[counter + 1]
            else:
                result.append(content)
            counter += 1
        return result


    def rowsCodeFiles(self, rows, rowsNumber, contentRowsNumber):
        contentRange = self.getSlideRange(rowsNumber, contentRowsNumber)
        breakList = self.getBreakContentList(rows)
        problablyPositions = self.calcCutDelimiter(rowsNumber, contentRange, breakList, 2)
        deliterList = self.calcBetterPosition(problablyPositions, contentRange, contentRowsNumber)

        if len(deliterList) != 0:
            deliterList[0] = 0
            deliterList.append(contentRowsNumber)
        else:
            deliterList.append(0)
            deliterList.append(contentRowsNumber)
        return self.groupRows(rows, deliterList)

    def calcBetterPosition(self, problablyPositions, contentRange,contentSize):
        del contentRange[0]
        distanceList = {}
        result = []
        result.append(0)
        counter = 0
        for r in contentRange:
            for i in problablyPositions:
                calc = i-r
                if(calc < 0 ):
                    calc = calc*-1
                distanceList[calc] = i
            if len(distanceList.keys()) > 1:
                betterPosition = distanceList[sorted(distanceList.keys())[0]]
            else:
                betterPosition = 0
                
            if betterPosition in range(r-2,r+2):
                result.append(betterPosition)
            else:
                result.append(r)

            distanceList = {}
        result.append(contentSize)
        return result

    def calcCutDelimiter(self, rowsNumber, contentRange, breakList, margin):
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
            return range(0, contentRowsNumber, rowsNumber)
        else:
            return [0]

    def getBreakContentList(self,rows):
        counter = 0
        breakMap = []
        for row in rows:
            if row == '' or (len(row) == row.count(' ')):
                breakMap.append(True)
            else:
                breakMap.append(False)

            counter += 1
        return breakMap

    def groupRows(self, rows, contentRange):
        groups = []
        group = ''
        times = len(contentRange) - 1
        for t in range(times):
            for r in range(contentRange[t],contentRange[t+1],1):
                group += rows[r] + '\n'
            groups.append(group)
            group = ''
        return groups
    

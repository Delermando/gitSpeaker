class Content(object):

    def rows(self, rows, rowsNumber, contentRowsNumber):
        contentRange = self.createCutMap(rows,rowsNumber, contentRowsNumber)
        return self.groupRows(rows, contentRange, rowsNumber)
    
    def createCutMap(self, rows, rowsNumber, contentRowsNumber):
        contentRange = self.getSlideRange(rowsNumber, contentRowsNumber)
        breakList = self.getBreakContentList(rows)
        deliterList = self.calcCutDelimiter(rowsNumber, contentRange, breakList, 2)
        if len(deliterList) != 0:
            deliterList[0] = 0
            deliterList.append(contentRowsNumber)
        else:
            deliterList.append(0)
            deliterList.append(contentRowsNumber)
        print(deliterList)
        return deliterList


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
            return range(0, contentRowsNumber, int(rowsNumber))
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


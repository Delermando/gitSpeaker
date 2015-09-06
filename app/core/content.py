class Content(object):

    def rows(self, rows, rowsNumber, contentRowsNumber):
        contentRange = self.getSlideRange(rowsNumber, contentRowsNumber)
        return self.groupRows(rows, contentRange, rowsNumber)
    
    def getSlideRange(self, rowsNumber, contentRowsNumber):
        
        if contentRowsNumber <= rowsNumber:
            return range(0, contentRowsNumber, int(rowsNumber))
        else:
            return [0]

    def groupRows(self, rows, contentRange, rowsNumber):
        groups = []
        group = ''
        for times in contentRange:
            for row in rows[ times : times + int(rowsNumber)]:
                group += row + '\n'
            groups.append(group)
            group = ''
        
        return groups


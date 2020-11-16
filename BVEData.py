


class BVEData():

    def __init__( self ):
        self.x = 0
        self.y = 0

        self.dictBoxes = {}
        pass

    def setShape( self, x, y ):
        self.x = x
        self.y = y

    def setBoxes( self, dictBoxes ):
        self.dictBoxes = dictBoxes

    def checkBoxes( self, x, y ):
        dictResult = {}

        listKeys = self.dictBoxes.keys()
        for strKey in listKeys:
            for tupData in self.dictBoxes[ strKey ]:
                bx, by, bw, bh = tupData

                if x < bx or x > bx + bw:
                    continue
                if y < by or y > by + bh:
                    continue
                if strKey not in dictResult:
                    dictResult[ strKey ] = []
                dictResult[strKey].append( tupData )

        return dictResult




    def printBoxes( self ):
        print( self.dictBoxes )


    # 출력용
    def __str__( self ):
        return "x : {}, y : {}".format( self.x, self.y )
from Yolo import Yolo
from Tracker import Tracker
from HVoice import H_Voice as hv 


class BVEData():

    dictKeyCreator = {
        ord('y') : Yolo,
        ord('t') : Tracker
    }

    def __init__( self ):
        self.endFlag = False
        self.stopFlag = False

        self.x = 0
        self.y = 0

        self.L_TH = 0
        self.H_TH = 0

        self.objYolo = None
        self.objTracker = None

        self.dictBoxes = {}
        self.dictActionFlag = {}
        self.dictFnLists = {}

        self.objHV = hv()

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

    def changeStatus( self, dictData ):
        self.stopFlag = not self.stopFlag

    def setEndFlag( self, dictData):
        self.endFlag = True

    def reinitialize( self, dictData):
        self.endFlag = False
        self.stopFlag = False

        self.x = 0
        self.y = 0

        self.L_TH = 0
        self.H_TH = 0

        self.objYolo = None
        self.objTracker = None

        self.dictBoxes = {}
        self.dictActionFlag = {}
        self.dictFnLists = {}

    def setTrackbarData( self, dictData):
        pass

    def setAction( self, dictData ):

        img = self.ImgData
        nKey = dictData["key"]

        fnCreator = BVEData.getKeyValue( nKey )

        if nKey not in self.dictFnLists:
            self.dictFnLists[ nKey ] = {}
            self.dictFnLists[ nKey ]["status"] = False
        self.dictFnLists[ nKey ]["status"] = not self.dictFnLists[ nKey ]["status"]

        if self.dictFnLists[ nKey ]["status"] == True:
            self.dictFnLists[ nKey ][ "object" ] = fnCreator( img )
            self.dictFnLists[ nKey ][ "actor" ] = self.dictFnLists[ nKey ][ "object" ].do
        else:
            del( self.dictFnLists[ nKey ] )

    def doAction( self ):
        image = self.ImgData
        for nKey in self.dictFnLists:
            EditedImg = self.dictFnLists[ nKey ][ "actor" ]( image )
            image = EditedImg

        return image 

    def setImage( self, frame ):
        self.ImgData = frame.copy()

    @classmethod
    def getKeyValue( cls, strKey ):
        return cls.dictKeyCreator[ strKey ]

    def run_voicemode( self ):
        self.objHV.listen_background()

    def stop_voicemode( self ):
        self.objHV.stop_listen_background()

    def getVoiceData( self ):
        return self.objHV.getMsg()

        



    def printBoxes( self ):
        print( self.dictBoxes )


    # 출력용
    def __str__( self ):
        return "x : {}, y : {}".format( self.x, self.y )
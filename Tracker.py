import numpy as np
import cv2

class Tracker():

    dictCVObjTrackers = {
        "csrt" : cv2.TrackerCSRT_create,
        "kcf" : cv2.TrackerKCF_create,
        "boosting" : cv2.TrackerBoosting_create,
        "mil" : cv2.TrackerMIL_create,
        "tld" : cv2.TrackerTLD_create,
        "medianflow" : cv2.TrackerMedianFlow_create,
        "mosse" : cv2.TrackerMOSSE_create
    }


    def __init__( self, img, strTrackerName = "csrt" ):

        self.box = tuple()
        self.Left = 0
        self.Right = 0
        self.Top = 0
        self.Bottom = 0

        self.listTtoB = []
        self.listLtoR = []

        self.imgData = img.copy()

        result = Tracker.checkTracker( strTrackerName )
        if result == False:
            print( "not exist " + strTrackerName + " Tracker!!")
            exit(0)
        self.strTrackerName = strTrackerName

        self.objTracker = Tracker.createTracker( strTrackerName )

        rect = self.selectROI()
        self.objTracker.init( self.imgData, rect )

    @classmethod
    def checkTracker( cls, strTrackerName ):
        return strTrackerName in cls.dictCVObjTrackers
    @classmethod
    def createTracker( cls, strTrackerName ):
        return cls.dictCVObjTrackers[ strTrackerName ]()

    def selectROI( self ):
        # rect = cv2.selectROI( "Selected Window", self.imgData, fromCenter=False, showCrosshair=True )
        rect = cv2.selectROI( "video", self.imgData, fromCenter=False, showCrosshair=True )
        # cv2.destroyWindow("Selected Window")
        return rect

    def setImage( self, img ):
        self.imgData = img.copy()

    def do( self, img ):

        self.setImage( img )
        
        res, self.box = self.objTracker.update( self.imgData )
        self.Left, self.Top, w, h = [ int(value) for value in self.box ]
        self.Right = self.Left + w
        self.Bottom = self.Top + h

        self.listTtoB.append( np.array( [ self.Top, self.Bottom ] ) )
        self.listLtoR.append( np.array( [ self.Left, self.Right ] ) )

        if len( self.listTtoB ) > 10 :
            del self.listTtoB[0]
            del self.listLtoR[0]

        self.point1 = ( int( self.Left ) , int( self.Top ) )
        self.point2 = ( int( self.Right ), int( self.Bottom ) )
        cv2.rectangle( self.imgData, self.point1, self.point2, ( 255, 255, 255 ), 2 )

        return self.imgData

    @classmethod
    def cropRange( cls, img, listTtoB, listLtoR ):

        fit_to = "height"
        output_size = ( 320, 320 )

        # compute moving average
        avg_height_range = np.mean( listTtoB, axis=0 ).astype( np.int )
        avg_width_range = np.mean( listLtoR, axis=0 ).astype( np.int )
        avg_center = np.array( [ np.mean( avg_width_range ), np.mean( avg_height_range ) ] )

        # compute scaled width and height
        scale = 1.3
        avg_height = ( avg_height_range[1] - avg_height_range[0] ) * scale
        avg_width = ( avg_width_range[1] - avg_width_range[0] ) * scale

        # compute new scaled ROI
        avg_height_range = np.array([avg_center[1] - avg_height / 2, avg_center[1] + avg_height / 2])
        avg_width_range = np.array([avg_center[0] - avg_width / 2, avg_center[0] + avg_width / 2])

        # fit to output aspect ratio
        if fit_to == 'width':
            avg_height_range = np.array([
            avg_center[1] - avg_width * output_size[1] / output_size[0] / 2,
            avg_center[1] + avg_width * output_size[1] / output_size[0] / 2
            ]).astype(np.int).clip(0, 9999)

            avg_width_range = avg_width_range.astype(np.int).clip(0, 9999)
        elif fit_to == 'height':
            avg_height_range = avg_height_range.astype(np.int).clip(0, 9999)

            avg_width_range = np.array([
            avg_center[0] - avg_height * output_size[0] / output_size[1] / 2,
            avg_center[0] + avg_height * output_size[0] / output_size[1] / 2
            ]).astype(np.int).clip(0, 9999)

        # crop image
        result_img = img[avg_height_range[0]:avg_height_range[1], avg_width_range[0]:avg_width_range[1]].copy()

        # resize image to output size
        result_img = cv2.resize(result_img, output_size)





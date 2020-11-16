import cv2
import os
import sys
import numpy as np

class Yolo():

    strWeightPath = "yolo_v3/yolov3.weights"
    strConfigPath = "yolo_v3/yolov3.cfg"
    strLabelPath = "yolo_v3/coco.names"
    dThreshold = 0.5
    dNMSThreshold = 0.4

    net = None
    listClasses = []
    npColors = None
    layer_names = None
    OutputLayers = None


    def __init__( self, img ):

        if img is None:
            print( 'No ImageData' )
            exit()
        self.imgData = img

        result = Yolo.readNetFile()
        result = Yolo.readClassNames()
        result = Yolo.getOutputLayer()

    @classmethod
    def readNetFile( cls ):
        cls.net = cv2.dnn.readNet( cls.strWeightPath, cls.strConfigPath )
        if cls.net.empty():
            print( "Net Open Failed. plz check weight & config File")
            return False

    @classmethod
    def readClassNames( cls ):
        with open( cls.strLabelPath, "rt" ) as LabelFile:
            cls.listClasses = LabelFile.read().rstrip('\n').split('\n')

        cls.npColors = np.random.uniform( 0, 255, size=( len( cls.listClasses ), 3 ))

    @classmethod
    def getOutputLayer( cls ):
        cls.layer_names = cls.net.getLayerNames()
        cls.OutputLayers = [ cls.layer_names[i[0] - 1] for i in cls.net.getUnconnectedOutLayers() ]

    def doYolo( self ):
        img = self.imgData

        img, dictBoxes = Yolo.initializeSetting( img )

        return dictBoxes
        
        
    @classmethod
    def initializeSetting( cls, img ):
        dictBoxes = {}
        blob = cv2.dnn.blobFromImage( img, 1/255., (320, 320), swapRB=True )
        print( blob )
        cls.net.setInput( blob )
        outs = cls.net.forward( cls.OutputLayers )

        h, w = img.shape[:2]

        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            # print( out )
            for detection in out:
                # detection: 4(bounding box) + 1(objectness_score) + 80(class confidence)
                # print( detection )
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > cls.dThreshold:
                    # 바운딩 박스 중심 좌표 & 박스 크기
                    cx = int(detection[0] * w)
                    cy = int(detection[1] * h)
                    bw = int(detection[2] * w)
                    bh = int(detection[3] * h)
                    MyData = ( cx, cy, bw, bh )
                    print( MyData )

                    # 바운딩 박스 좌상단 좌표
                    sx = int(cx - bw / 2)
                    sy = int(cy - bh / 2)

                    boxes.append([sx, sy, bw, bh])
                    confidences.append(float(confidence))
                    class_ids.append(int(class_id))

        # 비최대 억제
        indices = cv2.dnn.NMSBoxes(boxes, confidences, cls.dThreshold, cls.dNMSThreshold)

        for i in indices:
            i = i[0]
            sx, sy, bw, bh = boxes[i]
            label = f'{cls.listClasses[class_ids[i]]}: {confidences[i]:.2}'
            color = cls.npColors[class_ids[i]]
            cv2.rectangle(img, (sx, sy, bw, bh), color, 2)
            cv2.putText(img, label, (sx, sy - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2, cv2.LINE_AA)
            if cls.listClasses[ class_ids[i]] not in dictBoxes:
                dictBoxes[ cls.listClasses[class_ids[i]]] = []
            dictBoxes[ cls.listClasses[class_ids[i]]].append(( sx, sy, bw, bh ))

        # t, _ = cls.net.getPerfProfile()
        # label = 'Inference time: %.2f ms' % (t * 1000.0 / cv2.getTickFrequency())
        # cv2.putText(img, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
        #                 0.7, (0, 0, 255), 1, cv2.LINE_AA)

        return img, dictBoxes

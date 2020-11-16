import cv2
import os
import numpy as np
import sys
from BVEData import BVEData
from Yolo import Yolo

def onMouse( event, x, y, flags, param ):
    if event == cv2.EVENT_LBUTTONDOWN:
        param[1].setShape( x, y )
        dictResult = param[1].checkBoxes(x, y)
        print( dictResult )
    else:
        pass

def notting(pos): # 트랙바 핸들러
    pass
def player( filePath ):
    frameRate = 20
    swich = 0
    # 데이터 저장 객체 생성
    objData = BVEData()
    objYolo = None


    image = None
    flag = 0 #정지 상태
    L_TH = 0 #트랙바 low
    H_TH = 0 #트랙바 high


    cv2.namedWindow('video') # 창 생성
    cap = cv2.VideoCapture( filePath )
    #print(cap.get(cv2.CAP_PROP_FPS)) 프레임레이트확인 : 20

    # 트랙바 생성
    cv2.createTrackbar('Low_TH', 'video', 0, 255, notting) # video에는 트랙바를 생성 할 창이름을 적어주세요
    cv2.createTrackbar('High_TH', 'video', 0, 255, notting) # video에는 트랙바를 생성 할 창이름을 적어주세요


    while 1: # 비디오재생
        if flag == 1:# push - space bar
            frame = image
        else:
            ret, frame = cap.read()
            if not ret:# while문을 빠져나오기 위한 조건문
                break
        cv2.imshow('video',frame)
        # 63 52
        # target bar의 위치값을 받음
        Low_TH = cv2.getTrackbarPos('Low_TH', 'video')
        High_TH = cv2.getTrackbarPos('High_TH', 'video')

        # 마우스 Event에 대한 Callback 설정
        cv2.setMouseCallback( "video", onMouse, [ frame, objData ])
        # print( objData )

        if objYolo is not None:
            dictTmp = objYolo.doYolo()
            objYolo = None

            objData.setBoxes( dictTmp )
            objData.printBoxes()

        key = cv2.waitKey(33)
        if key == 32: # space
            flag = not flag
            image = frame
        elif key == 112 :# p
            L_TH = Low_TH
            H_TH = High_TH
            print(L_TH, H_TH)
        elif key == 114: # r
            objData = BVEData()
        elif key == 121: # y
            flag = not flag
            image = frame
            objYolo = Yolo( frame )
        elif key == 113: # q
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":#동영상 파일 경로

    if len( sys.argv ) <= 1 :
        strUsage = "편집할 동영상 파일을 인자로 넘겨 주세요!\nUsage : python [파일 이름].py [동영상 파일 path]"
        print( strUsage )
        exit()

    strFilePath = sys.argv[1]
    player( strFilePath )

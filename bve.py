import cv2
import os
import numpy as np
import sys
from BVEData import BVEData


def onMouse( event, x, y, flags, param ):
    if event == cv2.EVENT_LBUTTONDOWN:
        param[1].setShape( x, y )
        dictResult = param[1].checkBoxes(x, y)
        print( dictResult )
        # print( "hanelso")
    else:
        pass

def mappingMSG( msg ):

    result = -1

    dictMsgKey = {
        "tracking" : ord('t'),
        "YOLO" : ord('y'),
        "stop" : ord(" "),
        "start" : ord(" "),
        "reset" : ord('r'),
        "break" : ord('q'),
        "" : -1
    }

    if msg in dictMsgKey.keys():
        result = dictMsgKey[msg]

    return result

def checkActionFlagKey( key, playerData ):

    dictData = {}

    dictKeyAct = {
        ord(' ') : playerData.changeStatus,
        ord('q') : playerData.setEndFlag,
        ord('r') : playerData.reinitialize,
        ord('t') : playerData.setAction,
        ord('y') : playerData.setAction,
        ord('p') : playerData.setTrackbarData
    }

    if key == ord(' '):
        pass
    elif key == ord( 'p' ):
        pass
    elif key == ord('r'):
        pass
    elif key == ord('y'):
        dictData[ "key" ] = key
    elif key == ord('t'):
        dictData[ "key" ] = key
    elif key == ord('q'):
        pass

    if key in dictKeyAct:
        dictKeyAct[ key ]( dictData )
    

def notting(pos): # 트랙바 핸들러
    pass
def player( filePath ):
    frameRate = 20
    swich = 0
    # 데이터 저장 객체 생성
    playerData = BVEData()

    playerData.run_voicemode()

    frame = None
    image = None
    EditedImg = None
    dictActionFlag = {}
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
        if playerData.stopFlag == True:# push - space bar
            pass
        else:
            ret, frame = cap.read()
            if not ret:# while문을 빠져나오기 위한 조건문
                break
        playerData.setImage( frame )

        # 63 52
        # target bar의 위치값을 받음
        Low_TH = cv2.getTrackbarPos('Low_TH', 'video')
        High_TH = cv2.getTrackbarPos('High_TH', 'video')

        # 마우스 Event에 대한 Callback 설정
        cv2.setMouseCallback( "video", onMouse, [ frame, playerData ])

        # 편집 기능( Yolo, Tracker )
        EditedImg = playerData.doAction()

        # image 출력
        # cv2.imshow('video2', frame)
        cv2.imshow('video', EditedImg )

        key = cv2.waitKey(33)
        msg = playerData.getVoiceData()
        if msg != "":
            print( msg )
        key = mappingMSG( msg )

        checkActionFlagKey( key, playerData)

        if playerData.endFlag == True:
            break

    playerData.stop_voicemode()


    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":#동영상 파일 경로

    if len( sys.argv ) <= 1 :
        strUsage = "편집할 동영상 파일을 인자로 넘겨 주세요!\nUsage : python [파일 이름].py [동영상 파일 path]"
        print( strUsage )
        exit()

    strFilePath = sys.argv[1]
    player( strFilePath )

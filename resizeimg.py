import cv2
import os

path = "./tuna_can"
print(path)
if os.path.isdir(path):
    list = os.listdir(path)
    for files in list:
        srcpath = os.path.join(path,files)

        # print(srcpath)
        if os.path.isfile(srcpath):
            print(srcpath)
            src = cv2.imread(srcpath, cv2.IMREAD_COLOR)
            w,h,_ = src.shape
            print(w,h)
            if ((w > 2000) and (h > 2000)):
                dst = cv2.resize(src, dsize=(720, 1024), interpolation=cv2.INTER_AREA)

                cv2.imwrite(srcpath, dst)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            elif ((w < 1000) or (h < 1000)):
                pass
            else :
                dst = cv2.resize(src, dsize=(h/2,w/2), interpolation=cv2.INTER_AREA)

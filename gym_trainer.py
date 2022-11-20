import cv2
import numpy as np
import mediapipe as mp
import time
import PoseModule as pm


cap = cv2.VideoCapture('squat.mp4')
detector = pm.poseDetector()
count = 0
dir = 0
pTime = 0

while True:
        success, img = cap.read()
        img = cv2.resize(img,(800,700))
        imgRGB = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
        imgRGB = detector.findPose(imgRGB)
        lmList = detector.findPosition(imgRGB,False)
        if len(lmList) != 0:
                angle = detector.findAngle(img, 24, 26, 28)
                per = np.interp(angle, (40, 160), (0, 100))
                # print(angle,per)
                bar = np.interp(angle, (50, 160), (650, 100))
                color = (255, 0, 255)
                if per == 100:
                        color = (0, 255, 0)
                        if dir == 0:
                                count += 0.5
                                dir = 1
                if per == 0:
                        color = (0, 255, 0)
                        if dir == 1:
                                count += 0.5
                                dir = 0
                # print(count)
                cv2.rectangle(img, (650, 100), (725, 700), (255,255,255), 3)
                cv2.rectangle(img, (650, int(bar)), (725, 700), (255,255,255), cv2.FILLED)
                cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255), 4)
 
     
                cv2.rectangle(img, (0, 450), (250, 720), (0, 0, 0), cv2.FILLED)
                cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15, (255, 255, 255), 25)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
        cv2.imshow("Image",img)
        cv2.waitKey(10)

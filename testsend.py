from communication import *
import cv2
import numpy as np
import time

com = Communication(myip='localhost', receiveport=8100, sendip ='localhost', sendport=8000)
com.start()


black = np.zeros((256, 256))
t1 = t2 = 0
while True:
    cv2.imshow('', black)
    k = cv2.waitKey(10)
    if k == ord('q'):
        break
    if k == ord('s'):
        com.custom_send('/start', 0)
        print('SENDING:', '/start 0')
        cv2.putText(black, 'Sending: /start 0', (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), thickness=1)
        t1 = time.time()
    if k == ord('p'):
        com.custom_send('/stop', 0)
        print('SENDING:', '/stop 0')
        cv2.putText(black, 'Sending: /stop 0', (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), thickness=1)
        t1 = time.time()

    t2 = time.time()

    if t2 - t1 >= 1 and t2-t1 < 1.5:
        black = np.zeros((256, 256))


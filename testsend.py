from communication import *
import cv2
import numpy as np

com = Communication(myip='localhost', receiveport=8100, sendip ='localhost', sendport=8000)
com.start()


black = np.zeros((256, 256))
while True:
    cv2.imshow('', black)
    k = cv2.waitKey(10)
    if k == ord('q'):
        break
    if k == ord('s'):
        com.send('/start', 0)
    if k == ord('p'):
        com.send('/stop', 0)





# com.send('BLABLA')
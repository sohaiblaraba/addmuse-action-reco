from communication import *
com = Communication(myip='192.168.0.110', receiveport=8000, sendip ='192.168.0.100', sendport=8100)
com.start()

com.send('BLABLA')
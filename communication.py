from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client
import asyncio

import threading


class Communication():
    def __init__(self, myip='192.168.0.110', receiveport=8000, sendip ='192.168.0.110', sendport=7000):
        self.myip = myip
        self.sendip = sendip
        self.receiveport = receiveport
        self.sendport = sendport
        self.dispatcher = dispatcher.Dispatcher()
        self.server = None
        self.client = None
        self.start_reco = False
        self.stop_reco = False
        self.list_of_people_to_analyze = []
        self.list_of_people_to_communicate = []

    def rstart(self, unused_addr, args):
        print('START RECEIVED', args)
        self.start_reco = True
        self.list_of_people_to_analyze.append(int(args))
        self.list_of_people_to_analyze = list(dict.fromkeys(self.list_of_people_to_analyze)) # remove duplicates
        return None

    def rstop(self, unused_addr, args):
        print('STOP RECEIVED', args)
        self.start_reco = False
        self.stop_reco = True
        self.list_of_people_to_communicate.append(int(args))
        self.list_of_people_to_communicate = list(dict.fromkeys(self.list_of_people_to_communicate)) # remove duplicates
        print(self.list_of_people_to_communicate)
        

        if int(args) in self.list_of_people_to_analyze:
            self.list_of_people_to_analyze.remove(int(args))


    def dispatch(self):
        self.dispatcher.map('/start', self.rstart)
        self.dispatcher.map('/stop', self.rstop)

    def threadedFunction(self, settings):
        print( "serving on {}".format(self.server.server_address) )
        self.server.serve_forever()  # this call blocks forever...


    def start(self):
        self.dispatch()
        self.server = osc_server.ThreadingOSCUDPServer((self.myip, self.receiveport), self.dispatcher)
        settings = {}
        t = threading.Thread(target=self.threadedFunction, args=([settings]) )
        t.daemon = True
        t.start()
        self.client = udp_client.SimpleUDPClient(self.sendip, self.sendport)

    def send(self, message):
        self.client.send_message('/reco', message)
        print('[SENT]', '/reco', message)
        



        
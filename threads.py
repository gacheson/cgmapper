#!/usr/bin/env python2.7

import threading

class Thread(threading.Thread):
    def __init__(self, threadID, name, instance):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.instance = instance
    def run(self):
        print "Starting " + self.name
        start_gpu(self.instance)
        print "Exiting " + self.name

def start_gpu(instance):
    instance.start()


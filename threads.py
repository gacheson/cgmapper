#!/usr/bin/env python2.7

import threading

class myThread (threading.Thread):
    def __init__(self, threadID, name, instance):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.instance = instance
        self.threadLock = threading.Lock()
    def run(self):
        print "Starting " + self.name
        self.threadLock.acquire()
        start_gpu(self.instance)
        print "Exiting " + self.name
        self.threadLock.release()

def start_gpu(instance):
    instance.start()


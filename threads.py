#!/usr/bin/env python2.7

import threading

class Thread(threading.Thread):
    def __init__(self, threadID, name, instance):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.instance = instance
    def run(self):
        if self.instance.verbose_print:
            print 'Starting {0}'.format(self.name)
        start_gpu(self.instance)
        if self.instance.verbose_print:
            print 'Exiting {0}'.format(self.name)

def start_gpu(instance):
    instance.start()


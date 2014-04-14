#!/usr/bin/env python2.7

import threading
import utilities as util

class Thread(threading.Thread):
    def __init__(self, threadID, name, instance):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.instance = instance
    def run(self):
        util.cprint_('Starting {0}'.format(self.name), self.instance.debug_print)
        start_gpu(self.instance)
        util.cprint_('Exiting {0}'.format(self.name), self.instance.debug_print)

def start_gpu(instance):
    instance.start()


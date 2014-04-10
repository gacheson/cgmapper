#!/usr/bin/env python2.7

from itertools import product
import api
import collections
import csv
import numpy as np
import os
import scipy as sp
import scipy.stats
import sys
import threading
import time

fstream = csv.FileStream()
sgminer = api.SGMiner()
threadLock = threading.Lock()

class Instance:
    def __init__(self, gpu_id, m_min, m_max, m_step, c_min, c_max, c_step, mhs_accuracy, cy_write):
        self.card = gpu_id
        self.mem_min = m_min
        self.mem_max = m_max
        self.mem_step = m_step
        self.core_min = c_min
        self.core_max = c_max
        self.core_step = c_step
        self.desired_accuracy_in_mhs = mhs_accuracy
        self.half_cycle_write = cy_write
        self.csv = 'mhs-%i.csv' % gpu_id
        self.skip = []
        self.d = collections.deque()

    def _mean_confidence(self, data, confidence=0.95):
        infinity = 1.0e24
        a = 1.0 * np.array(data)
        n = len(a)
        if n == 0:
            print "not enough data"
            return infinity
        m, se = np.mean(a), scipy.stats.sem(a)
        h = se * sp.stats.t._ppf((1+confidence)/2., n-1)
        print "h: " + str(h)
        return h

    def cycle_thru_clocks(self):
        core_ramp = 1
        for mem in xrange(self.mem_min, self.mem_max+1, self.mem_step):
            if core_ramp == 1:
                for core in xrange(self.core_min, self.core_max+1, self.core_step):
                    core_ramp = self.set_clocks(mem, core, 1)
                if self.half_cycle_write:
                    fstream.write_to_file(self.csv, self.d)
            elif core_ramp == -1:
                for core in xrange(self.core_max, self.core_min-1, -self.core_step):
                    core_ramp = self.set_clocks(mem, core, -1)
                if self.half_cycle_write or not self.half_cycle_write:
                    if not self.half_cycle_write:
                        self.d.rotate(-(len(d) / 2))
                    fstream.write_to_file(self.csv, self.d)

    def sample_mhs(self, mem, core, ramp):
        samples = []
        time.sleep(10) # wait 15s for first sample, 5s else
        while len(samples) < 3 or self._mean_confidence(samples) > self.desired_accuracy_in_mhs:
            time.sleep(5)
            sample = sgminer.devs()[self.card]['MHS 5s']
            samples.extend([sample])
        mhs = np.mean(np.array(samples))

        if ramp == 1:
            self.d.append('%i,%i,%f' % (mem, core, mhs))
        if ramp == -1:
            self.d.appendleft('%i,%i,%f' % (mem, core, mhs))

        print '%i,%i,%f' % (mem, core, mhs)
        sys.stdout.flush()

    def set_clocks(self, mem, core, ramp):
        if not (mem, core) in self.skip:
            with threadLock:
                if mem == self.mem_min and core == self.core_min:
                    print sgminer.gpumem('%i,%i' % (self.card, mem))
                    print sgminer.gpuengine('%i,%i' % (self.card, core))
                elif core == self.core_min and ramp == 1 or core == self.core_max and ramp == -1:
                    print sgminer.gpumem('%i,%i' % (self.card, mem))
                else:
                    print sgminer.gpuengine('%i,%i' % (self.card, core))
                print 'GPU %i: adjusting clock to %i,%i' % (self.card, mem, core)

                self.sample_mhs(mem, core, ramp)

        return -ramp

    def start(self):
        self.skip = fstream.check_file(self.csv, self.skip)
        self.cycle_thru_clocks()

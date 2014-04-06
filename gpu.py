#!/usr/bin/env python2.7

from itertools import product
import api
import collections
import numpy as np
import os
import scipy as sp
import scipy.stats
import sys
import time

class Instance:
    def __init__(self, api_handle, gpu_id, m_min, m_max, m_step, c_min, c_max, c_step, mhs_accuracy, cy_write):
        self.sgminer = api_handle
        self.card = gpu_id
        self.mem_min = m_min
        self.mem_max = m_max
        self.mem_step = m_step
        self.core_min = c_min
        self.core_max = c_max
        self.core_step = c_step
        self.desired_accuracy_in_mhs = mhs_accuracy
        self.half_cycle_write = cy_write
        self.csv = 'mhs-gpu%i.csv' % gpu_id
        self.skip = []
        self.d = collections.deque()

    def mean_confidence(self, data, confidence=0.95):
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

    def set_clocks(self, mem, core, ramp):
        if not (mem, core) in self.skip:
            if mem == self.mem_min and core == self.core_min:
                print self.sgminer.gpumem('%i,%i' % (self.card, mem))
                print self.sgminer.gpuengine('%i,%i' % (self.card, core))
            elif core == self.core_min and ramp == 1 or core == self.core_max and ramp == -1:
                print self.sgminer.gpumem('%i,%i' % (self.card, mem))
            else:
                print self.sgminer.gpuengine('%i,%i' % (self.card, core))
            print 'GPU %i: adjusting clock to %i,%i' % (self.card, mem, core)

            s = self.sample_mhs(mem, core, ramp)
            return s

    def sample_mhs(self, mem, core, ramp):
        samples = []
        time.sleep(10) # wait 15s for first sample, 5s else
        while len(samples) < 3 or self.mean_confidence(samples) > self.desired_accuracy_in_mhs:
            time.sleep(5)
            sample = self.sgminer.devs()[self.card]['MHS 5s']
            samples.extend([sample])
        mhs = np.mean(np.array(samples))

        if ramp == 1:
            self.d.append('%i,%i,%f' % (mem, core, mhs))
        if ramp == -1:
            self.d.appendleft('%i,%i,%f' % (mem, core, mhs))

        print '%i,%i,%f' % (mem, core, mhs)
        sys.stdout.flush()

        return -ramp

    def check_step(self):
        if (self.mem_max - self.mem_min) % self.mem_step != 0:
            print 'GPU %i: memory step (%i) is not a factor of memory clock range (%i)' % (self.card, self.mem_step, self.mem_max - self.mem_min)
            sys.exit()
        if (self.core_max - self.core_min) % self.core_step != 0:
            print 'GPU %i: core step (%i) is not a factor of core clock range (%i)' % (self.card, self.core_max - self.core_min, self.core_step)
            sys.exit()

    def check_file(self):
        try:
            with open(self.csv, 'r') as output:
                for mem, core, mhs in [_.split(',') for _ in output]:
                    if mem != "mem":
                        self.skip.append((int(mem),int(core)))
        except IOError:
            with open(self.csv, 'w') as output:
    	        output.write('mem,core,mhs\n')
            pass

    def write_to_file(self, output):
        while True:
            try:
                output.write(self.d.popleft() + '\n')
            except IndexError:
                break
        output.flush()

    def start(self):
        self.check_step()
        self.check_file()
        self.main()

    def main(self):
        with open(self.csv, 'a') as output:
            core_ramp = 1
            for mem in xrange(self.mem_min, self.mem_max+1, self.mem_step):
                if core_ramp == 1:
                    for core in xrange(self.core_min, self.core_max+1, self.core_step):
                        core_ramp = self.set_clocks(mem, core, 1)
                    if self.half_cycle_write:
                        self.write_to_file(output)
                elif core_ramp == -1:
                    for core in xrange(self.core_max, self.core_min-1, -self.core_step):
                        core_ramp = self.set_clocks(mem, core, -1)
                    if self.half_cycle_write or not self.half_cycle_write:
                        if not self.half_cycle_write:
                            self.d.rotate(-(len(d) / 2))
                        self.write_to_file(output)

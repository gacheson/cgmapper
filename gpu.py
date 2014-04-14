#!/usr/bin/env python2.7

from itertools import product
import api
import collections
import numpy as np
import os
import scipy as sp
import scipy.stats
import sys
import threading
import time
import utilities as util

fstream = util.FileStream()
cgminer = api.CGMiner()
threadLock = threading.Lock()

class Instance:
    def __init__(self, gpu_id, m_min, m_max, m_step, c_min, c_max, c_step, mhs_accuracy, d_print, v_print):
        self.card = gpu_id
        self.mem_min = m_min
        self.mem_max = m_max
        self.mem_step = m_step
        self.core_min = c_min
        self.core_max = c_max
        self.core_step = c_step
        self.desired_accuracy_in_mhs = mhs_accuracy
        self.debug_print = d_print
        self.verbose_print = v_print
        self.filename = 'mhs-{0}.csv'.format(gpu_id)
        self.skip = []

    def _mean_confidence(self, data, confidence=0.95):
        infinity = 1.0e24
        a = 1.0 * np.array(data)
        n = len(a)
        if n == 0:
            util.cprint_('Not enough data', self.verbose_print)
            return infinity
        m, se = np.mean(a), scipy.stats.sem(a)
        h = se * sp.stats.t._ppf((1+confidence)/2., n-1)
        util.cprint_('GPU {0}: h = {1:.14f}'.format(self.card, np.asscalar(h)), self.verbose_print)
        return h

    def cycle_thru_clocks(self):
        core_ramp = 1
        for mem in xrange(self.mem_min, self.mem_max+1, self.mem_step):
            if core_ramp == 1:
                for core in xrange(self.core_min, self.core_max+1, self.core_step):
                    core_ramp = self.set_clocks(mem, core, 1)
            elif core_ramp == -1:
                for core in xrange(self.core_max, self.core_min-1, -self.core_step):
                    core_ramp = self.set_clocks(mem, core, -1)

    def find_set_optimal_clocks(self):
        values = fstream.file_to_list(self.filename)
        if values:
            max_ = max(values, key=lambda x:x[2])
            util.cprint_(cgminer.gpumem('{0},{1}'.format(self.card, max_[0])), self.debug_print)
            util.cprint_(cgminer.gpuengine('{0},{1}'.format(self.card, max_[1])), self.debug_print)
            print 'Setting GPU {0} to optimal clocks {1},{2}'.format(self.card, max_[0], max_[1])

    def sample_mhs(self, mem, core, ramp):
        samples = []
        time.sleep(10) # wait 15s for first sample, 5s else
        while len(samples) < 3 or self._mean_confidence(samples) > self.desired_accuracy_in_mhs:
            time.sleep(5)
            with threadLock:
                sample = cgminer.devs()[self.card]['MHS 5s']
            samples.extend([sample])
        mhs = np.mean(np.array(samples))

        util.cprint_('Measuring GPU {0} at {1},{2},{3:.6f}'.format(self.card, mem, core, mhs), self.verbose_print)
        sys.stdout.flush()
        
        return mhs

    def set_clocks(self, mem, core, ramp):
        if not (mem, core) in self.skip:
            with threadLock:
                if mem == self.mem_min and core == self.core_min:
                    util.cprint_(cgminer.gpumem('{0},{1}'.format(self.card, mem)), self.debug_print)
                    util.cprint_(cgminer.gpuengine('{0},{1}'.format(self.card, core)), self.debug_print)
                elif core == self.core_min and ramp == 1 or core == self.core_max and ramp == -1:
                    util.cprint_(cgminer.gpumem('{0},{1}'.format(self.card, mem)), self.debug_print)
                else:
                    util.cprint_(cgminer.gpuengine('{0},{1}'.format(self.card, core)), self.debug_print)

                print 'Adjusting GPU {0} clocks to {1},{2}'.format(self.card, mem, core)

            fstream.write_to_file(mem, core, self.sample_mhs(mem, core, ramp), self.card, self.filename, self.debug_print)
            fstream.sort_in_file(self.filename)

        return -ramp

    def start(self):
        self.skip = fstream.check_file(self.filename, self.skip, self.debug_print)
        self.cycle_thru_clocks()
        self.find_set_optimal_clocks()


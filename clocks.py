#!/usr/bin/env python

from itertools import product
import api
import collections
import numpy as np
import os
import scipy as sp
import scipy.stats
import sys
import time

# Customize these
card = 1       # Card number, 0 is the first
mem_min = 1250 # The memory clock to start at
mem_max = 1460 # The memory clock to end at
mem_step = 3   # The interval to try memory clocks at (1 = all, 2 = every other, etc.)
core_min = 830 # The core clock to start at
core_max = 890 # The core clock to end at
core_step = 1  # The interval to try core clocks
desired_accuracy_in_mhs = 0.002 # The desired accuracy of samples in megahashes per second. .002 or .001 is recommended here
half_cycle_write = True # The desired frequency of writes made to file. Half cycle (True) writes at core min and at core max. Full cycle (False) only writes at core min


# Probably don't customize these
csv='mhs.csv'
infinity = 1.0e24
core_ramp = 1


sgminer = api.SGMiner()
d = collections.deque()

def mean_confidence(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    if n == 0:
      print "not enough data"
      return infinity
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * sp.stats.t._ppf((1+confidence)/2., n-1)
    print "h: " + str(h)
    return h

def step_check():
    if (mem_max - mem_min) % mem_step != 0:
        print 'memory step (%i) is not a factor of memory clock range (%i)' % (mem_step, mem_max - mem_min)
        sys.exit()
    if (core_max - core_min) % core_step != 0:
        print 'core step (%i) is not a factor of core clock range (%i)' % (core_max - core_min, core_step)
        sys.exit()

def cycle_clocks(ramp):
    if not (mem, core) in skip:
        if mem == mem_min and core == core_min:
            print sgminer.gpumem('%i,%i' % (card, mem))
            print sgminer.gpuengine('%i,%i' % (card, core))
        elif core == core_min and ramp == 1 or core == core_max and ramp == -1:
            print sgminer.gpumem('%i,%i' % (card, mem))
        else:
            print sgminer.gpuengine('%i,%i' % (card, core))
        print 'adjusting clock to %i,%i' % (mem, core)

        samples = []
        time.sleep(10) # wait 15s for first sample, 5s else
        while len(samples) < 3 or mean_confidence(samples) > desired_accuracy_in_mhs:
            time.sleep(5)
            sample = sgminer.devs()[card]['MHS 5s']
            samples.extend([sample])
        mhs = np.mean(np.array(samples))

        if ramp == 1:
            d.append('%i,%i,%f' % (mem, core, mhs))
        if ramp == -1:
            d.appendleft('%i,%i,%f' % (mem, core, mhs))

        print '%i,%i,%f' % (mem, core, mhs)
        sys.stdout.flush()

        return -ramp

def write_to_file():
    while True:
        try:
            output.write(d.popleft() + '\n')
        except IndexError:
            break
    output.flush()

step_check()

skip = []
try:
    with open(csv, 'r') as output:
        for mem, core, mhz in [_.split(',') for _ in output]:
            if mem != "mem":
                skip.append((int(mem),int(core)))
except IOError:
    with open(csv, 'w') as output:
    	output.write('mem,core,mhs\n')
    pass

with open(csv, 'a') as output:
    for mem in xrange(mem_min, mem_max+1, mem_step):
        if core_ramp == 1:
            for core in xrange(core_min, core_max+1, core_step):
                core_ramp = cycle_clocks(1)
            if half_cycle_write:
                write_to_file()
        elif core_ramp == -1:
            for core in xrange(core_max, core_min-1, -core_step):
                core_ramp = cycle_clocks(-1)
            if half_cycle_write or not half_cycle_write:
                if not half_cycle_write:
                    d.rotate(-(len(d) / 2))
                write_to_file()

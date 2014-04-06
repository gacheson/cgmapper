#!/usr/bin/env python

import api
import gpu

# Customize these
card = 1 # Card number, 0 is the first
mem_min = 1250 # The memory clock to start at
mem_max = 1460 # The memory clock to end at
mem_step = 3 # The interval to try memory clocks at (1 = all, 2 = every other, etc.)
core_min = 830 # The core clock to start at
core_max = 890 # The core clock to end at
core_step = 1 # The interval to try core clocks
desired_accuracy_in_mhs = 0.002 # The desired accuracy of samples in megahashes per second. .002 or .001 is recommended here
half_cycle_write = True # The desired frequency of writes made to file. Half cycle (True) writes at core min and at core max. Full cycle (False) only writes at core min

sgminer = api.SGMiner()

gpu1 = gpu.Instance(sgminer, card, mem_min, mem_max, mem_step, core_min, core_max, core_step, desired_accuracy_in_mhs, half_cycle_write)

gpu1.start()


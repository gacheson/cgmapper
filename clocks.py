#!/usr/bin/env python

import utilities as util
import gpu
import sys
import threads

# Customize these
card = '1'       # Card number, 0 is the first
mem_min = '1400' # The memory clock to start at
mem_max = '1500' # The memory clock to end at
mem_step = '1'   # The interval to try memory clocks at (1 = all, 2 = every other, etc.)
core_min = '925' # The core clock to start at
core_max = '1050' # The core clock to end at
core_step = '1'  # The interval to try core clocks
desired_accuracy_in_mhs = 0.002 # The desired accuracy of samples in megahashes per second. .002 or .001 is recommended here
debug_print = False # The desired debug print setting. Debug print  will show execution statements for each GPU thread
verbose_print = False # The desired verbose print setting. Verbose print will show additional data about each GPU thread


gpu_id = map(int, card.split(','))
m_min = map(int, mem_min.split(','))
m_max = map(int, mem_max.split(','))
m_step = map(int, mem_step.split(','))
c_min = map(int, core_min.split(','))
c_max = map(int, core_max.split(','))
c_step = map(int, core_step.split(','))

card_length = len(gpu_id)
argument_length = 1
use_single = False

if any(len(lst) != card_length for lst in [m_min, m_max, m_step, c_min, c_max, c_step]): # not individually set
    use_single = True
    if any(len(lst) != argument_length for lst in [m_min, m_max, m_step, c_min, c_max, c_step]): # not single
        print 'Uneven argument length. Check your settings.'
        sys.exit()

gpu_list = []
thread_list = []

if use_single:
    for g in xrange(0, len(gpu_id)):
        gpu_list.append(gpu.Instance(gpu_id[g], util.get_first(m_min), util.get_first(m_max), util.get_first(m_step), util.get_first(c_min), util.get_first(c_max), util.get_first(c_step), desired_accuracy_in_mhs, debug_print, verbose_print))
else:
    for g in xrange(0, len(gpu_id)):
        gpu_list.append(gpu.Instance(gpu_id[g], m_min[g], m_max[g], m_step[g], c_min[g], c_max[g], c_step[g], desired_accuracy_in_mhs, debug_print, verbose_print))

for t in xrange(1, len(gpu_list)+1):
    t = threads.Thread(t, 'Thread-{0}'.format(t), gpu_list[t-1])
    t.start()
    thread_list.append(t)

for t in thread_list:
    t.join()
util.cprint_('Exiting Main Thread', debug_print)


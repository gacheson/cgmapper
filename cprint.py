#!/usr/bin/env python2.7

"""
Utility function to allow for conditional printing of a string
"""
def cprint_(string, flag, count=None):
    if flag and count > 0:
        for c in xrange(0, count+1):
            print string
    elif flag and (count == None or count == 0):
        print string
    else:
        pass


#!/usr/bin/env python2.7

"""
Utility function that allows for conditional printing of strings
"""
def cprint_(string, flag, count=None):
    if flag and (count == None or count <= 0):
        print string
        if not count == None or count == 0:
            count -= 1
    else:
        pass


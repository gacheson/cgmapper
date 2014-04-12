#!/usr/bin/env python2.7

def bprint(s, p, c=None):
    if p and (c == None or c <= 0):
        print s
        if not c == None or c == 0:
            c -= 1
    else:
        pass


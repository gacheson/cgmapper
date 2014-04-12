#!/usr/bin/env python2.7

import boolprint as bp
import collections

class FileStream:
    def check_file(self, csv, skip, debug_print):
        try:
            with open(csv, 'r') as output:
                for mem, core, mhs in [_.split(',') for _ in output]:
                    if mem != "mem":
                        skip.append((int(mem),int(core)))
        except IOError:
            with open(csv, 'w') as output:
                output.write('mem,core,mhs\n')
                bp.bprint("Making file '{0}'".format(csv), debug_print)
            pass
        output.close()
        return skip

    def write_to_file(self, card, csv, d, debug_print):
        with open(csv, 'a') as output:
            while True:
                try:
                    output.write(d.popleft() + '\n')
                    bp.bprint("Writing GPU {0} buffer contents to file '{1}'".format(card, csv), debug_print, 1)
                except IndexError:
                    break
            output.close()


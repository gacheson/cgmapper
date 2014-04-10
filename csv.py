#!/usr/bin/env python2.7

import collections

class FileStream:
    def check_file(self, csv, skip):
        try:
            with open(csv, 'r') as output:
                for mem, core, mhs in [_.split(',') for _ in output]:
                    if mem != "mem":
                        skip.append((int(mem),int(core)))
        except IOError:
            with open(csv, 'w') as output:
                output.write('mem,core,mhs\n')
            pass
        output.close()
        return skip

    def write_to_file(self, csv, d):
        with open(csv, 'a') as output:
            while True:
                try:
                    output.write(d.popleft() + '\n')
                except IndexError:
                    break
            output.close()

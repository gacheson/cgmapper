#!/usr/bin/env python2.7

import csv
import operator
import sys

class FileStream:
    def check_file(self, filename, skip, debug_print):
        try:
            with open(filename, 'rb') as output:
                reader = csv.reader(output, delimiter=',')
                next(reader, None) # skip the header
                for row in reader:
                    skip.append((int(row[0]),int(row[1])))
        except IOError:
            with open(filename, 'wb') as output:
                writer = csv.writer(output, delimiter=',', quoting=csv.QUOTE_NONE)
                writer.writerow(["mem","core","mhs"])
                cprint_("Making file '{0}'".format(filename), debug_print)
            pass
        return skip

    def file_to_list(self, filename, header=False):
        temp = []
        with open(filename, 'rb') as output:
            reader = csv.reader(output, delimiter=',')
            if not header:
                next(reader, None) # skip the header
                for row in reader:
                    temp.append(tuple(row))
            else:
                temp.append(next(reader, None)) # save the header
        return temp

    def sort_in_file(self, filename):
        header = self.file_to_list(filename, True)
        data = self.file_to_list(filename)

        data = sorted(data, key=operator.itemgetter(0, 1))

        with open(filename, 'wb') as output:
            writer = csv.writer(output, delimiter=',', quoting=csv.QUOTE_NONE)
            for row in header:
                writer.writerow(row)
            for row in data:
                writer.writerow(row)

    def write_to_file(self, mem, core, mhs, card, filename, debug_print):
        with open(filename, 'ab') as output:
            writer = csv.writer(output, delimiter=',', quoting=csv.QUOTE_NONE)
            writer.writerow([mem, core, "{0:.6f}".format(mhs)])
            cprint_("Writing GPU {0} data to file '{1}'".format(card, filename), debug_print, 1)

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


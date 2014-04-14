#!/usr/bin/env python2.7

import csv
import operator
import sys
import time

class FileStream:
    def check_file(self, filename, skip, debug_print):
        try:
            with open(filename, 'rb') as output:
                reader = csv.reader(output, delimiter=',')
                next(reader, None) # skip the header
                for row in reader:
                    skip.append((int(row[0]),int(row[1])))
                cprint_("Found file '{0}'".format(filename), debug_print, 1)
        except IOError:
            with open(filename, 'wb') as output:
                writer = csv.writer(output, delimiter=',', quoting=csv.QUOTE_NONE)
                writer.writerow(["mem","core","mhs"])
                cprint_("Making file '{0}'".format(filename), debug_print, 1)
            pass
        return skip

    def file_to_list(self, filename, debug_print, header=False):
        temp = []
        with open(filename, 'rb') as output:
            reader = csv.reader(output, delimiter=',')
            if not header:
                next(reader, None) # skip the header
                for row in reader:
                    temp.append(tuple(row))
                cprint_("Reading data from file '{0}' into memory".format(filename), debug_print, 1)
            else:
                temp.append(next(reader, None)) # save the header
                cprint_("Reading header from file '{0}' into memory".format(filename), debug_print, 1)
        return temp

    def sort_in_file(self, filename, debug_print):
        header = self.file_to_list(filename, debug_print, True)
        data = self.file_to_list(filename, debug_print)

        data = sorted(data, key=operator.itemgetter(0, 1))

        with open(filename, 'wb') as output:
            writer = csv.writer(output, delimiter=',', quoting=csv.QUOTE_NONE)
            for row in header:
                writer.writerow(row)
            for row in data:
                writer.writerow(row)
            cprint_("Writing sorted data to file '{0}'".format(filename), debug_print, 1)

    def write_to_file(self, mem, core, mhs, card, filename, debug_print):
        with open(filename, 'ab') as output:
            writer = csv.writer(output, delimiter=',', quoting=csv.QUOTE_NONE)
            writer.writerow([mem, core, "{0:.6f}".format(mhs)])
            cprint_("Writing GPU {0} data to file '{1}'".format(card, filename), debug_print, 1)

"""
Utility function to allow for conditional printing of a string
"""
def cprint_(string, flag, delay=0, count=None):
    if flag and count > 0:
        for _ in xrange(0, count):
            print string
            time.sleep(delay)
    elif flag and (count == None or count == 0):
        print string
        time.sleep(delay)
    else:
        pass

"""
Utility function to get the first item in a list
"""
def get_first(iterable, default=None):
    if iterable:
        for item in iterable:
            return item
    return default


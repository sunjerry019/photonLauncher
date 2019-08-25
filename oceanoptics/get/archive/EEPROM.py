#!/usr/bin/env python2

import sys, os
base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, "..", "..", "helpers"))
sys.path.insert(0, root_dir)
from getSpectra import Icecube
import struct
import binascii

with Icecube() as cube:
    # READ EEPROM
    for i in xrange(0, 31):
        print "Reading Byte " + str(i)
        cube.icecube.bulkWrite(1, '\x05' + chr(i))
        data = cube.icecube.bulkRead(1, 17)
        # bytes = [data[i:i+2] for i in xrange(0, len(data), 2)]
        retCount = len(data)
        print(retCount)
        unpacked = struct.unpack('<' + str(retCount) +'c', data)
        print(unpacked)

    # print(binascii.hexlify(data).decode('ascii'))

    # READ TEMPERATURE
    cube.icecube.bulkWrite(1, '\x6C')
    data = cube.icecube.bulkRead(1, 3)
    if struct.unpack('<c', data[0:1])[0] == b'\x08':
        # Read successful
        ADC = struct.unpack('<h', data[1:])[0]
        print(0.003906 * ADC)
    else:
        print("ADC Read unsuccessful")


# 000f701700000000000f000000008055
# import struct
#
# data = b'\x00\x0f\x70\x17\x00\x00\x00\x00\x00\x0f\x00\x00\x00\x00\x80\x55'
# a = struct.pack('<s', data)
# b = struct.unpack('<s', a)
# print b
# bytes = [data[i:i+1] for i in xrange(0, len(data))]

# https://docs.python.org/3.0/library/struct.html

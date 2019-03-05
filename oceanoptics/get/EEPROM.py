#!/usr/bin/env python2

# import sys
# sys.path.insert(0, '../../helpers/')
# from getSpectra import Icecube
# import struct
# import binascii
#
# with Icecube() as cube:
#     cube.icecube.bulkWrite(1, '\xFE')
#     data = cube.icecube.bulkRead(1, 30)
#     bytes = [data[i:i+2] for i in xrange(0, len(data), 2)]
#     print(struct.unpack('<', data))
#     # print(binascii.hexlify(data).decode('ascii'))


# 000f701700000000000f000000008055
import struct

data = b'\x00\x0f\x70\x17\x00\x00\x00\x00\x00\x0f\x00\x00\x00\x00\x80\x55'
a = struct.pack('<h', data)
b = struct.unpack('<h', a)
print b
# bytes = [data[i:i+1] for i in xrange(0, len(data))]

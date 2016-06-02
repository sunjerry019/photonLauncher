import sys
sys.path.insert(0, '../../helpers/')

from getSpectra import Icecube
import time

with Icecube() as cube:
    cube.setIntegrationTime(10)
    while True:
        try:
            spec = cube.getSpectra()
            with open('.temp', 'w') as f:
                for i in spec:
                    f.write("{}\t{}\n".format(i[0], i[1]))
            time.sleep(1)
        except KeyboardInterrupt:
            print "Saving..."
            cube.__exit__()
#            with open("{}.dat".format(time.strftime("%M%S")) as g:
#                for _ in spec:
#                    g.write("{}\t{}\n".format(_[0], _[1]))

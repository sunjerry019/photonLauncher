import sys, os
base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, "..", "..", "helpers"))
sys.path.insert(0, root_dir)
from getSpectra import Icecube
import cmd
import time
from threading import Thread
import subprocess

class spectre(cmd.Cmd):
    def do_start(self, line):
        self.log = False
        self.cube = Icecube()
        self.spec = 0
        self.cube.setIntegrationTime(10)
        t = Thread(target=self.specgen)
        u = Thread(target=self.plot)
        t.start()
        time.sleep(0.1)
        u.start()
    def plot(self):
        subprocess.call(["gnuplot", "loop.gnu"])

    def specgen(self):
        while True:
            print "\r{}".format(time.strftime("%D"))
            self.spec = self.cube.getSpectra()
            with open('.temp', 'w') as f:
                for i in self.spec:
                    f.write("{}\t{}\n".format(i[0], i[1]))
            if self.log:
                self.n -= 1
                for i in self.spec:
                    g.write("{}\t{}\n".format(i[0], i[1]))
                if self.n == 0:
                    self.log = False
                    self.g.close()

            time.sleep(1)

    def do_EOF(self, line):
        print("\n Exiting Spectre prompt.")
        self.cube.close()
        return True

    def do_capture(self, n = 1):
        self.n = n
        self.log = True
        self.g = open('/mnt/photonics/spectra/{}'.format(time.strftime('%Y%m%d_%H%M')), 'w')
if __name__ == "__main__":
    specterm().cmdloop()

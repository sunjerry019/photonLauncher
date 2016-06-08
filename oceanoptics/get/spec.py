import sys
sys.path.insert(0, "../../helpers")
from getSpectra import Icecube
import cmd
import time
from threading import Thread
import subprocess

class specterm(cmd.Cmd):
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
            time.sleep(1)

    def do_EOF(self, line):
        print("\n Exiting specterm prompt.")
        self.cube.close()

        return True
if __name__ == "__main__":
    specterm().cmdloop()

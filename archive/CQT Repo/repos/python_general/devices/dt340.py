import subprocess


class DT340():

    """
    Dummy class to interact with the DT340 counter PCI board, based on the
    program written by Christian.
    """
    cmd = '/home/qitlab/programs/dt340/apps/counter2'

    def __init__(self):
        pass

    @property
    def read_all(self):
        """
        returns an array of floats, each one corresponding to the value
        of a channel, in order
        """
        return subprocess.check_output(self.cmd).strip().split()

    def read_ch(self, ch=0):
        """
        returns an array of floats, each one corresponding to the value
        of a channel, in order
        """
        if isinstance(ch, int):
            return self.read_all[ch]
        else:
            return [self.read_all[x] for x in ch]

if __name__ == '__main__':
    counter = DT340()
    all_counts = counter.read_all
    print['Counts in channel {0}: {1}\n'.format(idx, counts)
          for idx, counts
          in enumerate(all_counts)]

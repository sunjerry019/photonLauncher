import numpy as np
import matplotlib.pylab as plt
import datetime


class Spectrum:
    def __init__(self, filename=''):
        self.noise_a = []
        self.frequency_a = []
        self.noise_b = []
        self.frequency_b = []
        self.noise_c = []
        self.frequency_c = []
        self.filename = filename
        self.date = datetime.date
        self.RBW = []
        self.VBW = []

        if filename != '':
            self.generate(filename)

    def generate(self, filename):
        """
        import file

        """
        self.filename = filename
        frequency = self.frequency_a
        noise = self.noise_a

        with open(filename, 'r') as f:
            for line in f:
                if '# Begin TRACE B Data' in line:
                    frequency = self.frequency_b
                    noise = self.noise_b

                if 'DATE=' in line:
                    date = line.strip().split('-')
                    self.date = datetime.date(int(date[0].split('=')[1]), int(date[1]), int(date[2]))

                elif 'RBW=' in line:
                    self.RBW = float(line.split('=')[1])

                elif 'VBW=' in line:
                    self.VBW = float(line.split('=')[1])

                if line[0:2] == 'P_':
                    frequency.append(float(line.split()[2]))
                    noise.append(float(line.split()[0].split('=')[1]))

    def plot(self, new_figure='yes'):
        """
        function to plot the spectrum
        """

        if new_figure == 'yes':
            plt.figure('Spectrum from file: '+self.filename)
            plt.xlabel('frequency (MHz)')
            plt.ylabel('noise (dBm)')
            plt.title('Taken on the ' + self.date.isoformat()
                      + '\nSpan:  {0:.2e} to {1:.2e} MHz\n'
                      'RBW={2:.2e} MHz, VBW={3:.2e} MHz'.format(np.min(self.frequency_a),
                                                                np.max(self.frequency_a),
                                                                self.RBW, self.VBW))
        plt.plot(self.frequency_a, self.noise_a)
        plt.xlim([min(self.frequency_a), max(self.frequency_a)])

import numpy as np
import time
import subprocess

dac_set_exe = '/home/qitlab/programs/usbpatgendriver/testapps/usbdacset'


def set_dac(channel, new_voltage):
    """
    Set the voltage on the USB DAC

    :param channel: channel to address
    :param new_voltage: set voltage
    """
    try:
        subprocess.check_call([dac_set_exe, str(channel), str(new_voltage)], stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    except Exception:
        pass


def ramp_fn(amplitude, sampling):
	# part 1: generate the ramp with the proper sampling
	shape = np.linspace(0.,1., int(sampling))

	#part 2: adjust the amplitude
	amp = max(amplitude)-min(amplitude)
	bias = min(amplitude)
	return shape * amp + bias


def main():
	channel = 1
	t_channel = 5
	sampling = 2000
	freq = 1  # in hertz
	# creates the ramp
	ramp = ramp_fn([-10, 10], sampling)

	# adjust the timing
	wait_t = 1./(freq * sampling)
	print(wait_t)
	for i in range(10):
		set_dac(t_channel, 5)
		time.sleep(.005)
		set_dac(t_channel, 0)
		print(i)		
		for new_v in ramp:
			set_dac(channel, new_v)
			time.sleep(wait_t)
			# print(new_v)

if __name__ == '__main__':
	main()



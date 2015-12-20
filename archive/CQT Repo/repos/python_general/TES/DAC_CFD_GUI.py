#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk
import subprocess
import glob
import cfd_lib as cfd

dac_set_exe = '/home/qitlab/programs/usbpatgendriver/testapps/usbdacset'
cfd_path = glob.glob('/dev/serial/by-id/*CFD*')[0]
tes_00_channel = 0
tes_01_channel = 2
mod_00_channel = 1
mod_01_channel = 3
scale = 4.07


# class CFD(serial.Serial):
#     def __init__(self, device_path=''):
#         if device_path == '':
#             device_path = glob.glob('/dev/serial/by-id/*CFD*')[0]
#         try:
#             serial.Serial.__init__(self, device_path, timeout=2)
#         except:
#             print('The indicated device cannot be found')
#
#     def set(self, channel, new_voltage):
#         self.write('TRESH {0} {1}\n'.format(channel, new_voltage).encode('ascii'))
#
#     @property
#     def threshold(self):
#         self.write('TRESH? 0\n'.encode('ascii'))
#         self.write('TRESH? 1\n'.encode('ascii'))
#         return [th.strip() for th in self.readlines()]

cfd = cfd.CFD()


def set_cfd_00(*args):
    new_v = CFD_00_entry.get()
    cfd.set(0, new_v)


def set_cfd_01(*args):
    new_v = CFD_01_entry.get()
    cfd.set(1, new_v)


def clamp(n):
    return max(min(10.0, float(n)), -10.0)


def set_dac(channel, new_voltage):
    """
    Set the voltage on the USB DAC

    :param channel: channel to address
    :param new_voltage: set voltage
    """
    try:
        subprocess.check_call([dac_set_exe, str(channel), str(new_voltage)], stderr=subprocess.STDOUT,
                              stdout=subprocess.PIPE)
    except Exception:
        pass


def apply_t00(*args):
    new_v = tes_bias_00_in.get()
    new_v = clamp(new_v)
    tes_bias_00_out.set(new_v)
    set_dac(tes_00_channel, new_v)
    current_00.set('{0:.2f}'.format(new_v*scale))


def apply_t01(*args):
    new_v = tes_bias_01_in.get()
    new_v = clamp(new_v)
    tes_bias_01_out.set(new_v)
    set_dac(tes_01_channel, new_v)
    current_01.set('{0:.2f}'.format(new_v*scale))


def apply_m00(*args):
    new_v = modulation_00_in.get()
    new_v = clamp(new_v)
    modulation_00_out.set(new_v)
    set_dac(mod_00_channel, new_v)


def apply_m01(*args):
    new_v = modulation_01_in.get()
    new_v = clamp(new_v)
    modulation_01_out.set(new_v)
    set_dac(mod_01_channel, new_v)


def set_zero(*args):
    tes_bias_00_out.set(0)
    tes_bias_01_out.set(0)
    modulation_00_out.set(0)
    modulation_01_out.set(0)
    [set_dac(channel, 0) for channel in range(3)]
    tes_bias_00_in.set(0)
    tes_bias_01_in.set(0)
    modulation_00_in.set(0)
    modulation_01_in.set(0)
    current_00.set(0)
    current_01.set(0)


def set_zero_b(*args):
    tes_bias_00_out.set(0)
    modulation_00_out.set(0)
    [set_dac(channel, 0) for channel in [0, 2]]
    tes_bias_00_in.set(0)
    modulation_00_in.set(0)
    current_00.set(0)


def set_zero_g(*args):
    tes_bias_01_out.set(0)
    modulation_01_out.set(0)
    [set_dac(channel, 0) for channel in [1, 3]]
    tes_bias_01_in.set(0)
    modulation_01_in.set(0)
    current_01.set(0)


def close_w(*args):
    set_zero()
    root.destroy()

# ## Setting up the main window ###
root = Tk()
root.title("ADC controller")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

###  Variables used ###
tes_bias_00_in = StringVar()
tes_bias_01_in = StringVar()
tes_bias_00_out = StringVar()
tes_bias_01_out = StringVar()
modulation_00_in = StringVar()
modulation_01_in = StringVar()
modulation_00_out = StringVar()
modulation_01_out = StringVar()
current_00 = StringVar()
current_01 = StringVar()

CFD_tr_00 = StringVar()
CFD_tr_01 = StringVar()

# Configuring the entry as spinboxes
tes_bias_00_in_entry = Spinbox(mainframe, width=7, from_=-10.0, to=10.0, increment=0.013,
                               textvariable=tes_bias_00_in, command=apply_t00)
modulation_00_in_entry = Spinbox(mainframe, width=7, from_=-10.0, to=10.0, increment=0.05,
                                 textvariable=modulation_00_in, command=apply_m00)
CFD_00_entry = Spinbox(mainframe, width=7, from_=0, to=1, increment=0.001,
                       textvariable=CFD_tr_00, command=set_cfd_00)

tes_bias_01_in_entry = Spinbox(mainframe, width=7, from_=-10.0, to=10.0, increment=0.013,
                               textvariable=tes_bias_01_in, command=apply_t01)
modulation_01_in_entry = Spinbox(mainframe, width=7, from_=-10.0, to=10.0, increment=0.05,
                                 textvariable=modulation_01_in, command=apply_m01)
CFD_01_entry = Spinbox(mainframe, width=7, from_=0, to=1, increment=0.001,
                       textvariable=CFD_tr_01, command=set_cfd_01)

### positioning the widgets
# Inputs
tes_bias_00_in_entry.grid(column=2, row=2, sticky=(W, E))
tes_bias_01_in_entry.grid(column=2, row=6, sticky=(W, E))
modulation_00_in_entry.grid(column=2, row=3, sticky=(W, E))
modulation_01_in_entry.grid(column=2, row=7, sticky=(W, E))

CFD_00_entry.grid(column=2, row=4, sticky=(W, E))
CFD_01_entry.grid(column=2, row=8, sticky=(W, E))

# Labels
ttk.Label(mainframe, text="Set (V)").grid(column=2, row=1, sticky=W)
ttk.Label(mainframe, text="Actual (V)").grid(column=3, row=1, sticky=E)
ttk.Label(mainframe, text="Current (uA)").grid(column=4, row=1, sticky=E)
ttk.Label(mainframe, text="Blue TES 00 (ch 0)").grid(column=1, row=2, sticky=(W, E))
ttk.Label(mainframe, text="Green TES 01 (ch 2)").grid(column=1, row=6, sticky=(W, E))
ttk.Label(mainframe, text="MOD 00 (ch 1)").grid(column=1, row=3, sticky=(W, E))
ttk.Label(mainframe, text="MOD 01 (ch 3)").grid(column=1, row=7, sticky=(W, E))
ttk.Label(mainframe, text="CFD 00").grid(column=1, row=4, sticky=(W, E))
ttk.Label(mainframe, text="CFD 01").grid(column=1, row=8, sticky=(W, E))

# outputs
ttk.Label(mainframe, textvariable=tes_bias_00_out).grid(column=3, row=2, sticky=(W, E))
ttk.Label(mainframe, textvariable=tes_bias_01_out).grid(column=3, row=6, sticky=(W, E))
ttk.Label(mainframe, textvariable=modulation_00_out).grid(column=3, row=3, sticky=(W, E))
ttk.Label(mainframe, textvariable=modulation_01_out).grid(column=3, row=7, sticky=(W, E))
ttk.Label(mainframe, textvariable=current_00).grid(column=4, row=2, sticky=(W, E))
ttk.Label(mainframe, textvariable=current_01).grid(column=4, row=6, sticky=(W, E))

# buttons
ttk.Button(mainframe, text="Set Blue to 0", command=set_zero_b).grid(column=4, row=4, sticky=W)
ttk.Button(mainframe, text="Set Green to 0", command=set_zero_g).grid(column=4, row=8, sticky=W)

### padding the space surrounding all the widgets
for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)


###  Bindings  ###
tes_bias_00_in_entry.focus()
tes_bias_00_in_entry.bind('<Return>', apply_t00)
tes_bias_01_in_entry.bind('<Return>', apply_t01)
modulation_00_in_entry.bind('<Return>', apply_m00)
modulation_01_in_entry.bind('<Return>', apply_m01)
CFD_00_entry.bind('<Return>', set_cfd_00)
CFD_01_entry.bind('<Return>', set_cfd_01)

# set all the voltages to zero if you close the window
root.protocol('WM_DELETE_WINDOW', close_w)

# Initialize the input fields to zero
tes_bias_00_in.set(0)
tes_bias_01_in.set(0)
modulation_00_in.set(0)
modulation_01_in.set(0)

# finally we run it!
root.mainloop()

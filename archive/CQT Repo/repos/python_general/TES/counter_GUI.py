#!/usr/bin/env python3

"""
counter_GUI.py is the GUI for continuous counting using the USB counter module.


"""

from tkinter import *
from tkinter import ttk

sys.path.append('..')
from devices.USBcounter import *


def set_time(*args):
    counter.set_integration(int(timer_00.get()))


def start_f(*args):
    loop_flag.set(True)
    while loop_flag.get():
        all_c = counter.read_counts()
        counter_00.set(all_c[0])
        counter_01.set(all_c[1])
        counter_02.set(all_c[2])
        root.update()


def stop_f(*args):
    loop_flag.set(False)


### Setting up the main window ###
root = Tk()
root.title("USB counter")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

counter_dev = "/dev/serial/by-id/usb-Centre_for_Quantum_Technologies_USB_Counter_Ucnt-QO07F-if00-port0"
counter = Counter(counter_dev)
loop_flag = BooleanVar()
loop_flag.set(False)

###  Variables used 
counter_00 = StringVar()
counter_01 = StringVar()
counter_02 = StringVar()
timer_00 = StringVar()

# buttons
ttk.Button(mainframe, text="Start", command=start_f).grid(column=1, row=1, sticky=W)
ttk.Button(mainframe, text="Stop", command=stop_f).grid(column=2, row=1, sticky=W)

# controls
time_entry = Spinbox(mainframe, width=7, from_=0, to=10000, increment=50, textvariable=timer_00, command=set_time)
time_entry.grid(column=3, row=6, sticky=(W, E))
timer_00.set(1000)

# outputs
ttk.Label(mainframe, textvariable=counter_00).grid(column=2, row=2, sticky=(W, E))
ttk.Label(mainframe, textvariable=counter_01).grid(column=2, row=3, sticky=(W, E))
ttk.Label(mainframe, textvariable=counter_02).grid(column=2, row=4, sticky=(W, E))

### padding the space surrounding all the widgets
for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)
    
# finally we run it!
root.mainloop()
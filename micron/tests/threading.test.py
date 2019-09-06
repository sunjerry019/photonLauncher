#!/usr/bin/env python3
#
import time
import multiprocessing

def huhu():
    i = 0
    while True:
        print("Running uwu", i)
        i += 1
        time.sleep(0.5)

x = multiprocessing.Process(target=huhu)
x.start()

time.sleep(2)

for p in multiprocessing.active_children():
    p.terminate()

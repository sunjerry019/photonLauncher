#!/usr/bin/env python3

import pyaudio
import sys
sys.path.insert(0, "../")

from pwmaudio import noALSAerror

with noALSAerror():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    print(p.get_host_api_count())
    print(info)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxOutputChannels')) > 0:
                # print("Output Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
                print("Output Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i))

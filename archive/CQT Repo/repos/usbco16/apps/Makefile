# Makefile for the multicoincidence unit, modified to work with the usb version
# of the interface. Requires also the usbco16 driver
# 
# current status: copying from nudaq-based code, not tested yet.


all:  co16usb bareco16usb bc2

co16: co16usb.c	
	gcc -Wall -O3 -o co16usb co16usb.c

bareco16usb: bareco16usb.c
	gcc -Wall -O3 -o  bareco16usb bareco16usb.c

bc2: bc2.c
	gcc -Wall -O3 -o bc2 bc2.c


.PHONY: clean
clean:
	rm -f *~
	rm -f co16usb
	rm -f bareco16usb
	rm -f bc2

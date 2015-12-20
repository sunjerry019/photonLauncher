# Makefile for the usb programmer card driver.

# directory for the driver for the local OS version
localdir=$(subst /,\/,$(PWD))
loaderdir=udev
loadersrc1=$(loaderdir)/udevsrc
loadertarget1=$(loaderdir)/61-usbtmst3.rules
# this tries to establish the group for the device file
devicegrp=$(shell id -gn)

all: driver udev apps

# execute version-specific makefile
.PHONY: driver
driver:	$(loadertarget1)
	$(MAKE) -C driver

$(loadertarget1): $(loadersrc1)
	cat $(loadersrc1) | sed "s/DRIVERPATH/$(localdir)\/driver/g" | sed "s/users/$(devicegrp)/g" >$(loadertarget1)

.PHONY: clean
clean:	
	rm -f $(loadertarget1)
	rm -f 2.6/*.o 2.6/*.mod.* 2.6/*.ko 2.6/.d*
	rm -fr 2.6/.tmp*
	rm -f 2.6/Module*
	rm -f 2.6/.[a-zA-Z]*
	rm -fr *~
#	make -C apps clean


udev: 	driver $(loadertarget1)
	sudo cp $(loadertarget1) /etc/udev/rules.d/

.PHONY: apps
apps:
	make -C apps

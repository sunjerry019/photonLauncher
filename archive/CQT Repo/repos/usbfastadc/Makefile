# Makefile for the usb programmer card driver.

# directory for the driver for the local OS version (lecagy code)
localdir=$(subst /,\/,$(PWD))
sourcedir=$(PWD)/2.6
loaderdir=hotplug
loadersrc1=$(loaderdir)/udevsrc
loadertarget1=$(loaderdir)/61-usbfastadc.rules
# this tries to establish the group for the device file
devicegrp=$(shell id -gn)

all: driver hotplug apps

# execute version-specific makefile
.PHONY: driver
driver:	$(loadertarget1)
	$(MAKE) -C /lib/modules/`uname -r`/build M=$(sourcedir)

$(loadertarget1): $(loadersrc1)
	cat $(loadersrc1) | sed "s/users/$(devicegrp)/g" >$(loadertarget1)

.PHONY: clean
clean:	
	rm -f $(loadertarget1)
	rm -f 2.6/*.o 2.6/*.mod.* 2.6/*.ko 2.6/.d*
	rm -fr 2.6/.tmp*
	rm -f 2.6/Module*
	rm -f 2.6/.[a-zA-Z]*
	rm -fr *~
	make -C apps clean


udev: 	driver $(loadertarget1)
	sudo $(MAKE) -C /lib/modules/`uname -r`/build M=$(sourcedir) modules_install
	sudo /sbin/depmod -a
	sudo cp $(loadertarget1) /etc/udev/rules.d/

.PHONY: apps
apps:
	make -C apps

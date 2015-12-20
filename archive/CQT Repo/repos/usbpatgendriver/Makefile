# Makefile for the usb pattern generator card. For multiple SuSE versions.
# Currently  generates the drivers and uploads different hotpluggers
#
# This is a dirty version for driver development


# directory for the driver for the local OS version
localdir=$(subst /,\/,$(PWD))
version="2.6"
sourcedir=$(PWD)/2.6
loaderdir=hotplug
loadersrc1=$(loaderdir)/udevsrc
loadertarget1=$(loaderdir)/61-usbpattgen.rules
devicegrp=$(shell id -gn)

all: driver hotplug apps

# execute version-specific makefile
.PHONY: driver
driver:	$(loadertarget1)
	$(MAKE) -C /lib/modules/`uname -r`/build M=$(sourcedir)

$(loadertarget1): $(loadersrc1)
	cat $(loadersrc1) | sed "s/DRIVERPATH/$(localdir)\/2.6/g" | sed "s/users/$(devicegrp)/g" >$(loadertarget1)

.PHONY: apps
apps:
	$(MAKE) -C testapps

.PHONY: clean
clean:	
	rm -f $(loadertarget1)
	rm -f 2.6/*.o 2.6/*.mod.* 2.6/*.ko 2.6/.d*
	rm -fr 2.6/.tmp*
	rm -f 2.6/.[a-zA-Z]*
	$(MAKE) -C testapps clean

udev: 	driver $(loadertarget1)
	sudo $(MAKE) -C /lib/modules/`uname -r`/build M=$(sourcedir) modules_install
	sudo /sbin/depmod -a
	sudo cp $(loadertarget1) /etc/udev/rules.d/

hotplugd: driver $(loadertarget2)
	cp $(loadertarget2) /etc/hotplug.d/usb/
	chmod 744 /etc/hotplug.d/usb/t6.hotplug


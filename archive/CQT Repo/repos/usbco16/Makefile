# Makefile for the usb timestamp card.
#
# current status: first try 21.11.09chk


# directory for the driver for the local OS version
localdir=$(subst /,\/,$(PWD))
sourcedir=$(PWD)/2.6
loaderdir=hotplug
loadersrc1=$(loaderdir)/udevsrc
loadertarget1=$(loaderdir)/60-usbco16.rules
udevscript1="s/users/$(shell id -gn)/g"
udevscript2="s/DRIVERPATH/$(localdir)\/2.6/g"

all: driver $(loadertarget1)

# execute version-specific makefile
.PHONY: driver
driver:	$(loadertarget1)
	$(MAKE) -C /lib/modules/`uname -r`/build M=$(sourcedir)

$(loadertarget1): $(loadersrc1)
	sed -e $(udevscript1) -e $(udevscript2) $(loadersrc1) >$(loadertarget1)

.PHONY: apps
apps:
	$(MAKE) -C apps

.PHONY: clean
clean:	
	rm -f $(loadertarget1)
	rm -f 2.6/*.o 2.6/*.mod.* 2.6/*.ko 2.6/.d*
	rm -fr 2.6/.tmp*

udev: 	driver $(loadertarget1)
	sudo $(MAKE) -C /lib/modules/`uname -r`/build M=$(sourcedir) modules_install
	sudo /sbin/depmod -a
	sudo cp $(loadertarget1) /etc/udev/rules.d/

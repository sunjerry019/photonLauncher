/* usbpattgen1.c  - version for kernel version 2.6

   Driver module for the self-knitted USB gadget for a pattern generator.


   early driver version (usbpattgen1.c), based on  usbtimetag.c.
   Should prepare the device endpoint links, and allow a few ioctls
   to communicate with the device for initial test runs.

   first version: 4.3.07 Christian Kurtsiefer

*/

#include <linux/module.h>
#include <linux/usb.h>
#include <linux/kernel.h>
#include <asm/ioctl.h>
#include <linux/string.h>


#include "usbpattgen_io.h"    /* contains all the ioctls */


/* Module parameters*/
MODULE_AUTHOR("Christian Kurtsiefer <christian.kurtsiefer@gmail.com>");
MODULE_DESCRIPTION("Experimental driver for USB pattern generator\n");
MODULE_LICENSE("GPL");  

#define USBDEV_NAME "usbpattgen1"   /* used everywhere... */
#define USB_VENDOR_ID_CYPRESS 0x04b4
#define USB_DEVICE_ID 0x1235


/* local status variables for cards */
typedef struct cardinfo {
    int iocard_opened;
    int major;
    int minor;
    struct usb_device *dev;
    struct device *hostdev; /* roof device */
    unsigned int outpipe1; /* contains pipe ID */ 
    unsigned int inpipe1;
    unsigned int outpipe2; /* EP2 large output pipe */
    int maxpacket; /* maximum packet size for EP2 */
    struct cardinfo *next, *previous; /* for device management */

    struct urb **urblist; /* pointer to urblist */
    int errstat;           /* error status set during a callback */


    /* for debugging */
    char *dummybuf;
    int recbytes2;


    /* for proper disconnecting behaviour */
    wait_queue_head_t closingqueue; /* for the unload to wait until closed */
    int reallygone;  /* gets set to 1 just before leaving the close call */

} cdi;

static struct cardinfo *cif=NULL; /* no device registered */

/* search cardlists for a particular minor number */
static struct cardinfo *search_cardlist(int index) {
    struct cardinfo *cp;
    for (cp=cif;cp;cp=cp->next) if (cp->minor==index) break;
    return cp; /* pointer to current private device data */
}

/*************************************************************************/


/* minor device 0 (simple access) structures */
static int usbdev_flat_open(struct inode *inode, struct file *filp) {
    struct cardinfo *cp;
    int err; /* for error messages in opening */
    cp= search_cardlist(iminor(inode));
    if (!cp) return -ENODEV;
    if (cp->iocard_opened) 
	return -EBUSY;
    cp->iocard_opened = 1;
    filp->private_data = (void *)cp; /* store card info in file structure */
    /* set USB device in correct alternate mode */
   
    /* look out for usb_set_interface() function */
    err=usb_set_interface(cp->dev, 0, 1); /* select alternate setting 1 */
    if (err) return -ENODEV; /* something happened */

    /* initialize transfer engine state */
    cp->errstat=0;

    return 0;
}
static int usbdev_flat_close(struct inode *inode, struct file *filp) {
    struct cardinfo *cp = (struct cardinfo *)filp->private_data;

    cp->iocard_opened = 0;

    /* eventually tell the unloader that we are about to close */
    cp->reallygone=0;
    wake_up(&cp->closingqueue);
    /* don't know if this is necessary but just to make sure that we have
       really left this call */
    cp->reallygone=1;
    return 0;
}
static int usbdev_flat_ioctl(struct inode *inode, struct file *filp, unsigned int cmd, unsigned long arg) {
    struct cardinfo *cp = (struct cardinfo *)filp->private_data;
    unsigned char data[5]; /* send stuff */
    unsigned char len=3; unsigned char chksum=0;
    int err;
    int atrf; /* actually transferred data */
    
    if (!cp->dev) return -ENODEV;

    switch (cmd) {
	/* simple commands which send direct control urbs to the device */
	case SendDac: case PatternRAM_lseek: /* 24 bit argument */
	    data[4]=(arg>>16) & 0xff; /* 3rd byte */
	    len++; chksum+=data[4];
	case Send_RF_parameter: /* 16 bit argument */
	    data[3]=(arg>>8) & 0xff; /* MSbyte */
	    len++; chksum+=data[3];
	case Rf_Reference: case RequestStatus: /* one byte commands */
	    data[2]=arg & 0xff; /* LSbyte or only command byte */
	    len++; chksum+=data[2];
	case Reset_Pattern_unit: case InitDac: /* comands w/o argument */
	case ProgMode: case RunMode: case IdleMode:
	case ForceIdle: case ForceRun:
	    data[0]=len; chksum +=len;
	    data[1]=cmd & 0xff; chksum +=data[1];
	    data[len-1]=chksum;
	    /* just send the last significant byte to the device */
	    /* wait for 1 sec */
	    err=usb_bulk_msg(cp->dev, cp->outpipe1, data, len, &atrf, 100);
	    return err?err:atrf; /* return error number of transferred bytes */
	    break;
	case 2000: /* read inpipe1 for debugging */
	    err=usb_bulk_msg(cp->dev, cp->inpipe1, cp->dummybuf,
			     64, &atrf, 100);
	    return err?err:(cp->dummybuf[0] & 0xff);
	case 2004: /* read inpipe1 for debugging */
	    err=usb_bulk_msg(cp->dev, cp->inpipe1, data,
			     5, &atrf, 100);
	    return err?err:(cp->dummybuf[0] + 
			    (cp->dummybuf[1]<<8) +
			    (cp->dummybuf[2]<<16) +
			    (cp->dummybuf[3]<<24) );
	    break;
	case 2005: /* write out dummybuf via ep2 */
	    err=usb_bulk_msg(cp->dev, cp->outpipe2, cp->dummybuf,
			     arg, &atrf, 100);
	    return err?err:atrf;

	default:
	    return -ENOSYS; /* function not implemented */
    }
    return 0; /* went ok... */
}

/* minor device 0 (simple access) file options */
static struct file_operations usbdev_simple_fops = {
    open:    usbdev_flat_open,
    release: usbdev_flat_close,
    ioctl:   usbdev_flat_ioctl,

};


/* static structures for the class  entries for udev */
static char classname[]="pattengen%d";


/* when using the usb major device number */
static struct usb_class_driver patterngenclass = { 
    name: classname,
    fops: &usbdev_simple_fops,
    mode: S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP ,
    minor_base: 100, /* somewhat arbitrary choice... */
};


/* initialisation of the driver: getting resources etc. */
static int __init usbdev_init_one(struct usb_interface *intf, const struct usb_device_id *id ) {
    int iidx; /* index of different interfaces */
    struct usb_host_interface *setting; /* pointer to one alt setting */
    struct cardinfo *cp; /* pointer to this card */
    int found=0; /* hve found interface & setting w correct ep */
    int epi; /* end point index */
    int retval;

    /* make sure there is enough card space */
    cp = (struct cardinfo *)kmalloc(sizeof(struct cardinfo),GFP_KERNEL);
    if (!cp) {
	printk("%s: Cannot kmalloc device memory\n",USBDEV_NAME);
	return -ENOMEM;
    }

    cp->iocard_opened = 0; /* no open */

    retval=usb_register_dev(intf, &patterngenclass);
    if (retval) { /* coul not get minor */
	printk("%s: could not get minor for a device.\n",USBDEV_NAME);
	goto out2;
    }
    cp->minor = intf->minor;


    /* find device */
    for (iidx=0;iidx<intf->num_altsetting;iidx++){ /* probe interfaces */
	setting = &(intf->altsetting[iidx]);
	if (setting->desc.bNumEndpoints==3) {
	    for (epi=0;epi<3;epi++) {
		/* printk("epi: %d, ead: %d\n",epi,
		   setting->endpoint[epi].desc.bEndpointAddress); */
		switch (setting->endpoint[epi].desc.bEndpointAddress) {
		    case 1:
			found |=1; break;
		    case 129: /* the  EP1 input */
			found |=2;
			break;
		    case 2: /* the large EP2 out */
			cp->maxpacket = 
			    setting->endpoint[epi].desc.wMaxPacketSize;
			found |=4;
			break;

		}
		if (found == 7) break;
	    }
	}
    }
    if (found != 7) {/* have not found correct interface */
	printk(" did not find interface; found: %d\n",found);
	goto out1; /* no device found */
    }


    /* generate usbdevice */
    cp->dev = interface_to_usbdev(intf);
    cp->hostdev = cp->dev->bus->controller; /* for nice cleanup */

    /* construct endpoint pipes */
    cp->outpipe1 = usb_sndbulkpipe(cp->dev, 1); /* construct bulk EP1 out */
    cp->inpipe1 = usb_rcvbulkpipe(cp->dev, 129); /*  EP1 in pipe */
    cp->outpipe2 = usb_sndbulkpipe(cp->dev, 2); /* large EP2 out pipe */
    cp->dummybuf = (char *)kmalloc(1024,GFP_KERNEL);
    cp->recbytes2=0;
    printk("pipe1: %d, pipe2: %d\n",cp->outpipe1,cp->outpipe2);


    /* construct a wait queue for proper disconnect action */
    init_waitqueue_head(&cp->closingqueue);

    /* insert in list */
    cp->next=cif;cp->previous=NULL; 
    if (cif) cif->previous = cp;
    cif=cp;/* link into chain */
    usb_set_intfdata(intf, cp); /* save private data */

    return 0; /* everything is fine */
 out1:
    usb_deregister_dev(intf, &patterngenclass);
 out2:
    return -EBUSY;
}

static void __exit usbdev_remove_one(struct usb_interface *interface) {
    struct cardinfo *cp=NULL; /* to retreive card data */
    /* do the open race condition protection later on, perhaps with a
       semaphore */
    lock_kernel();  /* to prevent race condition with open */
    cp = (struct cardinfo *)usb_get_intfdata(interface);
    if (!cp) {
	printk("usbdev: Cannot find device entry \n");
	return;
    }
    /* printk("%s: try to remove card info structure at %p\n",
       USBDEV_NAME,cp); */

    /* try to find out if it is running */
    if (cp->iocard_opened) {
	printk("%s: device got unplugged while open. How messy.....\n",
	       USBDEV_NAME);

	/* ... and now we hope that someone realizes that we took away the
	   memory and closes the device */
	wait_event(cp->closingqueue, !(cp->iocard_opened));
	/* really don't know if this is necessary, or if wakeup comes late
	   enough */
	while (!cp->reallygone) schedule(); /* wait until it is set */
    }

    /* remove from local device list */
    if (cp->previous) { 
	cp->previous->next = cp->next;
    } else {
	cif=cp->next;
    }
    if (cp->next) cp->next->previous = cp->previous;
    /* printk("%s: next/previous entry: %p / %p, cif: %p\n",
       USBDEV_NAME, cp->next, cp->previous, cif);  */

    /* mark interface as dead */
    usb_set_intfdata(interface, NULL);
    usb_deregister_dev(interface, &patterngenclass);

    unlock_kernel();

    kfree(cp->dummybuf);
    kfree(cp); /* give back card data container structure */
    
}

/* driver description info for registration; more details?  */

static struct usb_device_id usbdev_tbl[] = {
    {USB_DEVICE(USB_VENDOR_ID_CYPRESS, USB_DEVICE_ID)},
    {},
};

MODULE_DEVICE_TABLE(usb, usbdev_tbl);

static struct usb_driver usbdev_driver = { 
    .owner =     THIS_MODULE,
    .name =      USBDEV_NAME, /* "usbdev-driver", */
    .id_table =  usbdev_tbl,
    .probe =     usbdev_init_one,
    .disconnect =    usbdev_remove_one,
};

static void  __exit usbdev_clean(void) {
    usb_deregister( &usbdev_driver );
}

static int __init usbdev_init(void) {
    int rc;
    cif=NULL;
    rc = usb_register( &usbdev_driver );
    if (rc) 
	err("%s: usb_register failed. Err: %d",USBDEV_NAME,rc);
    return rc;
}

module_init(usbdev_init);
module_exit(usbdev_clean);

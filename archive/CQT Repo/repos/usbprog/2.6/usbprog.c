/* usbprog.c   -  USB device driver for an atmel/jtag/swd programmer

  Copyright (C) 2010,2011 Christian Kurtsiefer <christian.kurtsiefer@gmail.com>


  This driver provides a simple interface to the control commands passed onto
  the device via the EP1 interface.

  The driver provides a character device node. EP1 commands (see "usbprog_io.h"
  for a detailed explanation) are implemented with ioctl() calls.

  Some of the JTAG commands require more than one parameter; see description
  below.



  status: 19.09.10chk  first code
          30.10.10chk  taking in jtag commands
	  30.01.11chk  swd commands start to work

*/

#include <linux/module.h>
#include <linux/usb.h>
#include <linux/kernel.h>
#include <asm/ioctl.h>
#include <linux/string.h>
#include <asm/uaccess.h>
#include <linux/mm.h>
#include <asm/fcntl.h>
#include <linux/version.h>
#include <asm/errno.h>
#include <linux/slab.h>


#include "usbprog_io.h"    /* contains all the ioctls */

/* driver version; for encoding see usbdds_io.h file */
#define driver_version 0x00010000

/* dirty fixes for broken usb_driver definitions */
#if (LINUX_VERSION_CODE > KERNEL_VERSION(2,6,11) )
#define HAS_NO_OWNER so_sad
#define HAS_NO_DEVFS_MODE
#endif

/* Module parameters*/
MODULE_AUTHOR("Christian Kurtsiefer <christian.kurtsiefer@gmail.com>");
MODULE_DESCRIPTION("Experimental driver for a atmel/jtag/swd programmer\n");
MODULE_LICENSE("GPL");  

#define USBDEV_NAME "usbprog"   /* used everywhere... */
#define USB_VENDOR_ID_CYPRESS 0x04b4
#define USB_DEVICE_ID 0x1239

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



/* generic control routine to pass an argument to the USB unit */
int send_control_command(struct cardinfo *cp, int cmd, 
			 unsigned long arg) {
    unsigned char data[6]; /* for sending stuff */
    unsigned char len=3; unsigned char chksum=0;
    int err;
    int atrf; /* actually transferred data */

    if (!cp->dev) return -ENODEV;
    switch (cmd) {
         /* simple commands which send direct control urbs to the device */
        case Send_Word: /* 32 bit argument (and retreive response) */
	    data[5]=(arg>>24) & 0xff; len++; chksum+=data[5];
	/* three byte commands */
        case JTAG_forcestate:
        case JTAG_runstate:  /* second arg is a 16 bit cycle number, contained
			        in bits 23:8 of the argument */
	    data[4]=(arg>>16) & 0xff; len++; chksum+=data[4];
	/* 16 bit data */
        case SWD_Sendword:
	    data[3]=(arg>>8) & 0xff; /* MSbyte */
	    len++; chksum+=data[3];
	    // printk(" two/three byte command: cmd: %d, arg: %06x\n",cmd& 0xff, arg);
	/* one byte commands */
        case Set_Delay:
        case JTAG_ENDDR: /* argument is between 0 and 3, otherwise error */
        case JTAG_ENDIR: /* argument is between 0 and 3, otherwise error */
        case JTAG_setTRST: /* one byte argument, info is contained in LSB */
        case SWD_Reset:
	    data[2]=arg & 0xff; /* LSbyte or only command byte */
	    //printk(" one byte command: cmd: %d, arg: %d\n",cmd, arg);
	    len++; chksum+=data[2];
	/* comands w/o argument */
        case Reset_Target: case Unreset_Target:
        case JTAG_initialize:
        case 254:  /* erase flash command */
	    data[0]=len; chksum +=len;
	    data[1]=cmd & 0xff; chksum +=data[1];
	    data[len-1]=chksum;
	    /* wait for 1 sec */
	    err=usb_bulk_msg(cp->dev, cp->outpipe1, data, len, &atrf, 1*HZ);
	    //printk("retval: %d\n",err);
	    return err; /* return error number or 0 if ok*/
    }
    return -ENOSYS; /* default */

}

/* -----------------------------------------------------------------*/
/* basic methods for communicating with the device */

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
    if (err) {
	cp->iocard_opened = 0;
	return -ENODEV; /* something happened */
    }

    /* initialize transfer engine state */
    cp->errstat=0;

    return 0;
}
static int usbdev_flat_close(struct inode *inode, struct file *filp) {
    struct cardinfo *cp = (struct cardinfo *)filp->private_data;

    /* set unit into run mode if we were not in O_RDONLY */
    if (filp->f_flags & O_ACCMODE);

    cp->iocard_opened = 0;

    /* eventually tell the unloader that we are about to close */
    cp->reallygone=0;
    wake_up(&cp->closingqueue);
    /* don't know if this is necessary but just to make sure that we have
       really left this call */
    cp->reallygone=1;
    return 0;
}
#define MAXCHAINBYTES 50
typedef struct bit_chain {
  int length; 
  char content[MAXCHAINBYTES];
} bitchain;


static long usbdev_flat_ioctl(struct file *filp,
			     unsigned int cmd, unsigned long arg) {
    struct cardinfo *cp = (struct cardinfo *)filp->private_data;
    int err;
    int atrf; /* actually transferred data */
    char *data = cp->dummybuf;
    unsigned char chksum;
    int i;
    struct bit_chain *arg2;
    char *arg3= (char *) arg;
    int length=0;
    int totalpayload, thispayload, headersize, dataoffset, copybytes; 

    if (!cp->dev) return -ENODEV;

    /* take care of data sending / receiving commands separately */
    if ((cmd == JTAG_scandata) || (cmd == JTAG_scanIR)) {
      /* we need to extract data from bit stream */
      arg2=(struct bit_chain *)arg; /* interpret as pointer */
      i=copy_from_user(&length, &arg2->length, sizeof(int));
      if (i) return -ENOMEM;
      /* check if command has valid length first */
      if (length> 20000) { /* no, we have too many bits */
	return -E2BIG;
      }

      /* now we need to loop through a number of packets */
      totalpayload = (length+7)/8+1; /* this is in bytes, data+checksum */
      data[1] = cmd & 0xff; /* command is first byte */
      data[2] = length & 0xff;
      data[3] = (length>>8) & 0xff;
      dataoffset=0; headersize=4; chksum=0; /* values for first block */
      /* now we loop through all blocks */
      do {
	thispayload = totalpayload<64-headersize?
	  totalpayload:
	  64-headersize; /* may include cksm */
	data[0]=thispayload+headersize; /* how many bytes to send */
        /* calculate real bytes to copy from users */ 
	copybytes=thispayload; 
	if (totalpayload<65-headersize) copybytes--; /* we need to add chksum */
	
	if (copy_from_user(&data[headersize], 
			   &arg2->content[dataoffset], 
			   copybytes)) return -ENOMEM;
	dataoffset+=copybytes;
	
        /* calculate checksum */
        for (i=1; i<copybytes+headersize; i++) chksum += data[i];
        /* do we need to add the checksum? */
        if (totalpayload<65-headersize) data[data[0]-1]=chksum;	  

	/* send stuff */
	//printk(" (send) collateral info: thispayload: %d, totalpayload: %d, ofs: %d\n"	 thispayload, totalpayload, dataoffset);
	//  for (i=0; i<8; i++) printk(" %02x",data[i]);
	//  printk("\n");

	err=usb_bulk_msg(cp->dev, cp->outpipe1, data, data[0], &atrf, 1*HZ);
	if (err) return err;
	totalpayload -= thispayload;
	headersize=1; /* for subsequent packages if needed */
      } while (totalpayload>0);
      
      /* retreive respond */
      totalpayload = (length+7)/8; /* this is in bytes, only data */
      dataoffset=0;
      do {
	thispayload=(totalpayload<64?totalpayload:64);
	//printk(" before read: totalpayload: %d, thispayload: %d\n",	       totalpayload, thispayload);
	err=usb_bulk_msg(cp->dev, cp->inpipe1, &data[dataoffset],
			 64, &atrf, 1*HZ);
	if (err) {
	  printk("usbprog error @1; cmd: %d\n",cmd);
	  printk(" (receive) collateral info: thispayload: %d, totalpayload: %d, ofs: %d, err: %d\n",
		 thispayload, totalpayload, dataoffset, err);
	  for (i=0; i<8; i++) printk(" %02x",data[i]);
	  printk("\n");

	  return err;
	}
	if (atrf>64) return -ENOMEM;
	dataoffset +=atrf;
	totalpayload -= atrf;
      } while (totalpayload>0);
      
      if (copy_to_user(arg2->content, data, dataoffset)) return -ENOMEM;
      return 0; /* everything went ok */
      
    }


    /* treatment of the SWD commands which return stuff */
    if (cmd == SWD_Write || cmd == SWD_Read || cmd == SWD_Acquire) {
      /* prepare data to be transmitted */
      chksum=0;
      length= (cmd==SWD_Write)?5:1; /* bytes to transfer */
      if (copy_from_user(&data[2],arg3,length)) return -ENOMEM;
      for (i=0;i<length;i++) chksum += data[2+i];
      
      data[1] = cmd & 0xff ; chksum +=data[1]; /* command */
      data[0] = length+3; data[length+2]=chksum & 0xff;

      /* send out usb command */
      err=usb_bulk_msg(cp->dev, cp->outpipe1, data, data[0], &atrf, 1*HZ);
      if (err) return err;

      /* pick up reponse */
      err=usb_bulk_msg(cp->dev, cp->inpipe1, data,
		       64, &atrf, 1*HZ);
      if (err) return err;

      if (atrf>5) return -ENOMEM;

      if (copy_to_user(arg3, data, atrf)) return -ENOMEM;
      return 0; /* everything went ok */

    }

    err = send_control_command(cp,cmd,arg); /* send cmd */
    if (err) return err;

    /* command with reaback */
    if (cmd == Send_Word ) {
 	/* collect response */
	err=usb_bulk_msg(cp->dev, cp->inpipe1, cp->dummybuf,
			 5, &atrf, 1*HZ);

	return err?err:((unsigned char)cp->dummybuf[0] + 
			((unsigned char)cp->dummybuf[1]<<8) +
			((unsigned char)cp->dummybuf[2]<<16) +
			((unsigned char)cp->dummybuf[3]<<24) );
    }
	    
    /* core ioctl commands */
    return 0;
}



/* minor device 0 (simple access) file options */
static struct file_operations usbdev_simple_fops = {
    open:    usbdev_flat_open,
    release: usbdev_flat_close,
    unlocked_ioctl:   usbdev_flat_ioctl,
};


/* static structures for the class  entries for udev */
static char classname[]="usbprog%d";


/* when using the usb major device number */
static struct usb_class_driver atmelprogclass = { 
    name: classname,
    fops: &usbdev_simple_fops,
#ifndef HAS_NO_DEVFS_MODE
    mode: S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP ,
#endif
    minor_base: 100, /* somewhat arbitrary choice... */
};


/* initialisation of the driver: getting resources etc. */
static int usbdev_init_one(struct usb_interface *intf, const struct usb_device_id *id ) {
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

    retval=usb_register_dev(intf, &atmelprogclass);
    if (retval) { /* coul not get minor */
	printk("%s: could not get minor for a device.\n",USBDEV_NAME);
	goto out2;
    }
    cp->minor = intf->minor;


    /* find device */
    for (iidx=0;iidx<intf->num_altsetting;iidx++){ /* probe interfaces */
	setting = &(intf->altsetting[iidx]);
	if (setting->desc.bNumEndpoints==2) {
	    for (epi=0;epi<2;epi++) {
		/* printk("epi: %d, ead: %d\n",epi,
		   setting->endpoint[epi].desc.bEndpointAddress); */
		switch (setting->endpoint[epi].desc.bEndpointAddress) {
		    case 1:
			found |=1; break;
		    case 129: /* the  EP1 input */
			found |=2;
			break;
		}
		if (found == 3) break;
	    }
	}
    }
    if (found != 3) {/* have not found correct interface */
	printk(" did not find interface; found: %d\n",found);
	goto out1; /* no device found */
    }


    /* generate usbdevice */
    cp->dev = interface_to_usbdev(intf);
    cp->hostdev = cp->dev->bus->controller; /* for nice cleanup */

    /* construct endpoint pipes */
    cp->outpipe1 = usb_sndbulkpipe(cp->dev, 1); /* construct bulk EP1 out */
    cp->inpipe1 = usb_rcvbulkpipe(cp->dev, 129); /*  EP1 in pipe */
    cp->dummybuf = (char *)kmalloc(1024,GFP_KERNEL);
    cp->recbytes2=0;

    /* construct a wait queue for proper disconnect action */
    init_waitqueue_head(&cp->closingqueue);

    /* insert in list */
    cp->next=cif;cp->previous=NULL; 
    if (cif) cif->previous = cp;
    cif=cp;/* link into chain */
    usb_set_intfdata(intf, cp); /* save private data */

    return 0; /* everything is fine */
 out1:
    usb_deregister_dev(intf, &atmelprogclass);
 out2:
    return -EBUSY;
}

static void usbdev_remove_one(struct usb_interface *interface) {
    struct cardinfo *cp=NULL; /* to retreive card data */
    /* do the open race condition protection later on, perhaps with a
       semaphore */
    cp = (struct cardinfo *)usb_get_intfdata(interface);
    if (!cp) {
	printk("usbdev: Cannot find device entry \n");
	return;
    }

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

    /* mark interface as dead */
    usb_set_intfdata(interface, NULL);
    usb_deregister_dev(interface, &atmelprogclass);

    kfree(cp->dummybuf);
    kfree(cp); /* give back card data container structure */
    
}

/* driver description info for registration; more details?  */

static struct usb_device_id usbdev_tbl[] = {
    {USB_DEVICE(USB_VENDOR_ID_CYPRESS, USB_DEVICE_ID)},
    {}
};

MODULE_DEVICE_TABLE(usb, usbdev_tbl);

static struct usb_driver usbdev_driver = { 
#ifndef HAS_NO_OWNER
    .owner =     THIS_MODULE,
#endif
    .name =      USBDEV_NAME,
    .id_table =  usbdev_tbl,
    .probe =     usbdev_init_one,
    .disconnect =    usbdev_remove_one,
};

static void  __exit usbdev_clean(void) {
    usb_deregister( &usbdev_driver );
}

static int __init usbdev_init(void) {
    int rc;
    cif=NULL; // can we really call this?
    rc = usb_register( &usbdev_driver );

    if (rc) 
	pr_err("%s: usb_register failed. Err: %d",USBDEV_NAME,rc);
    return rc;
}

module_init(usbdev_init);
module_exit(usbdev_clean);

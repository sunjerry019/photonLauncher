/* structure that stores contains known devices. 
   some of the info can be found in "Using Flash memory and Hadened Control
   Functions in MACXO2 Devices Reference Guide", page 63
*/

#include <stdio.h>
#include "deviceprops.h"

struct deviceproperties descr_XO2_1200HC = {
 dname:       "XO2-1200HC",
 cfgsize:    278400,
 fusenumber: 343936,
 ebits:      80,
 ubits:      32,
 idcode:     0x012ba043
};

/* this is incomplete and wrong!! */
struct deviceproperties descr_XO2_1200U = {
 dname:       "XO2-1200U",
 cfgsize:    100000,
 fusenumber: 300000,
 ebits:      80,
 ubits:      32,
 idcode:     0x12345678 // dummy
};

struct deviceproperties * devlist[] = {
    &descr_XO2_1200HC,
    &descr_XO2_1200U,
    NULL
};

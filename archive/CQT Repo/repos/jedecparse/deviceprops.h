/* structure that stores known devices. */

#include <stdint.h>

typedef struct deviceproperties {
    char dname[20];
    int cfgsize;
    int fusenumber;
    int ebits;
    int ubits;
    uint32_t idcode;
} dev_prop;


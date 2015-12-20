CC=gcc
CFLAGS=-Wall -Wextra -lm -L. -lftd2xx -Wl,-rpath /usr/local/lib

APP = synthusb

all: $(APP)

$(APP): synthusb.c	
	$(CC) synthusb.c -o $(APP) $(CFLAGS)
	
clean:
	rm -f *.o ; rm $(APP) ; rm *~

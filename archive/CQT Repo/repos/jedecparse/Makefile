all: jedecparse jedecprog

jedecparse: jedecparse.c
	gcc -Wall -O3 -o jedecparse jedecparse.c

jedecprog: jedecprog.c deviceparameters.c jtag_components.c 
	gcc -Wall -O3 -lm -o jedecprog deviceparameters.c jtag_components.c jedecprog.c

clean:
	rm -f jedecparse
	rm -f jedecprog

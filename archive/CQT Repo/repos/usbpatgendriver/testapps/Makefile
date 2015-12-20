all: tpg1 tpg2 makepatt simplepattern usbdacset usbrfgenset usbdacsetmillivolt newpatgen newrfgenset newpatgen_setmode

tpg1: tpg1.c
	gcc -Wall -O3 -o tpg1 tpg1.c

tpg2: tpg2.c
	gcc -Wall -O3 -o tpg2 tpg2.c

makepatt: makepatt.c
	gcc -Wall -O3 -o makepatt makepatt.c

simplepattern: simplepattern.c
	gcc -Wall -O3 -o simplepattern simplepattern.c

usbdacset: usbdacset.c
	gcc -Wall -O3 -o usbdacset usbdacset.c

usbdacsetmillivolt: usbdacsetmillivolt.c
	gcc -Wall -O3 -o usbdacsetmillivolt usbdacsetmillivolt.c

usbrfgenset: usbrfgenset.c
	gcc -Wall -O3 -o usbrfgenset usbrfgenset.c

newpatgen: newpatgen.c
	gcc -Wall -O3 -o newpatgen newpatgen.c

newrfgenset: newrfgenset.c
	gcc -Wall -O3 -o newrfgenset newrfgenset.c

newpatgen_setmode: newpatgen_setmode.c
	gcc -Wall -O3 -o newpatgen_setmode newpatgen_setmode.c

clean:
	rm -f tpg[12]
	rm -f *~
	rm -f makepatt
	rm -f simplepattern
	rm -f usbdacset
	rm -f usbdacsetmillivolt
	rm -f usbrfgenset
	rm -f newpatgen
	rm -f newrfgenset
	rm -f newpatgen_setmode

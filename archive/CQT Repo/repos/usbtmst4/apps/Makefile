all: jtagprg playclock powerplay clearflash playadc testfpga1 testfpga2

clearflash: clearflash.c
	gcc -Wall -O3 -o clearflash clearflash.c

playclock: playclock.c timestampcontrol.h
	gcc -Wall -O3 -o playclock playclock.c

playadc: playadc.c
	gcc -Wall -O3 -o playadc playadc.c

jtagprg: jtagprg.c usbprog_io.h
	gcc -Wall -lm -O3 -o jtagprg jtagprg.c

powerplay: powerplay.c timestampcontrol.h
	gcc -Wall -O3 -o powerplay powerplay.c

testfpga1: testfpga1.c timestampcontrol.h
	gcc -Wall -O3 -o testfpga1 testfpga1.c

testfpga2: testfpga2.c timestampcontrol.h
	gcc -Wall -O3 -o testfpga2 testfpga2.c

clean: 
	rm -f jtagprg
	rm -f playclock
	rm -f playadc
	rm -f clearflash
	rm -f powerplay
	rm -f testfpga1
	rm -f testfpga2
	rm -f *~

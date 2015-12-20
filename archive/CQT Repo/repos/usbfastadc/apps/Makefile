all:jtagprg playclock playcpld showrdy fulltest reset_unit osci1 osci2 clearflash osci3 streamread qrngread

clearflash: clearflash.c
	gcc -Wall -O3 -o clearflash clearflash.c

osci3: osci3a.c
	gcc -Wall -O3 -o osci3 osci3a.c

osci2: osci2.c
	gcc -Wall -O3 -o osci2 osci2.c

osci1: osci1.c
	gcc -Wall -O3 -o osci1 osci1.c

reset_unit: reset_unit.c
	gcc -Wall -O3 -o reset_unit reset_unit.c

fulltest: fulltest.c
	gcc -Wall -O3 -o fulltest fulltest.c

showrdy: showrdy.c
	gcc -Wall -O3 -o showrdy showrdy.c

playclock: playclock.c
	gcc -Wall -O3 -o playclock playclock.c

playcpld: playcpld.c
	gcc -Wall -O3 -o playcpld playcpld.c

jtagprg: jtagprg.c usbprog_io.h
	gcc -Wall -lm -O3 -o jtagprg jtagprg.c

streamread: streamread.c
	gcc -Wall -O3 -o streamread streamread.c

qrngread: qrngread.c
	gcc -Wall -O3 -o qrngread qrngread.c

clean: 
	rm -f jtagprg
	rm -f playclock
	rm -f playcpld
	rm -f showrdy
	rm -f fulltest
	rm -f reset_unit
	rm -f osci1
	rm -f osci2
	rm -f osci3
	rm -f streamread
	rm -f qrngread
	rm -f *~

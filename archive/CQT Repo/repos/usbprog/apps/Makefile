all: atmtest clear_dds_flash jtagprg psocprog psoc_to_jtag psocprog_own psocfix

psc_to_jtag: psoc_to_jtag.c
	gcc -Wall -O3 -o psoc_to_jtag psoc_to_jtag.c

pscprog: psocprog.c
	gcc -Wall -O3 -o psocprog psocprog.c

pscprog_own: psocprog_own.c
	gcc -Wall -O3 -o psocprog_own psocprog_own.c

atmtest: atmtest.c usbprog_io.h
	gcc -Wall  -O3 -o atmtest atmtest.c

clear_dds_flash: clear_dds_flash.c usbprog_io.h
	gcc -Wall  -O3 -o clear_dds_flash clear_dds_flash.c

jtagprg: jtagprg.c usbprog_io.h
	gcc -Wall -lm -O3 -o jtagprg jtagprg.c

psocfix: psocfix.c
	gcc -Wall -O3 -o psocfix psocfix.c

clean: 
	rm -f psoc_to_jtag
	rm -f psocprog
	rm -f psocprog_own
	rm -f atmtest
	rm -f jtagprg
	rm -f clear_dds_flash
	rm -f psocfix
	rm -f *~

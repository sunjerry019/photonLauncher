all: reset_dds t3 dds_encode sweep_test clear_dds_flash setclock

setclock: setclock.c
	gcc -Wall -O3 -o setclock setclock.c

reset_dds: reset_dds.c
	gcc -Wall -O3 -o reset_dds reset_dds.c

t3: t3.c
	gcc -Wall -O3 -o t3 t3.c

dds_encode: dds_encode.c
	gcc -Wall -lm -O3 -o dds_encode dds_encode.c

sweep_test: sweep_test.c
	gcc -Wall  -O3 -lm -o sweep_test sweep_test.c

clear_dds_flash: clear_dds_flash.c
	gcc -Wall  -O3 -o clear_dds_flash clear_dds_flash.c


clean: 
	rm -f clear_dds_flash
	rm -f reset_dds
	rm -f t3
	rm -f dds_encode
	rm -f sweep_test
	rm -f *~

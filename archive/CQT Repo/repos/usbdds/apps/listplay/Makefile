all: ltt chirp testlist

ltt: ltt.c
	gcc -Wall -O3 -o ltt ltt.c

chirp: chirp.c
	gcc -Wall -O3 -lm -o chirp chirp.c

testlist: testlist.c
	gcc -Wall -O3 -lm -o testlist testlist.c

clean:
	rm -f ltt
	rm -f chirp
	rm -f testlist

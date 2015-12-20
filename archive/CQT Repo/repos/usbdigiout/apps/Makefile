all: settimer sendpatt pattgen

settimer: settimer.c
	gcc -Wall -O3 -o settimer settimer.c

sendpatt: sendpatt.c
	gcc -Wall -O3 -o sendpatt sendpatt.c

pattgen: pattgen.c
	gcc -Wall -O3 -o pattgen pattgen.c

.PHONY: clean
clean:
	rm -f settimer
	rm -f sendpatt
	rm -f pattgen
	rm -f *~

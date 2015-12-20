all:	getrate

getrate: getrate.c
	gcc -O3 -Wall -o getrate getrate.c


.PHONY:	clean
clean:
	rm -f *~
	rm -f getrate
	rm -f cntlogpipe
	rm -f rawevents
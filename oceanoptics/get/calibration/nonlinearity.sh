#!/usr/bin/env bash

for INT in {10..500..10}
do
    echo "$INT ms Integration Time"
	../livespec.py 1000 -t $INT -d "$INT ms Integration Time - Bright" -p
done

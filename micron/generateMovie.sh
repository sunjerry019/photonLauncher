#!/bin/bash

ffmpeg -f image2 -r 120 -i "./results/test-%01d.png" -vcodec mpeg4 -y "./videos/test.mp4"
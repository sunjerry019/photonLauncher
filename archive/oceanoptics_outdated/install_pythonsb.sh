#!/bin/bash

OS="unknown";
platform=$(python -mplatform);

if [[ grep $platform ARCH | wc -mt 0]]; then
    $OS="arch"
elif [[ condition ]]; then
    #statements
fi

echo $OS

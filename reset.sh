#!/bin/bash

if [ -e data ]; then
    mv data data.$(date --utc +%Y-%m-%d-%H:%M:%S)
fi
mkdir data

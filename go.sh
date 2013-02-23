#!/bin/bash

if [ ! -e "data/dockets.csv" ]; then
    python fetch/scrapedockets.py 1 > data/dockets.csv
    cat data/dockets.csv | csvcut -c 2 | sed -e 's,$,/,' > data/urls.txt
fi

if [ ! -e "data" ]; then
    mkdir data
fi



downloaded_line=$(egrep ^Downloaded: data/wget.log)
if [ ! -e "data/wget.log" -o -n "$downloaded_line" ]; then
    cd data
    wget -e robots=off --no-host-directories --no-parent --recursive --cut-dirs=2 -l 1 --no-clobber -o ../data/wget.log -i ../data/urls.txt
    cd ..
fi

find data/ -name '*.pdf' -print0 | xargs -0 -- convert/pdf2pgm_multi
find data/ -name '*.pgm' -print0 | xargs -0 -- convert/pgm2txt_multi


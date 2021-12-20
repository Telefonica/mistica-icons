#!/bin/bash

# get path from command line
MYWD=$1

for file in *.svg
do
  echo $file $MYWD
  cat "$file" | inkscape --pipe --export-filename="${file%%.*}.pdf"
done
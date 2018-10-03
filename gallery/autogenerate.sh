#!/bin/bash

./Photon-0.4.6/photon -v -d 5 -t 100x75  -k mae_web src

cat photos/index.html | sed -e 's/"..\/index.html/"..\/..\/index.html/g' |sed -e 's/..\/images/images/g'|sed -e 's/Family_and_Friends\/index.html/index.html/g'> photos/index.html.tmp
mv photos/index.html.tmp photos/index.html

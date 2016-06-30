#!/bin/bash

path="./bipartite/"

for year in {2011..2016} ;
do
	echo "Create Gif for year: $year"
	convert "$path/$year/"*.png -delay 1 -loop 1 animation-$year.gif
done


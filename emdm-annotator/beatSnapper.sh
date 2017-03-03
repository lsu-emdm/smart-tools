#!/bin/sh

# Beat Tracker

echo "____Beat Tracking____"


if [ "$2" = "csv" ]
then
	sonic-annotator -t transforms/beatSnap.n3 $1 -w csv --csv-stdout > outputFiles/beats.csv
else
	sonic-annotator -t transforms/beatSnap.n3 $1 -w jams --jams-stdout > outputFiles/beats.json
fi




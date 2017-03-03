#!/bin/sh

# Beat Tracker
# arguments: beatSnappier.sh [ filename (csv) ]
# beatSnappier incorporates creating the skeleton file as a tmp file before running the transform.

echo "____Beat Tracking____"

sonic-annotator -s vamp:qm-vamp-plugins:qm-tempotracker:beats > transforms/beatSnap.tmp

if [ "$2" = "csv" ]
then
	sonic-annotator -t transforms/beatSnap.tmp $1 -w csv --csv-stdout > outputFiles/beats.csv
else
	sonic-annotator -t transforms/beatSnap.tmp $1 -w jams --jams-stdout > outputFiles/beats.json
fi

rm transforms/beatSnap.tmp


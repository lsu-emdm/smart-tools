#!/bin/sh

echo $1
echo "::::::"
echo $2

# sonic-annotator -t transforms/audioNotes.n3 ../audioSamples/WhitneyAnthem.mp3 -w jams --jams-stdout > outputFiles/whitNotes.json


if [ "$2" = "csv" ] 
then
	echo $2
	sonic-annotator -t transforms/audioNotes.n3 "$1" -w csv --csv-stdout > outputFiles/notes.csv
	
else
	sonic-annotator -t transforms/audioNotes.n3 "$1" -w jams --jams-stdout > outputFiles/notes.json
fi



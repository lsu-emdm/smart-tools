#!/bin/sh
# Whitney melodia extraction
#
# with optional argument to read in a different file than the WhitneyAnthem.
# the output file name is generated based on the input file name.

echo $1

# sonic-annotator -t transforms/melodia_melody.n3 audioSamples/WhitneyAnthem.mp3 -w jams --jams-basedir outputFiles/ --jams-force



if [ -z "$1" ]
then
	sonic-annotator -t transforms/melodia_melody.n3 audioSamples/WhitneyAnthem.mp3 -w jams --jams-basedir outputFiles/ --jams-force
else
	sonic-annotator -t transforms/melodia_melody.n3 $1 -w jams --jams-basedir outputFiles/ --jams-force
	echo "Working on file"
fi


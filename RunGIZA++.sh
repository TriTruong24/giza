#!/bin/bash
if [ $# -ne 4 ]
then
  echo "Add parameter !"
  exit -1
fi

FOLDER=$1
SOURCE_FILE=$2
TARGET_FILE=$3
OUTPUT_FOLDER=$4

cd /content/giza-pp/GIZA++-v2
./plain2snt.out $FOLDER"/"$SOURCE_FILE $FOLDER"/"$TARGET_FILE
echo "Finished plain2snt source target"
cd /content/giza-pp/mkcls-v2
./mkcls -p$FOLDER"/"$SOURCE_FILE -V$FOLDER"/"$SOURCE_FILE.vcb.classes
echo "Finished mkcls source source"
./mkcls -p$FOLDER"/"$TARGET_FILE -V$FOLDER"/"$TARGET_FILE.vcb.classes
echo "Finished mkcls target target"
cd /content/giza-pp/GIZA++-v2
./snt2cooc.out $FOLDER"/"$SOURCE_FILE.vcb $FOLDER"/"$TARGET_FILE.vcb $FOLDER"/"$SOURCE_FILE"_"$TARGET_FILE.snt > $FOLDER"/"$SOURCE_FILE"_"$TARGET_FILE.cooc
./GIZA++ -S $FOLDER"/"$SOURCE_FILE.vcb -T $FOLDER"/"$TARGET_FILE.vcb -C $FOLDER"/"$SOURCE_FILE"_"$TARGET_FILE.snt -CoocurrenceFile $FOLDER"/"$SOURCE_FILE"_"$TARGET_FILE.cooc -o result -outputpath $OUTPUT_FOLDER


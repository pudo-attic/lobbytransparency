#!/bin/bash

TS=`date +"%Y-%m-%d"`
CACHE="/tmp/eutr-$TS"
echo $CACHE
mkdir -p $CACHE
if [ ! -e $CACHE/ir.xml ]
then
  curl -o $CACHE/ir.xml "http://ec.europa.eu/transparencyregister/public/consultation/statistics.do?action=getLobbyistsXml&fileType=NEW"
fi
if [ ! -e $CACHE/ap.xml ]
then
  curl -o $CACHE/ap.xml "http://ec.europa.eu/transparencyregister/public/consultation/statistics.do?action=getLobbyistsXml&fileType=ACCREDITED_PERSONS"
fi

python run.py $CACHE/ir.xml $CACHE/ap.xml
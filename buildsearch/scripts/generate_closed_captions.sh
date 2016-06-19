#!/bin/sh

VIDEO_DIR="/path-to-webapps-base/video"
DOWNLOAD_DIR="/path-to-webapps-base/captions"
LOGFILE="runlog.txt"
AMI_DIR="/path-to-azure-media-indexer-java"
LISTFILE="videoslist.txt"

cd $AMI_DIR
{
for i in `cat $LISTFILE | sed s/.mp4//g`
do
    echo "Start executing $i "
    mvn exec:java -Dexec.args="-a $i -c ./app.config -f $VIDEO_DIR/$i.mp4 -p ./default-ami.config -o $DOWNLOAD_DIR"
    
done
} 2>&1 | tee $LOGFILE

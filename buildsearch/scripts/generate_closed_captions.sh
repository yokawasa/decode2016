#!/bin/sh

VIDEO_DIR="/data1/worksdata/build2016/video"
DOWNLOAD_DIR="/data1/worksdata/build2016/captions/new"
LOGFILE="/data1/worksdata/build2016/captions/new/runlog.txt"
AMI_DIR="/home/yoichika/dev/github/azure-media-indexer-java.test"
LISTFILE="/home/yoichika/dev/tests/azure/search/decode/build2016/work/nottmlmp4list.txt"

cd $AMI_DIR
{
for i in `cat $LISTFILE | sed s/.mp4//g`
do
    echo "Start executing $i "
    mvn exec:java -Dexec.args="-a $i -c ./app.config -f $VIDEO_DIR/$i.mp4 -p ./default-ami.config -o $DOWNLOAD_DIR"
    
done
} 2>&1 | tee $LOGFILE

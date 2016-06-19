#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import commands
import os.path

caption_uploader = 'upload_cation.py'


def getsessionname(url):
    arr=url.split('/')
    return arr[len(arr)-1]

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    if (argc != 4):
        print 'Usage: # python %s <csvfile> <caption_data_dir> <indexname>' % argvs[0]
        quit()
   
    csvfile = argvs[1];
    capdir = argvs[2];
    indexname = argvs[3];

    import csv
    with open(csvfile, 'r') as f:
        reader = csv.reader(f)
        next(reader)   # skip header
        # title,speakers,description,link,video,thumbnail
        for row in reader:
            link = row[3]
            mp4file = row[4]
            sessionid = getsessionname(link)
            ttmlfile = "{0}/{1}.ttml".format(capdir,mp4file)
            # execute caption update only if ttmlfile exists
            if not os.path.exists(ttmlfile):
                print 'file[%s] does not exist' % ttmlfile
                continue
            cmd = "{0} {1} {2} {3}".format(caption_uploader,ttmlfile, sessionid, indexname)
            print cmd
            cmdout = commands.getoutput(cmd)
            print cmdout

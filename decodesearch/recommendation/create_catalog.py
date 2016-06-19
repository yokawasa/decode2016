#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def gettrackname(s):
    # N.trackname -> trackname
    arr=s.split('.')
    return arr[len(arr)-1]

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    if (argc != 3):
        print 'Usage: # python %s <csvfile> <ouput_catalog_file>' % argvs[0]
        quit()
   
    csvfile = argvs[1];
    catfile = argvs[2];

    cf = open(catfile,"w")
    import csv
    with open(csvfile, 'r') as f:
        reader = csv.reader(f)
        next(reader)   # skip header
        # title,speakers,description,link,video,thumbnail
        for row in reader:
            sessionid=row[22]
            title=row[0].decode('utf8')
            track = gettrackname(row[2])
            line = "{0},{1},{2}".format(sessionid,title.encode('utf8'),track)
            cf.write(line)
            cf.write("\n")
    cf.close

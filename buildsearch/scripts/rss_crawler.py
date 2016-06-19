#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import csv
import feedparser
import urllib
import sys
import re

FEEDURL='https://s.ch9.ms/Events/Build/2016/RSS'
CSV_FILENAME='build2016.csv'

def usage_quit(c):
    print 'Usage: # python %s <outputdir> [-skip|--skip]' % c
    print ''
    print '   <outputdir>:  output directory where event csv, video filename list, video files are store'
    print '   -skip|--skip: skip downloading video files'
    quit()

def empty(v):
    return False if ( v and not v.isspace() ) else True

def getvideofilename(title):
#    return "{0}.mp4".format(re.sub(r'[ :]+', '_', title))
    return "{0}.mp4".format(re.sub(r'[ :+#]+', '_', title))

def download(url,outfile):
    urllib.urlretrieve(url,"{0}".format(outfile))

def crawl(outputdir,downloadVideo):
    
    csvfile = "{0}/{1}".format(outputdir, CSV_FILENAME)

    # create if not exists with a
    cf = open(csvfile, 'ab')
    csvWriter = csv.writer(cf)
    csvheaderrow = []
    csvheaderrow.append("title")
    csvheaderrow.append("speakers")
    csvheaderrow.append("description")
    csvheaderrow.append("link")
    csvheaderrow.append("video")
    csvheaderrow.append("thumbnail")
    csvWriter.writerow(csvheaderrow)
     
    # request & parse rss feed via feedparser
    feed=feedparser.parse(FEEDURL)
    
    for entry in feed[ 'entries' ]:
        video='';
        videofilename=''
        thumbnail=''
        # Get the smallest thumbnail
        if (entry.has_key('media_thumbnail') and len(entry['media_thumbnail']) > 0):
            thumbsize=0
            for mt in entry['media_thumbnail']:
                s = int(mt['width'])
                if (thumbsize == 0 or s < thumbsize ):
                    thumbsize = s
                    thumbnail = mt['url']
        # Get the smallest video mp4 
        if (entry.has_key('media_content') and len(entry['media_content']) > 0):
            videosize=0
            for mc in entry['media_content']:
                if (mc['medium'] == 'video' ):
                    s = int(mc['filesize'])
                    if ( videosize ==0 or s < videosize ):
                        # Skip the file with filesize=1 as always the file with filesize=1 is the largest
                        if ( s !=1 ):
                            videosize = s
                            video = mc['url']
        # Skip if either thumbnail or video is empty
        if ( empty(thumbnail) or empty(video) ):
            continue

        # Print entry info only when we have both video and thumbnail
        # Write to CSV
        videofilename = getvideofilename(entry['title'].encode('utf8'));
        csvdatarow=[]
        csvdatarow.append(entry['title'].encode('utf8'))
        csvdatarow.append(entry['author'].encode('utf8'))
        csvdatarow.append(entry['description'].encode('utf8'))
        csvdatarow.append(entry['link'])
        csvdatarow.append(videofilename)
        csvdatarow.append(thumbnail)
        csvWriter.writerow(csvdatarow)
        
        if downloadVideo:
            # Download mp4
            outvideofile = "{0}/{1}".format(outputdir,videofilename)
            print "Downloading %s ..." % videofilename
            download(video, outvideofile)
        ###
        ###  END OF LOOP
    # Close files
    cf.close()   

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    if (argc < 2 or argc > 3 ):
        usage_quit(argvs[0])
    
    downloadVideo=True
    if argc ==3:
        p =  argvs[2].lower()
        if (p != '-skip' and p != '--skip'):
            usage_quit(argvs[0])
        downloadVideo=False
     
    crawl(argvs[1],downloadVideo)

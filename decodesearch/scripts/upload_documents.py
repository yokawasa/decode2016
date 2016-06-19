#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

config_file = 'search.conf'
api_version = '2015-02-28'
permalink_base='https://www.microsoft.com/ja-jp/events/decode/2016/session.aspx'
thumbnail_url_base = 'http://searchjapanwest.blob.core.windows.net/decode16images'

def gettrackname(s):
    # N.trackname -> trackname
    arr=s.split('.')
    return arr[len(arr)-1]

def read_config(s):
    config = {}
    f = open(s)
    line = f.readline().strip()
    while line:
        #print line
        line = f.readline().strip()
        # skip if line start from sharp
        if line[0:1] == '#':
            continue
        arrs=line.split('=')
        if len(arrs) != 2:
            continue
        config[arrs[0]] = arrs[1]
    f.close
    return config

class AzureSearchClient:
    def __init__(self, api_url, api_key, api_version):
        self.api_url=api_url
        self.api_key=api_key
        self.api_version=api_version
        self.headers={
            'Content-Type': "application/json; charset=UTF-8",
            'Api-Key': self.api_key,
            'Accept': "application/json", 'Accept-Charset':"UTF-8"
        }

    def add_documents(self,index_name, documents, merge):
        action = 'mergeOrUpload' if merge else 'upload'
        for document in documents:
            document['@search.action'] = action
        
        # Create JSON string for request body
        import simplejson as json
        reqobjects={}
        reqobjects['value'] = documents
        from StringIO import StringIO
        io=StringIO()
        json.dump(reqobjects, io)
        req_body = io.getvalue()
        # HTTP request to Azure search REST API
        import httplib
        conn = httplib.HTTPSConnection(self.api_url)
        conn.request("POST",
                "/indexes/{0}/docs/index?api-version={1}".format(index_name, self.api_version),
                req_body, self.headers)
        response = conn.getresponse()
        print "status:", response.status, response.reason
        data = response.read()
        print "data:", data
        conn.close()

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    if (argc != 3):
        print 'Usage: # python %s <csvfile> <indexname>' % argvs[0]
        quit()
   
    csvfile = argvs[1];
    indexname = argvs[2];
    documents = []
    docnum = 0
    import csv
    with open(csvfile, 'r') as f:
        reader = csv.reader(f)
        next(reader)   # skip header
        # title,speakers,description,link,video,thumbnail
        for row in reader:
            sessionid=row[7]
            title=row[0].decode('utf8')
            speakername=row[5].decode('utf8')
            speakerid=row[6]
            track = gettrackname(row[2])
            url= "{0}#{1}".format(permalink_base, sessionid)
            thumbnail= "{0}/spk-{1}.jpg".format(thumbnail_url_base, speakerid)
            description=row[1].decode('utf8')
            document = {
                "id" : sessionid,
                "title": title,
                "speakername": speakername,
                "speakerid": speakerid,
                "track": track,
                "url": url,
                "thumbnail": thumbnail,
                "description": description
            }
            documents.append(document)

    config = read_config(config_file)
    client=AzureSearchClient(
        "{0}.search.windows.net".format(config["SEARCH_SERVICE_NAME"]),
        config["SEARCH_API_KEY"],
        api_version)
    client.add_documents(indexname, documents, 'upload')

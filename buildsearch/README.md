#  Build 2016 Speech Search (closed caption)

This reposotiry contains source codes used for Build 2016 Speech Search (closed caption) during de:code 2016 DEV-018 session

Demo site: [https://aka.ms/build2016captions](https://aka.ms/build2016captions)

![build2016 speech search screenshot](https://github.com/yokawasa/decode2016/raw/master/buildsearch/img/screen-build2016sessions-closedcaption-search.png)

## Target environments to run
 * Scripts for data generation and upload: Linux / Mac OS where Python and Shell scripts are runnable
 * Webapps: only need to have HTTPD on any OS that can handle HTML and PHP

## Procedure for data generation and uploading
### 1. Azure Search

To use Microsoft Azure Search, you must create an Azure Search service in the Azure Portal. Here are instructions:
 * [Create a service](https://azure.microsoft.com/en-us/documentation/articles/search-create-service-portal/)

### 2. Azure Search Account Info Configuration for Scrpts

Put your azure search service name and API admin key info in the following search.conf file:

<u>buildsearch/scripts/search.conf</u>

    # Azure Search Service Name ( never put space before and after = )
    SEARCH_SERVICE_NAME=<Azure Search Service Name>
    # Azure Search API Admin Key ( never put space before and after = )
    SEARCH_API_KEY=<Azure Search API Admin Key>

### 3. Create Schema

The following scripts create build2016sessions and build2016captions index schema in your Azure Search service:

    cd buildsearch/scripts
    ./create_sessions_schema.sh
    ./create_captions_schema.sh

<u>build2016sessions schema</u>

    {
        "name": "build2016sessions",
        "fields": [
            { "name":"id", "type":"Edm.String", "key": true, "searchable": false, "filterable":true, "facetable":false },
            { "name":"title", "type":"Edm.String", "searchable": true, "filterable":true, "sortable":true, "facetable":false, "analyzer":"en.microsoft" },
            { "name":"speakers", "type":"Edm.String", "searchable": true, "filterable":true, "sortable":true, "facetable":false, "analyzer":"en.microsoft" },
            { "name":"url", "type":"Edm.String", "searchable": false, "filterable":false, "sortable":false, "facetable":false },
            { "name":"thumbnail", "type":"Edm.String", "searchable": false, "filterable":false, "sortable":false, "facetable":false },
            { "name":"video", "type":"Edm.String", "searchable": false, "filterable":false, "sortable":false, "facetable":false },
            { "name":"text", "type":"Edm.String", "searchable": true, "filterable":false, "sortable":false, "facetable":false, "analyzer":"en.microsoft" }
        ],
        "suggesters": [
            { "name":"sessionsg", "searchMode":"analyzingInfixMatching", "sourceFields":["title","speakers"] }
        ],
        "corsOptions": {
            "allowedOrigins": ["*"],
            "maxAgeInSeconds": 300
        }
    }

<u>build2016captions schema</u>

    {
        "name": "build2016captions",
        "fields": [
            { "name":"id", "type":"Edm.String", "key": true, "searchable": false, "filterable":false, "facetable":false },
            { "name":"sessionid", "type":"Edm.String","searchable": false, "filterable":true, "facetable":false },
            { "name":"beginsec", "type":"Edm.Int32", "searchable": false, "filterable":false, "sortable":true, "facetable":false },
            { "name":"begin", "type":"Edm.String", "searchable": false, "filterable":false, "sortable":false, "facetable":false },
            { "name":"end", "type":"Edm.String", "searchable": false, "filterable":false, "sortable":false, "facetable":false },
            { "name":"caption", "type":"Edm.String", "searchable": true, "filterable":false, "sortable":false, "facetable":false, "analyzer":"en.microsoft" }
        ],
        "corsOptions": {
            "allowedOrigins": ["*"],
            "maxAgeInSeconds": 300
        }
    }

### 4. Upload build 2016 session data onto build2016sessions index

A script, upload_sessions.py generate build sessions data from build2016.csv included in buildsearch/data directory and upload them to build2016sessions index.

    cd buildsearch/scripts
    ./upload_sessions.py ../data/build2016.csv build2016sessions

Just for the one who are interested in how to generate build2016.csv, I included rssCrawler.py in buildsearch/scripts directory. rssCrawler.py is the one that fetchs build 2016 breakout sessions raw data from original ch9 site, mechanizes fetched data, and generate build2016.csv.

    cd buildsearch/scripts
    # if you want to generate only build2016.csv, run lik this
    ./rss_crawler.py /path-to-output-dir/ -skip
    # if you want to not only generate build2016.csv but also download build 2016 breakout session videos, run lik this
    ./rss_crawler.py /path-to-output-dir/ 

### 5. Upload closed captions data onto build2016captions index

First fo all, extract closed captions data for each breakout sessions which is included as buildsearch/data/closed-caption-data.zip:

    cd buildsearch/data
    unzip closed-caption-data.zip

Then, run upload_captions.py script to upload all closed captions data for each breakout sessions onto build2016captions index:

    cd buildsearch/scripts
    ./upload_cations.py ../data/build2016.csv ../data build2016captions

[note] if you want to generate closed captions from video Contents by youself instead of using closed-caption-data.zip, go to an [optional procedure](#).

### 6. Download video contents (Optional)

Run this command to download build 2016 breakout session video contents only if you haven't downloaded yet:

    cd /path-to-dir-for-videos/
    buildsearch/videos/download_videos.sh

## Webapp deployment procedure

### 1. Azure Search Account Info Configuration for webapps scripts

Put your azure search service name and API Query key info in the following scripts:

<u>buildsearch/webapps/caption.php</u>

    $azureSearchAccount="<Azure Search Service Name>";
    $azureSearchQueryApiKey="<Azure Search API Query Key>";

<u>buildsearch/webapps/suggest.php</u>

    $azureSearchAccount="<Azure Search Service Name>";
    $azureSearchQueryApiKey="<Azure Search API Query Key>";

<u>buildsearch/webapps/search.js</u>

    var azureSearchAccount="<Azure Search Service Name>";
    var azureSearchQueryApiKey="<Azure Search API Query Key>";

<u>buildsearch/webapps/search-caption.js</u>

    var azureSearchAccount="<Azure Search Service Name>";
    var azureSearchQueryApiKey="<Azure Search API Query Key>";

### 2. Move all webapps, videos and captions files to appropriate directories

Suppose you want to deploy webapps files to /path-to-webapps-base/buildsearch, move all videos and captions files to the following dir respectively:

<table>
  <tr>
    <td>Webapp files </td><td>/path-to-webapps-base/buildsearch (ex. /var/www/html/buildsearch) <br>[notice] you can name any for webapp dir. It doesn't need to be buildsearch</td>
  </tr>
  <tr>
    <td>Videos files</td><td>/path-to-webapps-base/video (ex. /var/www/html/video)</td>
  </tr>
  <tr>
    <td>Closed Captions files</td><td>/path-to-webapps-base/captions (ex. /var/www/html/captions)</td>
  </tr>
</table>

Then, access your webapp index.html and see if the following page, which is basically the same as [the demo site](https://aka.ms/build2016captions), is displayed.

![build2016 search top screenshot](https://github.com/yokawasa/decode2016/raw/master/buildsearch/img/screen-build2016sessions-search-top.png)


## Generate Closed Captions from Video Contents (Optional Procedure) 

This is a procedure only for those who want to generate closed captions from video contents by themselves. If you use closed-caption-data.zip which is included in this repository instead of generating by yourself, skip this procedure.

### 1. Get azure_media_indexer_java ready

[azure_media_indexer_java](https://github.com/yokawasa/azure-media-indexer-java) is leveraged for closed cation generations, thus get azure_media_indexer_java ready by following an instruction [here](https://github.com/yokawasa/azure-media-indexer-java)

### 3. Configure a script for closed caption generation and run

Set appropriate path or filename in the following generate_closed_captions.sh file:

<u>buildsearch/scripts/generate_closed_captions.sh</u>

    VIDEO_DIR="/path-to-webapps-base/video"
    DOWNLOAD_DIR="/path-to-webapps-base/captions"
    LOGFILE="runlog.txt"
    AMI_DIR="/path-to-azure-media-indexer-java/"
    LISTFILE="videoslist.txt"

Then finally run the script to generate closed captions for video files that you specify in videoslist.txt.
    
    cd buildsearch/scripts
    ./generate_closed_captions.sh

## Questions, Request, and Contribution

Questions, reqeusts on this materials, bug reports and pull requests are all welcome on GitHub at https://github.com/yokawasa/decode2016.


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

Fill in your azure search service name and API admin key info in the following search.conf file:

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

### 5. Upload closed captions data for each breakout sessions onto build2016captions index

First fo all, extract closed captions data for each breakout sessions which is included as buildsearch/data/closed-caption-data.zip:

    cd buildsearch/data
    unzip closed-caption-data.zip

Then, run upload_captions.py script to upload all closed captions data for each breakout sessions onto build2016captions index:

    cd buildsearch/scripts
    ./upload_cations.py ../data/build2016.csv ../data build2016captions


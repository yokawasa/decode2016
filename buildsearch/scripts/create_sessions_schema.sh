#!/bin/sh

. ./search.conf

SERVICE_NAME=$SEARCH_SERVICE_NAME
ADMIN_KEY=$SEARCH_API_KEY
API_VER='2015-02-28'
CONTENT_TYPE='application/json'
URL="https://$SERVICE_NAME.search.windows.net/indexes?api-version=$API_VER"

curl -s\
 -H "Content-Type: $CONTENT_TYPE"\
 -H "api-key: $ADMIN_KEY"\
 -XPOST $URL -d'{
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
}'

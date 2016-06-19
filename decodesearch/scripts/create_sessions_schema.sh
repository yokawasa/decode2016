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
    "name": "decodesessions2016",
    "fields": [
        { "name":"id", "type":"Edm.String", "key": true, "searchable": false, "filterable":false, "facetable":false },
        { "name":"title", "type":"Edm.String", "searchable": true, "filterable":true, "sortable":true, "facetable":false, "analyzer":"ja.microsoft" },
        { "name":"speakername", "type":"Edm.String", "searchable": true, "filterable":true, "sortable":true, "facetable":false, "analyzer":"ja.microsoft" },
        { "name":"speakerid", "type":"Edm.String", "searchable": false, "filterable":false, "sortable":true, "facetable":false  },
        { "name":"track", "type":"Edm.String", "searchable": false, "filterable":true, "sortable":true, "facetable":false },
        { "name":"url", "type":"Edm.String", "searchable": false, "filterable":false, "sortable":true, "facetable":false },
        { "name":"thumbnail", "type":"Edm.String", "searchable": false, "filterable":false, "sortable":true, "facetable":false },
        { "name":"description", "type":"Edm.String", "searchable": true, "filterable":false, "sortable":false, "facetable":false, "analyzer":"ja.microsoft" }
     ],
     "suggesters": [
        { "name":"sessionsg", "searchMode":"analyzingInfixMatching", "sourceFields":["title","speakername"] }
     ],
     "corsOptions": {
        "allowedOrigins": ["*"],
        "maxAgeInSeconds": 300
    }
}'

var azureSearchAccount="<Azure Search Service Name>";
var azureSearchQueryApiKey = "<Azure Search API Query Key>";
var indexNameSessions="build2016sessions";
var inSearch = false;

// Instantiate the Bloodhound suggestion engine
var movies = new Bloodhound({
    datumTokenizer: function (datum) {
        return Bloodhound.tokenizers.whitespace(datum.value);
    },
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    remote: {
        url: "suggest.php?$top=10&suggesterName=sessionsg&$select=title&fuzzy=true&api-version=2015-02-28&search=%q",
        filter: function (movies) {
            // Map the remote source JSON array to a JavaScript object array
            return $.map(movies.value, function (movie) {
                return {
                    value: movie.title
                };
            });
        },
        prepare: function(query, settings) {
            settings.url = settings.url.replace('%q', query);
            return settings;
       }
    }
});

// Initialize the Bloodhound suggestion engine
movies.initialize();
// Instantiate the Typeahead UI
$('.input-group .form-control').typeahead(null, {
    displayKey: 'value',
    source: movies.ttAdapter()
});


function execSearch()
{
	var q = encodeURIComponent($("#q").val());
	var searchAPI = "https://" + azureSearchAccount + ".search.windows.net/indexes/"+ indexNameSessions +"/docs?$top=255&$select=id,title,thumbnail&api-version=2015-02-28&search=" + q;
	inSearch= true;
    $.ajax({
        url: searchAPI,
        beforeSend: function (request) {
            request.setRequestHeader("api-key", azureSearchQueryApiKey);
            request.setRequestHeader("Content-Type", "application/json");
            request.setRequestHeader("Accept", "application/json; odata.metadata=none");
        },
        type: "GET",
        success: function (data) {
			$( "#mediaContainer" ).html('');
			for (var item in data.value)
			{
				var id = data.value[item].id;
				var title = data.value[item].title;
				var imageURL = data.value[item].thumbnail;
				$( "#mediaContainer" ).append( '<div class="col-md-4" style="text-align:center"><a href="caption.php?sessionid=' + id + '"><img src=' + imageURL + ' height=200><br><div style="height:100px"><b>' + title + '</b></a></div></div>' );
			}
			inSearch= false;
        }
    });
}

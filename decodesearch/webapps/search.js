var azureSearchAccount="<Azure Search Service Name>";
var azureSearchQueryApiKey="<Azure Search API Query Key>";
var indexNameSessions="decodesessions2016";
var azureMLModelId = "046a71e5-294c-4b7b-9d12-a9e3d2745ebe";
var azureMLBuildId = "1555861";
var inSearch = false;


// Instantiate the Bloodhound suggestion engine
var sessions = new Bloodhound({
    datumTokenizer: function (datum) {
        return Bloodhound.tokenizers.whitespace(datum.value);
    },
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    remote: {
        url: "http://yoichika-dev1.japanwest.cloudapp.azure.com/decode/decode2016session-prepub/suggest.php?$top=10&suggesterName=sessionsg&$select=title,speakername&fuzzy=true&api-version=2015-02-28&search=%q",
        filter: function (sessions) {
            // Map the remote source JSON array to a JavaScript object array
            return $.map(sessions.value, function (session) {
                return {
                    value: session.title + ' ( ' + session.speakername + ' ) ' 
                };
            });
        },
        prepare: function(query, settings) {
            settings.url = settings.url.replace('%q', query);
            return settings;
        }
    },

});

// Initialize the Bloodhound suggestion engine
sessions.initialize();
$('.input-group .form-control').typeahead({
    hint: false,
    highlight: true,
    minLength: 1
}, {
    displayKey: 'value',
    source: sessions.ttAdapter(),
    limit : 9,
});


function execSearch()
{
	// Execute a search to lookup viable sessions
	var q = encodeURIComponent($("#q").val());
	var searchAPI = "https://" + azureSearchAccount + ".search.windows.net/indexes/" + indexNameSessions + "/docs?$top=120&$select=id,title,track,url,thumbnail,description&api-version=2015-02-28&search=" + q;
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
				var track = data.value[item].track;
				var url = data.value[item].url;
				var imageURL = data.value[item].thumbnail;
				$( "#mediaContainer" ).append( 
                    '<div class="col-md-4" style="text-align:center"><a href="javascript:void(0);" onclick="opensessionDetails(\'' 
                   + id + '\');"><img src=' + imageURL + ' height=150><br><div style="height:100px"><b>' + title + '</b></a><br>'+track+'</div></div>' );
			}
			inSearch= false;
        }
    });
}

function opensessionDetails( id )
{
	// Open the dialog with the recommendations
	$("#modal-title").html("Loading " + id + " ... ");
	$("#modal-description").html("");
	$("#modal-track").html("");
	$("#recDiv").html('Loading recommendations...');

	var lookupAPI = "https://" + azureSearchAccount + ".search.windows.net/indexes/" + indexNameSessions + "/docs/" + id +"?$top=12&$select=id,title,track,url,description&api-version=2015-02-28";
	inSearch= true;
    $.ajax({
        url: lookupAPI,
        beforeSend: function (request) {
            request.setRequestHeader("api-key", azureSearchQueryApiKey);
            request.setRequestHeader("Content-Type", "application/json");
            request.setRequestHeader("Accept", "application/json; odata.metadata=none");
        },
        type: "GET",
        success: function (data) {
			var id = data.id;
			var title = data.title;
			var track = data.track;
			var url = data.url;
			var description = data.description.replace(/\r?\n/g,""); // remove return
			description = description.replace(/\"/g,"");                         // remove double quote
	        $("#modal-title").html(id + ': <a href="' + url + '">' + title + '</a>');
	        $("#modal-description").html(description);
	        $("#modal-track").html('トラック: ' + track);
			inSearch= false;
        }
    });

    var recommendatationAPI = "https://api.datamarket.azure.com/data.ashx/amla/recommendations/v2/ItemRecommend?$format=json&modelId='" + azureMLModelId + "'&numberOfResults=5&buildId=" + azureMLBuildId + "&includeMetadata=false&apiVersion='1.0'&itemIds='" + id + "'";

    $.ajax({
        url: recommendatationAPI,
        beforeSend: function (request) {
            request.setRequestHeader("Authorization", "Basic eW9pY2hpLmthd2FzYWtpQGhvdG1haWwuY28uanA6NXJBdHRheHVXa0FBUjI5emtPeUFVQmRvLzJuSkVMMFNEMTFobWFnUEp1OA==");
        },
        type: "GET",
        success: function (data) {
            $("#recDiv").html('');
            $( "#recDiv" ).append('<ul>');
            var id = '';
            for (var item in data.d.results)
                $( "#recDiv" ).append( '<li>' + data.d.results[item].Id + ':<a href="https://www.microsoft.com/ja-jp/events/decode/2016/session.aspx#' + data.d.results[item].Id  +'" target="_blank">' + data.d.results[item].Name + '</li>' );
            $( "#recDiv" ).append('</ul>');
        }
    });

	$('#myModal').modal('show');
}


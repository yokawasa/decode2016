<?php
    $azureSearchAccount="<Azure Search Service Name>";
    $azureSearchQueryApiKey = "<Azure Search API Query Key>";
    $AZURESEARCH_URL_BASE= 'https://'.$azureSearchAccount.'.search.windows.net/indexes/build2016sessions/docs';

    $req=$_REQUEST;
    $params = array();
    if( is_array($req) ) {
        foreach( $req as $name => $value) {
            $params[$name] = $value;
       }
    }
    $sessionid =  empty($params['sessionid']) ? 'P420' : $params['sessionid'];

    // initial value
    $title='';
    $text='';
    $videofile ='';
    $vttfile ='';
    
    $url = $AZURESEARCH_URL_BASE . '?api-version=2015-02-28&$filter=' . urlencode(sprintf("id eq '%s'",$sessionid));
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL,$url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_TIMEOUT, 10);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array(
        'api-key: '. $azureSearchQueryApiKey,
        'Accept: application/json',
    ));

    $data = curl_exec($ch);
    if (curl_errno($ch)) {
        print "Error: " . curl_error($ch);
    } 
    else 
    {
        $res_arr = json_decode($data,true);
        $docs = $res_arr['value'];
        if (count($docs) ==1) {
            $title = $docs[0]['title'];
            $text = $docs[0]['text'];
            $s = urlencode($docs[0]['video']);
            $videofile = sprintf("../video/%s", $s);
            $vttfile = sprintf("../captions/%s.vtt",$s);
        }
    }
    curl_close($ch);

?>
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="favicon.ico">

    <title>Build 2016 Session Caption Search ( de:code 2016 demo site )</title>

    <!-- Bootstrap core CSS -->
    <link href="dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="dist/css/typeahead.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="design-caption.css" rel="stylesheet">

    <script type="text/javascript">

    function restart(value) {
        var video = document.getElementById("Video1");
        video.currentTime = value;
    }
    </script>

  </head>

  <body onLoad='init("<?php echo $sessionid; ?>")'>

    <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <a class="navbar-brand" href="/decode/build2016captions/">Build 2016 Session Caption Search ( de:code 2016 demo site )</a>
        </div>
      </div>
    </nav>

    <div class="container">

		<div class="row">
			<div class="input-group" style="padding:20px;"> 
				  <input type="text" class="form-control" placeholder="Search for...in closed captions" id="q"  onkeydown = "if (event.keyCode == 13) execSearch();" >
				  <span class="input-group-btn">
					<button class="btn btn-default" type="button" onclick='execSearch("<?php echo $sessionid; ?>");'>Go!</button>
				  </span>
                  
			</div><!-- /input-group -->
		</div>
    </div><!-- /.container -->

        <div class="colmask doublepage">

            <div class="colleft">
                <div class="col1">
                    <!-- Column 1 start -->
                    <center><h3>Session Video Track</h3></center>

    <br />
    <div>
        <video id="Video1" controls autoplay width="600">
            <source src="<?php echo $videofile; ?>" srclang="en" type="video/mp4">
            <track id="trackEN"  src="<?php echo $vttfile; ?>"  kind="captions" srclang="en" label="English" default>
        </video>
        
    <br>
    <br>
<a><?php echo $title; ?></a><br>
<?php echo $text; ?>
    </div>


                    <!-- Column 1 end -->
            </div>

            <div class="col2">
                <!-- Column 2 start -->
                <center><h3>Closed Captions</h3></center>
                <center><p id="hits2"></p></center>
                <div id="colcontainer2"></div>
                <!-- Column 2 end -->
            </div>

        </div> <!-- colleft -->


    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <script src="dist/js/bootstrap.min.js"></script>
    <!--Tiwtter Typeahead lib -->
    <script src="dist/js/typeahead.bundle.min.js"></script>
	<script src="search-caption.js"></script>
  </body>
</html>

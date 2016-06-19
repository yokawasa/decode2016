<?php
    $azureSearchAccount="<Azure Search Service Name>";
    $azureSearchQueryApiKey = "<Azure Search API Query Key>";
    $indexNameSessions="build2016sessions";

    $AZURESEARCH_URL_BASE= 'https://' . $azureSearchAccount .'.search.windows.net/indexes/'.$indexNameSessions.'/docs/suggest';

    $req=$_REQUEST;
    $params = array();
    if( is_array($req) ) {
        foreach( $req as $name => $value) {
            $params[$name] = $value;
       }
    }

    $p = array();
    foreach($params as $k => $v){
        $p[] = $k.'='.urlencode($v);
    }

    $url = $AZURESEARCH_URL_BASE . '?' . implode('&', $p);

    $opts = array(
        'http'=>array(
            'method'=>"GET",
            'header'=>"Accept: application/json\r\n" .
                "api-key: $azureSearchQueryApiKey\r\n",
            'timeout' =>10
        )
    );

    $context = stream_context_create($opts);
    $data = file_get_contents($url, false, $context);

    if ($data  === false) {
        print "Error!";
    }
    else 
    {
        //print var_dump($data);
        header('Content-Length: '.strlen($data));
        header('Content-Type: application/json; odata.metadata=minimal');
        header('Access-Control-Allow-Origin: *');
        print $data;
    }
?>

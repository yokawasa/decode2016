<?php
    $azureSearchAccount="<Azure Search Service Name>";
    $azureSearchQueryApiKey = "<Azure Search API Query Key>";
    $AZURESEARCH_URL_BASE= 'https://'.$azureSearchAccount.'.search.windows.net/indexes/decodesessions2016/docs/suggest';

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
        //print var_dump($data);
        header('Content-Length: '.strlen($data));
        header('Content-Type: application/json; odata.metadata=minimal');
        header('Access-Control-Allow-Origin: *');
        print $data;
    }
    curl_close($ch);
?>

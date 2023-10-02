<?php

$url = '127.0.0.1:2358/submissions?wait=true';
$code = $_POST['code'];
$data = array(
     "source_code" => $code,
     "language_id" => "50",
     "expected_output" => "hello world"
);
$data_string = json_encode($data);
$ch=curl_init($url);
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
curl_setopt($ch, CURLOPT_POSTFIELDS, $data_string);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HEADER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER,     
	array(         
            'Content-Type:application/json',         
            'Content-Length: ' . strlen($data_string),
	    'testheader:nchuojismyfirstproject'     
	) 
);

$result = curl_exec($ch);
$header_size = curl_getinfo($ch, CURLINFO_HEADER_SIZE);
$header = substr($result, 0, $header_size);
$body = substr($result, $header_size);
$body2 = json_decode($body);

session_start();
$_SESSION['token'] = $body2->token;
curl_close($ch);
header("Location: final.php");





<?php
// file_get_contentsでデータを取得
$url = 'http://127.0.0.1:6006/up';
// 送信するデータ
$filename = 'sample.jpg';
$image = file_get_contents('sample.jpg');

// echo $image;
// POSTするデータを作成
$header = [
    "Content-Type: application/json; charset=UTF-8;",
    "Content-Length: ".strlen($image),
    "File-Name: " . $filename
];
$context = stream_context_create([
    'http' => [
        'method'=> 'POST',
        'header'=> implode("\r\n", $header),
        'content' => $image
    ]
]);
$raw_data = file_get_contents($url, false, $context);
// jsonからstdClassに変換

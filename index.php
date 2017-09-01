<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Test page for file loading</title>

    <link href="css/public.css" rel="stylesheet" type="text/css" >
    <script src="js/jquery.min.js"></script>
    <script src="js/main.js"></script>

</head>
<body>

<?php

$output = shell_exec('omxplayer --win "0 0 640 480" /addsweb/2.mp4');
echo "<pre>$output</pre>";

?>

</body>
</html>

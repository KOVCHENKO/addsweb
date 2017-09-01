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

<div class="container">
    <div class="timer"></div>
    <div class="slideshow">
        <?php

        $dir = 'images';
        $images = scandir($dir);

        foreach($images as $image) {
            echo '<div class="slide">
                    <img class="image-type" src="images/'.$image.'" />
                  </div>';
        }

        ?>
    </div>
</div>

</body>
</html>
<?php

	$output = shell_exec('omxplayer --win "0 0 640 480" /addsweb/2.mp4');
	echo "<pre>$output</pre>";

?>
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<title>Lucky Numbers</title>
</head>
<body>
<?php

	/* This script generates 3 random numbers. */
	function gen_rand() {
		return rand(1, 99);
	}

	// Create three random numbers:
	$n1 = rand(1, 99);
	$n2 = rand(1, 99);
	$n3 = rand(1, 99);

	// Print out the numbers:
	print "<p>Your lucky numbers are:<br />";
	
	for ($i = 0; $i < 10; $i++) {
		print gen_rand() . "<br />";
	}
	print "</p>";

?>
</body>
</html>
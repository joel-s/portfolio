<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<title>Lucky Numbers</title>
</head>
<body>
<?php // Script 4.6 - random.php
/* This script generates 3 random numbers. */

// Address error handling, if you want.

// Create three random numbers:
$n1 = rand (1, 99);
$n2 = rand (1, 99);
$n3 = rand (1, 99);

// Print out the numbers:
print "<p>Your lucky numbers are:<br /> $n1<br /> $n2<br /> $n3</p>";
?>
</body>
</html>
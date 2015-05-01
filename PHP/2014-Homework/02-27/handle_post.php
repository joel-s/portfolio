<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Forum Posting</title>
<style type="text/css">
.number { font-weight: bold; }
</style>
</head>

<body>

<?php

ini_set('display_errors', 1);         // Display errors
error_reporting (E_ALL | E_STRICT);   // Show all possible problems!

// Get the values from the POST
$first_name = $_POST['first_name'];
$last_name = $_POST['last_name'];
$posting = nl2br($_POST['posting']);

$name = $first_name . ' ' . $last_name;

$html_post = htmlentities($_POST['posting']);
$strip_post = strip_tags($_POST['posting']);

print "<div>Thank you, $name, for your posting: 
<p>Original: $posting</p>
<p>Entity: $html_post</p>
<p>Stripped: $strip_post</p>
</div>";

?>

</body>
</html>

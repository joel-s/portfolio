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

print "<div><p>Thank you, $name, for your posting.</p>
<p>Posting: $posting</p>";

$name = urlencode($name);
$email = urlencode($_POST['email']);

print "<p>Click <a href=\"thanks.php?name=$name&email=$email\">here</a>
to continue.</p></div>";

?>

</body>
</html>

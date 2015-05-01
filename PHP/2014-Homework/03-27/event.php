<!DOCTYPE html>
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title>Add an Event</title>
</head>
<body>
<?php // Script 7.9 - event.php
/* This script handles the event form. */

ini_set('display_errors', 1);         // Display errors
error_reporting (E_ALL | E_STRICT);   // Show all possible problems!

// Print the text:
print "<p>You want to add an event called <b>{$_POST['name']}</b>" .
      " which takes place on: <br />";

// Print each weekday:
if (isset($_POST['days']) AND is_array($_POST['days'])) {

	foreach ($_POST['days'] as $day) {
		print "&nbsp &nbsp $day<br />\n";
	}

} else {
	print 'Please select at least one weekday for this event!';
}

// Complete the paragraph:
print '</p>';
?>
</body>
</html>
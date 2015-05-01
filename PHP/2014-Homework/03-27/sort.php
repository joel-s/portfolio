<!DOCTYPE html>
<html>
<head>
 <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
 <title>My Little Gradebook</title>
</head>

<body>

<?php

ini_set('display_errors', 1);         // Display errors
error_reporting (E_ALL | E_STRICT);   // Show all possible problems!

$grades = array(
'Richard' => 95,
'Sherwood' => 82,
'Toni' => 98,
'Franz' => 87,
'Melissa' => 75,
'Roddy' => 85
);

print '<p>Originally the array looks like this: <br />';
foreach ($grades as $student => $grade) {
	print "$student: $grade<br />\n";
}
print '</p>';

// Sort by value in reverse order
arsort ($grades);
print '<p>After sorting the array by value using arsort(), the array looks like this: <br />';
foreach ($grades as $student => $grade) {
	print "$student: $grade<br />\n";
}
print '</p>';

// Sort by key, then print again:
ksort ($grades);
print '<p>After sorting the array by key using ksort(), the array looks like this: <br />';
foreach ($grades as $student => $grade) {
	print "$student: $grade<br />\n";
}
print '</p>';

?>

</body>
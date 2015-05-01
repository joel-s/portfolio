<!DOCTYPE html>
<html>
<head>
 <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
 <title>No Soup for You!</title>
</head>
<body>
<h1>Mmm...soups</h1>

<?php


$soups = array (
'Monday' => 'Clam Chowder',
'Tuesday' => 'White Chicken Chili',
'Wednesday' => 'Vegetarian'
);


// Count and print the current number of elements:
$count1 = count ($soups);
print "<p>The soups array originally had $count1 elements.</p>\n"; 

// Add three items to the array:
$soups['Thursday'] = 'Chicken Noodle';
$soups['Friday'] = 'Tomato';
$soups['Saturday'] = 'Cream of Broccoli';
 
// Count and print the number of elements again:
$count2 = count ($soups);
print "<p>After adding 3 more soups, the array now has $count2 elements.</p>\n";

// Print the contents of the array:
print "<pre>\n";
print_r ($soups);
print "</pre>";

?>

</body>
<!DOCTYPE html>
<html>
<head>
 <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
 <title>Larry Ullman's Books and Chapters</title>
</head>

<body>

<h1>Some of Larry Ullman's Books</h1>

<?php

$phpvqs = array (1 => 'Getting Started with PHP', 'Variables', 'HTML Forms and PHP', 'Using Numbers');
$phpadv = array (1 => 'Advanced PHP Techniques', 'Developing Web Applications', 'Advanced Database Concepts', 'Security Techniques');
$phpmysql = array (1 => 'Introduction to PHP', 'Programming with PHP', 'Creating Dynamic Web Sites', 'Introduction to MySQL');

$books = array (
'PHP VQS' => $phpvqs,
'PHP Advanced VQP' => $phpadv,
'PHP and MySQL VQP' => $phpmysql
);

print "<p>The third chapter of my first book is <i>{$books['PHP VQS'][3]}</i>.</p>\n";
print "<p>The first chapter of my second book is <i>{$books ['PHP Advanced VQP'][1]}</i>.</p>\n";
print "<p>The fourth chapter of my fourth book is <i>{$books ['PHP and MySQL VQP'][4]}</i>.</p>\n";
print "\n";

foreach ($books as $title => $chapters) {
	print "<p><strong>$title</strong>"; 
	foreach ($chapters as $number => $chapter) { 
		print "<br />\nChapter $number is $chapter"; 
	} 	
	print "</p>\n\n"; 
}

?>

</body>
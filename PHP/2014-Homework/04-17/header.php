<?php // Script 8.11 - header.html #4

// Turn on output buffering:
ob_start();

?><!DOCTYPE html>

<head>
<title><?php // Print the page title.
if (defined('TITLE')) { // Is the title defined?
	print TITLE;
} else { // The title is not defined.
	print 'Raise High the Roof Beam! A J.D. Salinger Fan Club';
}
?></title>
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<link rel="stylesheet" href="css/1.css" type="text/css" 
media="screen,projection" />
</head>
<body>
<div id="wrapper">

<div id="header">
<p class="description">A J.D. Salinger Fan Club</p>
<h1><a href="index.php">Raise High the Roof Beam!</a></h1>
<ul id="nav">
<li><a href="books.php">Books</a></li>
<li><a href="#">Stories</a></li>
<li><a href="#">Quotes</a></li>
<li><a href="login.php">Login</a></li>
<li><a href="register.php">Register</a></li>
</ul>
</div><!-- header -->

<div id="sidebar">
<h2>Favorite Quotes</h2>
<p class="news">I don't exactly know what I mean by that, but I mean it.
     <br />- <em>The Catcher in the Rye</em></p>
<p class="news">I privately say to you, old friend... please accept from
     me this unpretentious bouquet of early-blooming parentheses: (((()))).<br />-
     <em>Raise High the Roof Beam, Carpenters and Seymour: An Introduction</em></p>
</div><!-- sidebar -->

<div id="content">
<!-- BEGIN CHANGEABLE CONTENT. -->
<!-- Script 8.6 - header.html -->
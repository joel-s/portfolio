<?php 
$title = "Home Page";
include 'header.php';
?>

<h1>Content goes here</h1>

<?php

open_mysql_db();

$insert = "INSERT INTO users(username, password) VALUES($user, $pswd)";
$select = "SELECT *";


?>

<?php
include 'footer.php';
?>

<!DOCTYPE html>
<html>

<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title><?php echo "Used Book Exchange | " . $title; ?></title>
    <link rel="stylesheet" type="text/css" href="styles.css">
</head>

<body>
    <div id="container">

	<div id="nav">
        <ul>
            <li><a href="index.php">Home</a></li>
            <li><a href="books.php">Books for Sale</a></li>
            <li><a href="register.php">Register</a></li>
            <li><a href="sell.php">Sell a Book</a></li>
	</ul>
	</div>

        <div id="main">  <!-- Closed in footer.php -->
<?php

ini_set('display_errors', 'On');      // Display errors
error_reporting (E_ALL | E_STRICT);   // Show all possible problems!

/******************************************************************************
 * MySQL Access functions
 *****************************************************************************/

function open_mysql_db() {
    $mysql_host = "localhost";
    $mysql_database = "books";
    $mysql_user = "books";
    $mysql_password = "password";

    $link = mysqli_connect($mysql_host, $mysql_user, $mysql_password, 
                           $mysql_database)
        or die(mysqli_error($link));

    return $link;
}

/* 
 * Return "" if email/password combo is valid, or an error string. 
 */
function authenticate_user($email, $password) {
   if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
       return "Invalid email address";
   }

   if (empty($password)) {
       return "Empty password";
   }
   
   $link = open_mysql_db();

   $query = "SELECT password FROM users WHERE email='" . $email . "';";

   $result = $link->query($query);
   if (!$result) {
       return "Database error: " . mysqli_error($link);
   }

   $row = mysqli_fetch_array($result);
   if (!$row) {
       return "Unknown email address";
   }
    
   if ($password != $row['password']) {
       return "Incorrect password";
   }
   
   return "";
}

?>

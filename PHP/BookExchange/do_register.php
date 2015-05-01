<?php 
$title = "Register";
include 'header.php';


$errors = array();

$email = filter_input(INPUT_POST, 'email', FILTER_VALIDATE_EMAIL);
if (!$email) {
   $errors[] = "You must specify a valid email address.";
}

$password = $_POST['password'];
if (empty($password)) {
   $errors[] = "You must specify a password.";
}

$confirm = $_POST['confirm_password'];
if ($confirm != $password ) {
   $errors[] = "Your password and confirmation must match.";
}

// TODO: Encrypt password

if ($errors) {
   foreach($errors as $error) {
       echo "<p class='error'>$error</p>";
   }
   echo "<p><a href='register.php'>Please correct errors to proceed.</a></p>";
} else {
   
   /*
    * INSERT new user into DB
    */

   $link = open_mysql_db();

   $query = "INSERT INTO users () VALUES ('$email', '$password');";

   if ($link->query($query)) {
       echo "<p>Successfully registered.</p>";
   } else {
       echo "<p class='error'>" . mysqli_error($link) . "</p>";
   }
}


include 'footer.php';
?>

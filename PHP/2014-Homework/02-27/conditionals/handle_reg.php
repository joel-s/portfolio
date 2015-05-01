<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>Registration</title>
    <style type="text/css" media="screen">
      .error { color: red; }
    </style>
  </head>
  <body>
    <h1>Registration Results</h1>

<?php
/* This script receives seven values from register.html:
email, password, confirm, year, terms, color, submit */

ini_set('display_errors', 1);         // Display errors
error_reporting (E_ALL | E_STRICT);   // Show all possible problems!

// Flag variable to track success:
$okay = TRUE;

// Validate the email address:
if (empty($_POST['email'])) {
   print '<p class="error">Please enter your email address.</p>';
   $okay = FALSE;
}

// Validate the password:
if (empty($_POST['password'])) {
   print '<p class="error">Please enter
   your password.</p>';
   $okay = FALSE;
}

// Check the two passwords for equality:
if ($_POST['password'] != $_POST['confirm']) {
   print '<p class="error">Your confirmed
   password does not match the original
   password.</p>';
   $okay = FALSE;
}

// Validate the year:
if ( is_numeric($_POST['year']) AND(strlen($_POST['year']) == 4) ) {

   // Check that they were born before 2015.
   if ($_POST['year'] < 2015) {
      $age = 2014 - $_POST['year'];
   // Calculate age this year.
   } else {
      print '<p class="error">Either you entered your birth year wrong or
             you come from the future!</p>';
      $okay = FALSE;
   } // End of 2nd conditional.
} else { // Else for 1st conditional.
    print '<p class="error">Please enter the year you were born as four
           digits.</p>';
    $okay = FALSE;
} // End of 1st conditional.

// Validate the terms:
if ( !( isset($_POST['terms']) AND ($_POST['terms'] == 'Yes') ) ) {
    print '<p class="error">You must accept the terms.</p>';
    $okay = FALSE;
}

// Validate the color:
switch ($_POST['color']) {

    case 'red':
    case 'yellow':
    case 'blue':
        $color_type = 'primary';
        break;

    case 'green':
        $color_type = 'secondary';
        break;

    default:
        print '<p class="error">Please select your favorite color.</p>';
        $okay = FALSE;
        break;

} // End of switch.

// If there were no errors, print a success message:
if ($okay) {
    print '<p>You have been successfully registered (but not really).</p>';
    print "<p>You will turn $age this year.</p>";
    print "<p>Your favorite color is a $color_type color.</p>";
}
?>
  </body>
</html>

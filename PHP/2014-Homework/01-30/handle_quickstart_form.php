<!DOCTYPE html>
<html>
  <head>
    <title>Your Pheedback</title>
  </head>
  
  <body>

    <?php

// Create shorthand variables for the values in the _POST array
$title = $_POST['title'];
$name = $_POST['name'];
$response = $_POST['response'];
$comments = $_POST['comments'];

// Print the received data
print "<p>Thank you, <strong>$title $name,</strong> for your comments.</p>";
print "<p>You found this example to be &ldquo;$response&rdquo; and added:<br />";
print "$comments</p>"

     ?>

  </body>
</html>

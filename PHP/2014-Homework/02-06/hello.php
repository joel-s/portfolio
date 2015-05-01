<!DOCTYPE html>
<html>
  <head>
    <title>Greetings!</title>
  </head>
  
  <body>

    <?php

ini_set ('display_errors', 1);       // Let me learn from my mistakes!
error_reporting (E_ALL | E_STRICT);  // Show all possible problems!


// Say "Hello" to the name specified in the URL parameter (e.g. ?name=Joe)
$name = $_GET['name'];
print "<p>Hello, <strong>$name</strong>!</p>";

     ?>

  </body>
</html>

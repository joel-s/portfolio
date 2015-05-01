<?php 
$title = "Register";
include 'header.php';
?>

<h1>Sign up to sell books</h1>

<form action="do_register.php" method="post">
  <table class="form">
    <tr>
      <td><label for="email">Email Address:</label></td>
      <td><input type="text" name="email"/></td>
      <td><em>Requests to buy a book will be sent to this
          address.</em></td>
    </tr>
    <tr>
      <td><label for="password">Password:</label></td>
      <td><input type="password" name="password"/></td>
      <td><em>Note: No password security, don't use your favorite
          password.</em></td>
    </tr>
    <tr>
      <td><label for="confirm password">Confirm Password:</label></td>
      <td><input type="password" name="confirm_password"/></td>
    </tr>
  </table>

  <p>
    <input type="submit" name="submit" value="Register"/>
  </p>

</form>

<?php
include 'footer.php';
?>

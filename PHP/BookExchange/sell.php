<?php 
$title = "Register";
include 'header.php';
?>

<h1>Sell a book</h1>

<form action="do_sell.php" method="post">
  <table class="form">
    <tr>
      <td><label for="email">Email Address:</label></td>
      <td><input type="text" name="email"/></td>
    </tr>
    <tr>
      <td><label for="password">Password:</label></td>
      <td><input type="password" name="password"/></td>
    </tr>
    <tr>
      <td>&nbsp;</td>
    </tr>
    <tr>
      <td><label for="author">Author (e.g., "Lewis, C.S."):</label></td>
      <td><input type="text" name="author"/></td>
    </tr>
    <tr>
      <td><label for="title">Title:</label></td>
      <td><input type="text" name="title"/></td>
    </tr>
    <tr>
      <td><label for="condition">Condition:</label></td>
      <td><input type="text" name="condition"/></td>
    </tr>
    <tr>
      <td><label for="price">Price:</label></td>
      <td><input type="text" name="price"/></td>
    </tr>
    <tr>
      <td><label for="msrp">MSRP (optional):</label></td>
      <td><input type="text" name="msrp"/></td>
    </tr>
    <tr>
      <td><label for="notes">Notes:</label></td>
      <td><textarea rows="5" cols="50" name="notes"></textarea></td>
    </tr>
  </table>

  <p>
    <input type="submit" name="submit" value="Post Book for Sale"/>
  </p>

</form>

<?php
include 'footer.php';
?>

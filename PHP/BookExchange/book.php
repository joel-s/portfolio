<?php 
$title = "Register";
include 'header.php';

$id = $_GET["id"]; 

/*
 * READ book record from DB
 */

$link = open_mysql_db();

$query = "SELECT * FROM books WHERE id=$id;";

   $result = $link->query($query) 
       or die("Database error: " . mysqli_error($link));

   $book = mysqli_fetch_array($result) or die("Unknown ID");

echo <<<_EOF_

<h1>{$book['title']}</h1>

<table class="form">
  <tr>
    <td>Author:</td>
    <td>{$book['author']}</td>
  </tr>
  <tr>
    <td>Title:</td>
    <td>{$book['title']}</td>
  </tr>
  <tr>
    <td>Condition:</td>
    <td>{$book['cond']}</td>
  </tr>
  <tr>
    <td>Price:</td>
    <td>{$book['price']}</td>
  </tr>
  <tr>
    <td>MSRP:</td>
    <td>{$book['msrp']}</td>
  </tr>
  <tr>
    <td>Notes:</td>
    <td>{$book['notes']}</td>
  </tr>
</table>

<p>
  <em>To do when we learn how to send emails: Add a "buy" button.</em>
</p>

_EOF_;


include 'footer.php';
?>

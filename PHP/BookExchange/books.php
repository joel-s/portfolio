<?php 
$title = "Books";
include 'header.php';

/*
 * Retrieve list of books from database.
 */

$link = open_mysql_db();

$query = "SELECT * FROM books ORDER BY author, title, price;";

$result = $link->query($query);
if ($result) {
    echo <<<_EOF_
<table class="books">
  <tr>
    <th>Author</th>
    <th>Title</th>
    <th>Condition</th>
    <th>Price</th>
    <th>MSRP</th>
  </tr>
_EOF_;
    while ($row = mysqli_fetch_array($result)) {
        $id = $row['id'];
        echo "<tr>";
        echo "<td>" . $row['author'] . "</td>";
        echo "<td><a href='book.php?id=$id'>" . $row['title'] . "</a></td>";
        echo "<td>" . $row['cond'] . "</td>";
        echo "<td>" . $row['price'] . "</td>";
        echo "<td>" . $row['msrp'] . "</td>";
        echo "</tr>";
    }

    echo "</table>";

} else {
   return "Database error: " . mysqli_error($link);
}


include 'footer.php';
?>

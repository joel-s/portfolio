<?php 
$title = "Sell a Book (Result)";
include 'header.php';

$email = filter_input(INPUT_POST, 'email', FILTER_VALIDATE_EMAIL);

$result = authenticate_user($_POST['email'], $_POST['password']);
if ($result != "") {
    echo "<p class='error'>Authentication error: " . $result . "</p>";
    
} else {
    /* Authentication succeeded; check for other errors */

    $errors = array();

    $author = $_POST['author'];
    if (empty($author)) {
        $errors[] = "You must specify an author.";
    }

    $title = $_POST['title'];
    if (empty($title)) {
        $errors[] = "You must specify a title.";
    }

    $condition = $_POST['condition'];
    if (empty($condition)) {
        $errors[] = "You must specify a condition.";
    }

    $price = $_POST['price'];
    if (empty($price)) {
        $errors[] = "You must specify a price.";
    }

    $msrp = $_POST['msrp'];
    $notes = $_POST['notes'];

    if ($errors) {
        foreach($errors as $error) {
            echo "<p class='error'>$error</p>";
        }
        echo "<p><a href='sell.php'>Please correct errors to proceed.</a></p>";
    } else {

        /*
         * INSERT new book into DB
         */

        $link = open_mysql_db();

        $query = "INSERT INTO books " .
                     "(author, title, cond, price, msrp, notes, email) " .
                 "VALUES ('$author', '$title', '$condition', '$price', " .
                         "'$msrp', '$notes', '$email');";

        if ($link->query($query)) {
            echo "<p>Book posted for sale.</p>";
        } else {
            echo "<p class='error'>" . mysqli_error($link) . "</p>";
        }
    }
}

include 'footer.php';
?>

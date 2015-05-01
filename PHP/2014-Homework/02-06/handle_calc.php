<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Product Cost Calculator: Results</title>
<style type="text/css">
.number { font-weight: bold; }
</style>
</head>

<body>

<?php

// Get the values from the POST
$price = $_POST['price'];
$quantity = $_POST['quantity'];
$discount = $_POST['discount'];
$tax = $_POST['tax'];
$shipping = $_POST['shipping'];
$payments = $_POST['payments'];

// Calculate the total
$subtotal = ($price * $quantity) + $shipping - $discount;

// Add the tax
$taxrate = 1 + $tax/100;
$total = $subtotal * $taxrate;

// Calculate the monthly payments
$monthly = $total / $payments;

// Format the numbers as $x.xx
$total = number_format($total, 2);
$monthly = number_format($monthly, 2);

/*
 * Display the calculated info.
 */

print <<<END

<p>
You have selected to purchase:<br />
<strong>$quantity</strong> item(s) at a price of<br />
$<strong>$price</strong> each plus a<br />
$<strong>$shipping</strong> shipping cost and a
<strong>$tax</strong>% tax rate.
</p>

<p>After your $<strong>$discount</strong> discount, the total cost is 
$<strong>$total</strong>.</p>

<p>Divided over <strong>$payments</strong> payments, that would be
$<strong>$monthly</strong> each.</p>

END

?>

</body>
</html>

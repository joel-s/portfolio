/*
 * This function displays a conversion table of values from <beg> to <end>
 * and their corresponding equivalents according to the <typ> parameter.
 */
function conversionTable(beg, end, typ) {
	
	var th1, th2, conv, bgColor;
	
	switch (typ) {

	case 1:
		th1 = "Miles";
		th2 = "Kilometers";
		break;

	case 2:
		th1 = "Fahrenheit";
		th2 = "Celsius";
		break;

	case 3:
		th1 = "Pounds"; 
		th2 = "Grams";
		break;

	case 4:
		th1 = "Gallons";
		th2 = "Liters";
		break;

	case 5:
		th1 = "Feet";
		th2 = "Meters";
	}			

	document.write("<table><tr><th>" + th1 + "</th><th>" + th2 + "</th></tr>\n");

	for (var i = beg; i <= end; i++) {
		
		switch (typ) {

			case 1:
				conv = i * 1.60934;
				bgColor = "#dde";
				break;
	
			case 2:
				conv = (i-32)*(5/9);
				bgColor = "#ded";
				break;
				
			case 3:
				conv = i * 453.592;
				bgColor = "#dee";
				break;

			case 4:
				conv = i * 3.8752;
				bgColor = "#ddd";
				break;
				
			case 5:
				conv = i * 0.3048;
				bgColor = "#dde";
				break;

		}			

		document.write("<tr><td>" + i + "</td><td>" + conv.toFixed(1) + "</td></tr>");
		
	}

	document.write("</table>");

}

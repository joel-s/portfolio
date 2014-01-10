
days = [ "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday" ];

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];


function showDate() {
	now = new Date();
	document.write(formatDate(now));
}

function formatDate(date) {
	day = date.getDay();
	mth = date.getMonth(); 
	return days[day] + ", " + months[mth] + " " + date.getDate() + ", " + date.getFullYear();
}


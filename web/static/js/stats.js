$(document).ready(function() {
	var d1 = [[0,3],[4,7],[8,5],[9,13]];
	$.each($(".cube"), function(i, cube) {
		alert("Run "+i);
		$(cube).children("#graph-placeholder").plot([d1]);
	});
});


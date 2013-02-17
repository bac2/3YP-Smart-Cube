function updateProfile(profile_id, cube_id) {
	$.post("/settings/cube?pid="+profile_id+"&cid="+cube_id, function(data) {
		document.getElementById("pname" + cube_id).innerHTML = data
	});
	document.getElementById("pname" + cube_id).innerHTML = "...";
}

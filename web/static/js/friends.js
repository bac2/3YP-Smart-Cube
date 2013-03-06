$(document).ready(function () {
	$.each($(".cube"), function(i, cube) {
		footer = $(cube).find(".modal-footer");
		footer.children(".btn-primary").click(createEvent);
	});

	$("#addfriend").children("button").click(addFriend);
});

function createEvent() {
	cube = $(this).parents(".cube");
	cube_id = cube.attr("cube_id");

	side = cube.find("#side_select").val();
	action = cube.find("#action_select").val();
	profile_id = cube.find("#action_select").attr("profile_id")

	$.post("/settings/event/"+cube_id+"?side="+side+"&action="+action+"&profile_id="+profile_id, function(data) {
			if(data == "success") {
				return;
			}
		});
}

function addFriend() {
	email = $(this).parent().children("label").children("input").val()
		$.post("/friends/add?email="+email, function(data) {
			if(data == "success") {
				$("#friendresult").html("Success!");
			} else {
				$("#friendresult").html("Email not found!");
			}
			$("#friendresult").show()
			setTimeout(function() {
				$("#friendresult").fadeOut(1000);
			}, 2000);
		});
}

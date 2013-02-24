function updateProfile(profile_id, cube_id) {
	console.log(profile_id);
	$.post("/settings/cube?pid="+profile_id+"&cid="+cube_id, function(data) {
		$("#pname" + cube_id).html(data);
	});
	$("#pname" + cube_id).html("...");
}

function delete_profile() {
	profile = $(this).parent()
	profile_id = profile.attr("profile_id");

	$.post("/settings/profile/delete/"+profile_id, function(data) {
		if(data == "success") {
			$("#profile"+profile_id).remove();
		} else if (data == "profile in use") {
			alert("This profile is still in use!");
		}
	});
}

function post_edit() {
	var profile = $(this).parent()
	var profile_id = profile.attr("profile_id");

	var name = profile.find("#name").children().first().val();
	var desc = profile.children("#tagline").children().first().val();
	var s1 = profile.children("#side1").children().first().val();
	var s2 = profile.children("#side2").children().first().val();
	var s3 = profile.children("#side3").children().first().val();
	var s4 = profile.children("#side4").children().first().val();
	var s5 = profile.children("#side5").children().first().val();
	var s6 = profile.children("#side6").children().first().val();

	var url = '/settings/profile/edit/'+profile_id+'?name='+name+'&desc='+desc+'&s1='+s1+'&s2='+s2+'&s3='+s3+'&s4='+s4+'&s5='+s5+'&s6='+s6;
	$.post(url, function(data) {
		if(data == 'success') {
			return;
		} else {
			alert("Oops! The server made a mistake!");
		}
	});

	
	profile.children('#confirm').hide();
	profile.children('#edit').show();
	
	profile.find("span").each( function( i, child ) {
		$(child.firstChild).replaceWith($(child.firstChild).val());
	});
}

function edit_profile() {
	var profile = $(this).parent()
	var profile_id = profile.attr("profile_id");
	
	profile.children('#edit').hide();
	profile.children('#confirm').show();

	profile.wrap('<form id="profile_form'+profile_id+'" action="/settings/profile/edit/'+profile_id+'" method="post" />');
	profile.find("span").each( function(i, child) {
		$(child.firstChild).replaceWith('<input type="text" value="'+$(child).html()+'">');
	});

}

$(document).ready(function() {
	$.each( $('.profile'), function(i, profile) {
		$(profile).children("#edit").click( edit_profile );
		$(profile).children('#confirm').click( post_edit );
		$(profile).children('#confirm').hide();

		$(profile).children("#delete").click(delete_profile);
	});
});	

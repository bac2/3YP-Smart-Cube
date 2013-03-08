function updateProfile() {
	var cube = $(this).parents(".cube");
	var cube_code = cube.attr("cube_code");
	var profile_id = $(this).attr("profile_id");
	var dropdown_text = cube.find(".pname")
	$.post("/cube/"+cube_code+"/profile?profile_id="+profile_id, function(data) {
		dropdown_text.html(data);
	});
	dropdown_text.html("...");
}

function setPublic() {
	var cube = $(this).parents(".cube");
	var cube_id = cube.attr("cube_code");
	var value = ($(this).html() == "Yes") ? 1 : 0;
	var dropdown_text = cube.find(".public_state");
	$.post("/cube/"+cube_code+"/public?value="+value, function(data) {
		dropdown_text.html(data);
	});
	dropdown_text.html("...");
}

function delete_profile() {
	profile = $(this).parent()
	profile_id = profile.attr("profile_id");

	$.delete("/profile/"+profile_id, function(data) {
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

	var url = '/profile/'+profile_id+'?name='+name+'&desc='+desc+'&s1='+s1+'&s2='+s2+'&s3='+s3+'&s4='+s4+'&s5='+s5+'&s6='+s6;
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

	profile.wrap('<form id="profile_form'+profile_id+'" action="/profile/'+profile_id+'" method="post" />');
	profile.find("span").each( function(i, child) {
		$(child.firstChild).replaceWith('<input type="text" value="'+$(child).html()+'">');
	});

}

function delete_event() {
	var event_id= $(this).parent().attr("event_id");
	var event_item = $(this).parent();

	$.delete_("/events/"+event_id, function(data) {
		event_item.hide();
	});
}

$(document).ready(function() {
	$.each( $('.cube'), function( i, cube ) {
		
		$(cube).children(".active_profile").find("ul").find("a").each(function( i, ele ){
			$(ele).click( updateProfile );
		});
		$(cube).children(".public").find("ul").find("a").each( function( i, ele) {
			$(ele).click( setPublic );
		});
	});
	$.each( $('.profile'), function(i, profile) {
		$(profile).children("#edit").click( edit_profile );
		$(profile).children('#confirm').click( post_edit );
		$(profile).children('#confirm').hide();

		$(profile).children("#delete").click(delete_profile);
	});

	$.each( $('.event'), function(i, event_item) {
		$(event_item).children("#delete").click(delete_event);
	});
	$('.collapse').on( {
		shown: function() {
			$(this).css('overflow', 'visible');
		},
		hide: function() {
			$(this).css('overflow', 'hidden');
		}
	});
});	

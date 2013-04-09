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
	$.post("/cube/"+cube_id+"/public?value="+value, function(data) {
		dropdown_text.html(data);
	});
	dropdown_text.html("...");
}

function delete_profile() {
	var profile = $(this).parent();
	var name = profile.find("#name");
	var profile_id = profile.attr("profile_id");

	$.delete_("/profile/"+profile_id, function(data) {
		if(data == "success") {
			$(profile).remove();
			$(".cube").each(function(i, cube) {
				$(cube).find(".dropdown-menu").find("a").each(function(j, a) {
					if ( $(a).html() == name.html() ){
						$(a).parent().remove() //remove the li
					}
				});
			});
		} else if (data == "profile in use") {
			alert("This profile is still in use!");
		}
	});
}

function post_edit() {
	var profile = $(this).parent()
	var profile_id = profile.attr("profile_id");

	var old_name = profile.find("#name").children().first().attr("old")
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
			if(old_name != name) {
				$(".cube").each(function(i, cube) {
					$(cube).find(".dropdown-menu").find("a").each(function(j, a) {
						if($(a).html() == old_name) {
							$(a).html(name);
						}
					});
				});
			}
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
		$(child.firstChild).replaceWith('<input type="text" old="'+$(child).html()+'"value="'+$(child).html()+'">');
	});

}

function delete_event() {
	var event_id= $(this).parent().attr("event_id");
	var event_item = $(this).parent();

	$.delete_("/events/"+event_id, function(data) {
		event_item.hide();
	});
}

function create_profile() {
	var body = $(this).parent().siblings().last();
	var name = body.find("#p_name").val();
	var desc = body.find("#p_desc").val();
	var s1 = body.find("#p_s1").val();
	var s2 = body.find("#p_s2").val();
	var s3 = body.find("#p_s3").val();
	var s4 = body.find("#p_s4").val();
	var s5 = body.find("#p_s5").val();
	var s6 = body.find("#p_s6").val();

	$.post("/profile?name="+name+"&desc="+desc+"&s1="+s1+"&s2="+s2+"&s3="+s3+"&s4="+s4+"&s5="+s5+"&s6="+s6, function(data) {
		if(data == "failed") {
			alert("Server Error: Could not add profile.")
			return;
		} else {
			//Add it to each cube and put it in the profiles list
			$(".cube").each(function(i, cube) {
				$(cube).find(".active_profile").find("ul").append('<li><a tabindex="-1" profile_id="'+data+'" href="#">'+name+'</a></li>');
				$(cube).find(".active_profile").find("ul").find("a").last().click( updateProfile );
			});
			$(".profiles-collapse").children(".well").children("a").before(
				'<div class="profile" profile_id="'+data+'"> \
				<button type="button" id="delete" class="close">&times;</button>\
				<button type="button" id="edit" class="close">✎</button>\
				<button type="button" id="confirm" class="close">✔</button>\
				<strong><span id="name">'+name+'</span></strong><br/>\
				Tag line: <span id="tagline">'+desc+'</span><br/>\
				Side 1: <span id="side1">'+s1+'</span><br/>\
				Side 2: <span id="side2">'+s2+'</span><br/>\
				Side 3: <span id="side3">'+s3+'</span><br/>\
				Side 4: <span id="side4">'+s4+'</span><br/>\
				Side 5: <span id="side5">'+s5+'</span><br/>\
				Side 6: <span id="side6">'+s6+'</span><br/>\
				<br/>\
				</div>'
			);
			element = $(".profile").last();
			element.children("#confirm").hide();
			element.children("#edit").click( edit_profile );
			element.children("#confirm").click( post_edit );
			element.children("#delete").click( delete_profile );
			return;
		}
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

	$("#profile_create").find(".btn-primary").click( create_profile );

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

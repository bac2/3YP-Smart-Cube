$(document).ready(function() {
	setInterval(checkEvents, 30000);
	checkEvents();
	$('#notif-bar').click(handleEvent);
	$('#notif-bar')[0].notifications = [];
});


/* Extend jQuery with functions for PUT and DELETE requests. (homework.wsnet.de/releases/9132) */

function _ajax_request(url, data, callback, type, method) {
	    if (jQuery.isFunction(data)) {
		            callback = data;
			            data = {};
				        }
	        return jQuery.ajax({
			        type: method,
		               url: url,
		               data: data,
		               success: callback,
		               dataType: type
			        });
}

jQuery.extend({
	    put: function(url, data, callback, type) {
		            return _ajax_request(url, data, callback, type, 'PUT');
			        },
	    delete_: function(url, data, callback, type) {
		            return _ajax_request(url, data, callback, type, 'DELETE');
			        }
});

function checkEvents() {
	$.get("/events", function(data) {
		d = JSON.parse(data)
		if ( d.length > 0 ) {
			$.each(d, function( i, event_item) {
				audiotag = $('#notif')[0]
				audiotag.currentTime = 0;
			audiotag.play();

			var div = $('#notif-bar');

			div[0].notifications.push("<span event_id=\""+event_item.event_id+"\">Event: "+event_item.name+" is now "+ event_item.side_name+"!</span>");
			div.html(div[0].notifications[0]);
			});
		}
	});
}

function handleEvent() {
	this.notifications.pop();
	event_id = $(this).children().first().attr("event_id");
	$.post("/events/"+event_id, function(data) {});
	if(this.notifications.length > 0) {
		$(this).html( this.notifications[0] );
	} else {
		$(this).html( "" );
	}
}

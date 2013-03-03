$(document).ready(function() {
	setInterval(checkEvents, 30000);
	checkEvents();
	$('#notif-bar').click(handleEvent);
	$('#notif-bar')[0].notifications = [];
});

function checkEvents() {
	$.get("/events/web", function(data) {
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
	$.post("/events/web/"+event_id, function(data) {});
	if(this.notifications.length > 0) {
		$(this).html( this.notifications[0] );
	} else {
		$(this).html( "" );
	}
}

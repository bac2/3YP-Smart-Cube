//cubes_data is globally set in the generated html

function time_sort(a, b) {
	if( new Date(a.time) > new Date(b.time) ) {
		return 1;
	} else {
		return 0;
	}
}

$(document).ready(function() {
	$.each($(".cube"), function(i, cube) {
		var cubes_data = [];
		$.post("/statistics/"+ $(cube).attr("cube_id"), function(data) {
			if( data.length > 0) {
				cubes_data = JSON.parse(data);
			}
		
			cubes_data.sort(time_sort);	
	
			var graph_labels = {};
			var total_time = 0;
			$(cubes_data).each( function (i, transition) {
				
				var to_date = new Date();
				if( i != cubes_data.length-1 ) {
					to_date = new Date(cubes_data[i+1].time);
				}
				var time_delta = to_date - new Date(transition.time);
				transition.time_delta = time_delta / 1000; //MILLI TO SECS
				
				total_time += time_delta;
				
				if(graph_labels.hasOwnProperty(transition.side_name)) {
					label = graph_labels[transition.side_name];
					label.data = label.data + time_delta/1000;
				} else {
					graph_labels[transition.side_name] = { label: transition.side_name, data: time_delta/1000, color: "#4572A7"};
				}
			});
			
			var graph_data = [];
			for (var label in graph_labels) {	
				graph_data.push(graph_labels[label])
			}
	
			$(cube).children("#graph-placeholder").plot(graph_data, {
				series: {
					pie: {
						show: true
					}
				},
				legend: {
					labelBoxBorderColor: "none"
				}
			});
		});
	});
});


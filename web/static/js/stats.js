//cubes_data is globally set in the generated html

function time_sort(a, b) {
	if( new Date(a.time) > new Date(b.time) ) {
		return 1;
	} else {
		return -1;
	}
}

$(document).ready(function() {
	$.each($(".cube"), function(i, cube) {
		$.get("/statistics/"+ $(cube).attr("cube_id"), function(data) {
			var cubes_data = [];
			if( data.length > 0) {
				cubes_data = JSON.parse(data);
			}
		
			cubes_data.sort(time_sort);	
	
			var graph_labels = {};
			var colors = ['#4572A7', '#80699B', '#AA4643', '#3D96AE', '#89A54E', '#23D53C', '#53D21A']
			$(cubes_data).each( function (i, transition) {
				
				if (transition.side_name == null) {
					transition.side_name= "Unknown";
				}
				var to_date = new Date();
				if( i != cubes_data.length-1 ) {
					to_date = new Date(cubes_data[i+1].time);
				}
				var time_delta = to_date - new Date(transition.time);
				transition.time_delta = time_delta / 1000; //MILLI TO SECS
				
				if(graph_labels.hasOwnProperty(transition.side_name)) {
					label = graph_labels[transition.side_name];
					label.data = label.data + time_delta/1000;
				} else {
					graph_labels[transition.side_name] = { label: transition.side_name, data: time_delta/1000, color: colors[transition.position]};
				}
			});
			
			var graph_data = [];
			for (var key in graph_labels) {	
				graph_data.push(graph_labels[key]);
			}

				

			$(cube).children(".graph-placeholder").plot(graph_data, {
				series: {
					pie: {
						show: true,
						combine: {
							color: '#999',
							threshold: 0.03
							
						},
						label: {
							show: true,
							radius: 2/3,
							formatter: function(label, series) {
								time = series.data[0][1];
								var days = Math.floor(time / (3600*24));
								time %= 3600*24;
				
								var hours = Math.floor(time / 3600);
								if(hours < 10) hours = "0"+hours;
								time %= 3600;
						
								var minutes = Math.floor(time / 60);
								if(minutes < 10) minutes = "0"+minutes;
								time %= 60;
						
								var seconds = Math.floor(time);
								if(seconds < 10) seconds = "0"+seconds;
								return '<div style="font-sizew:11px; text-align:center; color: white; padding:2px;">'+label+'<br/>'+days+' days '+hours+':'+minutes+':'+seconds+'<br/>'+Math.round(series.percent)+'%</div>';
							},
							background: {
								opacity: 0.8,
								color: '#444'
							}
						}
					},
				},
				grid: {
					hoverable: true
				},
				legend: {
					show: false
				}
			})

		});
	});
});



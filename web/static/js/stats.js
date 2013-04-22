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
		$(cube).find("ul").children().children().each(function(i, link) {
			$(link).click(generateNewGraph);
			if( i == 0 ) {
				$(link).click();
			}
		});
	});
});

function generateNewGraph() {
	var cube = $(this).parents(".cube");
	var cube_code = cube.attr("cube_code");
	var profile_transition_id = $(this).attr("profile_transition_id");
	//Grab the div
	var graph_div = $(cube).children(".profile_transition");
	//Set the attribute
	graph_div.attr("profile_transition_id", profile_transition_id);
	//Get the data
	$.get("/cube/"+cube_code+"/transitions/profile-transition/"+profile_transition_id, function(data) {
		var cubes_data = [];
		if( data.length > 0) {
			cubes_data = JSON.parse(data);
		} 
		if( cubes_data.length > 0 ) {
			generatePie(graph_div, cubes_data);
			generateGantt(graph_div, cubes_data);
			$(graph_div).show();
			$(cube).children(".error").hide();
			$(graph_div).find(".pieLabelBackground").each(function(i, background) {
				$(background).css("height", "64px").css("width", "84px");
			});
		} else {	
			$(cube).children(".error").show();
			$(graph_div).hide();
		}
	});
	var name = $(this).html();
	$(this).parents(".btn-group").children().first().html(name + ' <span class="caret"></span>');
}

function formatterFunction(label, series) {
	var time = series.data[0][1];
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
	return '<div style="font-size:11px; text-align:center; color: white; padding:2px;">'+label+'<br/>'+days+' days '+hours+':'+minutes+':'+seconds+'<br/>'+Math.round(series.percent)+'%</div>';
}

function generatePie(parent_div, cubes_data) {

	cubes_data.sort(time_sort);	

	var graph_labels = {};
	var colors = ['#4572A7', '#80699B', '#AA4643', '#3D96AE', '#89A54E', '#23D53C', '#53D21A'];

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

	$(parent_div).children(".pie-placeholder").plot(graph_data, {
		series: {
			pie: {
				show: true,
		combine: {
			color: '#999',
		threshold: 0.03

		},
		label: {
			show: true,
		radius: 4/5,
		formatter: formatterFunction,
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

}

function generateGantt(parent_div, cubes_data) {

	var data_array = []	
	var names = {}
	$(cubes_data).each( function (i, transition) {
		var data_item = []

		if (transition.side_name == null) {
			transition.side_name= "Unknown";
		}
	names[transition.position] = transition.side_name;
	var to_date = new Date();
	if( i != cubes_data.length-1 ) {
		to_date = new Date(cubes_data[i+1].time);
	}
	var data_item = [ new Date(transition.time), transition.position, to_date, "Transition" ];
	data_array.push(data_item);

	});
	
	//Required to convince it to show the last one
	var fake_data_item = [new Date(), 0, new Date(), "Fake"];
	data_array.push(fake_data_item);

	var ticks = []
		for( var key in names ) {
			ticks.push( [key, names[key]] );
		}
	var graph_data = [ { label:"states", data:data_array } ];

	$(parent_div).children(".gantt-placeholder").plot(graph_data, {
		series: {
			gantt: {
				active: true,
		show: true,
		barHeight: 1.0
			},
		nearBy: {},
		grid:	{ hoverable:true, clickable:true }

		},
		xaxis:  { mode: "time" },
		yaxis:  { min: -0.5, max: 6.5, ticks: ticks }
	});

}

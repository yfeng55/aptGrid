document.addEventListener('DOMContentLoaded', function(){


	// set up price slider
	$('.nstSlider').nstSlider({
        "left_grip_selector": ".leftGrip",
        "right_grip_selector": ".rightGrip",
        "value_bar_selector": ".bar",
        "highlight": {
            "grip_class": "gripHighlighted",
            "panel_selector": ".highlightPanel"
        },
        "value_changed_callback": function(cause, leftValue, rightValue) {
            $('.leftLabel').text("$" + leftValue);
            $('.rightLabel').text("$" + rightValue);
        },
    });

	// set up map
	mapboxgl.accessToken = 'pk.eyJ1IjoieWY4MzMiLCJhIjoiY2l3dHJ0ZTFkMDB6czJ0cWIxaWx2cmRhZyJ9.KYsJM4PxLOiC2dEwkjUf6w';
	var map = new mapboxgl.Map({
	    container: 'map',
	    style: 'mapbox://styles/mapbox/light-v9',
	    center: [-73.9654, 40.7829],
	    zoom: 11
	});







}, false);
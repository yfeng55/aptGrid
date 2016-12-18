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



	//bind an event listener to all search fields
	$('.searchinput').on("keydown", function(event){
		if(event.which == 13){

			var neighborhood_input = $(".neighborhood").val();
			var numbedrooms_input = $(".numbedrooms").val();
			var numbathrooms_input = $(".numbathrooms").val();
			var price_high = $(".rightLabel").text();
			var price_low = $(".leftLabel").text();

			// alert("new search:\n" + neighborhood_input + "\n" + numbedrooms_input + "\n" + numbathrooms_input + "\n" + price_low + "\n" + price_high);
			
			var request_url = "/listings?hood=" + neighborhood_input + "&numbedrooms=" + numbedrooms_input + "&numbathrooms=" + numbathrooms_input + "&pricelow=" + price_low + "&pricehigh=" + price_high;
			// alert(request_url);

			$.get(request_url, function(response){
				console.log(response);

				for(var i=0; i<response.length; i++){
					var lat_val = response[i]['latitude'];
					var lng_val = response[i]['longitude']

					var marker = new mapboxgl.Marker().setLngLat([lng_val, lat_val]).addTo(map);
					console.log(marker);
				}
			}.bind(this));
		}
	}.bind(this));




}, false);
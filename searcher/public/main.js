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

	// create color scale function
	var colorscale = d3.scale.linear()
		.domain([-1000, 1000])
		.range(["blue", "red"]);

	//get neighborhood stats
	var neighborhood_stats;
	$.get("/neighborhoods", function(response){
		neighborhood_stats = response;
	}.bind(this));


	//bind an event listener to all search fields
	$('.searchinput').on("keydown", function(event){
		if(event.which == 13){

			var neighborhood_input = $(".neighborhood").val();
			var numbedrooms_input = $(".numbedrooms").val();
			var numbathrooms_input = $(".numbathrooms").val();
			var price_high = $(".rightLabel").text();
			var price_low = $(".leftLabel").text();
			
			var request_url = "/listings?hood=" + neighborhood_input + "&numbedrooms=" + numbedrooms_input + "&numbathrooms=" + numbathrooms_input + "&pricelow=" + price_low + "&pricehigh=" + price_high;


			console.log(neighborhood_stats);
			$.get(request_url, function(response){

				// clear markers
				$(".mapboxgl-marker").remove();

				for(var i=0; i<response.length; i++){
					var lat_val = response[i]['latitude'];
					var lng_val = response[i]['longitude']

					//get price difference from neighborhood avg
					var price_diff = 0.0;
					for(var j=0; j<neighborhood_stats.length; j++){
						if( neighborhood_stats[j]['name'] == (response[i]['neighborhood']+"_"+response[i]['num_beds']) ){
							price_diff = response[i]['price'] - neighborhood_stats[j]['avg_price'];
							break;
						}
					}

					var listing_text = "<b>" + response[i]['title'] + "</b><br/>";
					listing_text += "<b>Price:  </b>$" + response[i]['price'] + "\t<em>(" + price_diff + ")</em><br/>";
					listing_text += response[i]['num_beds'] + "Bedrooms\t" + response[i]['num_baths'] + "Bathrooms<br/>";
					listing_text += "<em><a target='_blank' href='" + response[i]['link'] + "'>source: " + response[i]['link'].split(".")[1] + "</a></em>";

					var popup = new mapboxgl.Popup({offset:[0, -30]}).setHTML(listing_text);

					var el = document.createElement('div');
					el.className = 'mapboxgl-marker';
					el.style.backgroundColor = colorscale(price_diff);

					var marker = new mapboxgl.Marker(el).setLngLat([lng_val, lat_val]).setPopup(popup).addTo(map);
				}
			}.bind(this));
		}
	}.bind(this));

	



}, false);
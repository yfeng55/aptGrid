const express = require('express');
const exphbs  = require('express-handlebars');
const dbconfig = require('./config/db');
const path = require('path');
const MongoClient = require('mongodb').MongoClient
const cors = require('cors')
const app = express();


// enable CORS
app.use(cors())

// set view engine
app.engine('handlebars', exphbs({defaultLayout: 'mainlayout'}));
app.set('view engine', 'handlebars');

// set static directory
app.use(express.static('public/'));


// connect to database
var db;
MongoClient.connect(dbconfig.remoteurl, function (err, database){
	if(err){ console.log(err)}

	db = database;
	app.listen(process.env.PORT || 5000, function(){ console.log('listening on 5000') })
});


///// ROUTES /////

//return search page
app.get('/', function (req, res) {
    res.render('index');
});


//get all apartment listings
app.get('/listings', function(req, res) {

	console.log("----- NEW REQUEST -----");
	console.log(req.query);

	var query = {};
	if(req.query.hood){
		query['neighborhood'] = req.query.hood;
	}
	if(req.query.source){
		query['link'] = { "$regex": req.query.source, "$options": "i" };
	}


	if(req.query.numbedrooms){
		query['num_beds'] = parseInt(req.query.numbedrooms);
	}
	if(req.query.numbathrooms){
		query['num_baths'] = parseInt(req.query.numbathrooms);
	}
	if(req.query.pricelow && req.query.pricehigh){
		var pricelow_str = req.query.pricelow.replace(/\D/g,'');
		var pricehigh_str = req.query.pricehigh.replace(/\D/g,'');
		query['price'] = {"$gte": parseInt(pricelow_str), "$lt": parseInt(pricehigh_str)};
	}


	console.log("----- QUERY -----");
	console.log(query);

	db.collection('listings').find(query).toArray(function(err, results) {
		res.send(results);
	})
});


//get neighborhood stats
app.get('/neighborhoods', function(req, res) {

	db.collection('neighborhoods').find({}).toArray(function(err, results) {
		res.send(results);
	})
});













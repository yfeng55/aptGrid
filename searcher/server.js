const express = require('express');
const dbconfig = require('./config/db');
const path = require('path');
const MongoClient = require('mongodb').MongoClient
const cors = require('cors')
const app = express();


// enable CORS
app.use(cors())


// connect to database
var db;
MongoClient.connect(dbconfig.remoteurl, function (err, database){
	if(err){ console.log(err)}

	db = database;
	app.listen(3000, function(){ console.log('listening on 3000') })
});


///// ROUTES /////
//get all apartment listings
app.get('/listings', function(req, res) {

	var query = {};
	if(req.query.hood){
		query['neighborhood'] = req.query.hood;
	}
	if(req.query.source){
		query['link'] = { "$regex": req.query.source, "$options": "i" };
	}
	
	console.log(query);

	db.collection('listings').find(query).toArray(function(err, results) {
		res.send(results);
	})
});












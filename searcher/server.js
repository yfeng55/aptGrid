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

//root path: serve the landing page
app.get('/', function(req, res) {
	// res.sendFile(__dirname + '/index.html')
	res.send("INDEX ROUTE");
});


//get aggregate player stats
app.get('/apt_listings', function(req, res) {
	db.collection('apt_listings').find().toArray(function(err, results) {
		res.send(results);
	})
});










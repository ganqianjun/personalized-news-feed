var cors = require('cors');
var express = require('express');
var path = require('path');

var index = require('./routes/index');
var news = require('./routes/news');

var app = express();

// view engine setup
app.set('views', path.join(__dirname, '../pnf-client/build/'));
app.set('view engine', 'jade');

app.use('/static', express.static(path.join(__dirname, '../pnf-client/build/static/')));

// TODO: remove this after development is done.
app.use(cors());

app.use('/', index);
app.use('/news', news);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  res.send('404 Not Found');
});

module.exports = app;

const mongoose = require('mongoose');

// uri comes from config
module.exports.connect = (uri) => {
  mongoose.connect(uri);

  mongoose.connection.on('error', (err) => {
    console.error('Main.js - Mongoose connection error: ' + err);
    process.exit(1);
  });

  // load models
  require('./user');
};

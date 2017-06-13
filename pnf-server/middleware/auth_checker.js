const jwt = require('jsonwebtoken');
const User = require('mongoose').model('User');
const config = require('../config/config.json');

// to check whether the request has token
module.exports = (req, res, next) => {
  console.log('auth_checker.js: req: ' + req.headers);

  if (!req.headers.authorization) {
    return res.status(401).end();
  }

  // get the last part from a authorization header string like "bearer token-value"
  const token = req.headers.authorization.split(' ')[1];

  console.log('auth_checker.js: token: ' + token);

  // decode the token using a secret key-phrase
  return jwt.verify(token, config.jwtSecret, (err, decoded) => {
    // return 401 code if it's unauthorized status
    if (err) {
      return res.status(401).end();
    }

    const id = decoded.sub;

    // check if a user exists
    return User.findById(id, (userErr, user) => {
      if (userErr || !user) {
        return res.status(401).end();
      }

      return next();
    });
  });
};

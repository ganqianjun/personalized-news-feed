const config = require('../config/config.json');
const jwt = require('jsonwebtoken');
const PassportLocalStrategy = require('passport-local').Strategy;
const User = require('mongoose').model('User');

// usernameField and passwordField need to match
// the 'name'(Line 20) and 'password' (Line 27) in LoginForm.js
// the first param is an object, the second param is a callback function
module.exports = new PassportLocalStrategy({
  usernameField: 'email',
  passwordField: 'password',
  passReqToCallback: true
}, (req, email, password, done) => {
  const userData = {
    email: email.trim(),
    password: password.trim()
  };

  // find a user by email address
  return User.findOne({ email: userData.email }, (err, user) => {
    if (err) {
      return done(err);
    }

    // if user doesn't exist, return error
    if (!user) {
      const error = new Error('Incorrect email or password');
      error.name = 'IncorrectCredentialsError';
      return done(error);
    }

    // check if a hashed user's password is equal to a value saved in the database
    return user.comparePassword(userData.password, (passwordErr, isMatch) => {
      if (err) {
        return done(err);
      }

      // isMatch comes from the callbak of function 'comparePassword' (user.js)
      if (!isMatch) {
        const error = new Error('Incorrect email or password');
        error.name = 'IncorrectCredentialsError';

        return done(error);
      }

      // use user._id of mongoose for user in token
      const payload = {
        sub: user._id
      };

      // create a token string
      const token = jwt.sign(payload, config.jwtSecret);
      const data = {
        name: user.email
      };

      return done(null, token, data);
    });
  });
});

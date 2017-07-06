import React, {PropTypes} from 'react';

import Auth from '../Auth/Auth';
import LoginForm from './LoginForm';

class LoginPage extends React.Component {
  constructor(props, context) {
    super(props, context);

    this.state = {
      errors: {},
      user: {
        email: '',
        password: ''
      }
    };

    this.processForm = this.processForm.bind(this);
    this.changeUserInformation = this.changeUserInformation.bind(this);
  }

  processForm(event) {
    event.preventDefault();

    const email = this.state.user.email;
    const password = this.state.user.password;

    console.log('LoginPage : email - ' + email);
    console.log('LoginPage : password - ' + password);

    // post login data and handle response
    fetch('http://localhost:3000/auth/login', {
      method: 'POST',
      cache: false,
      headers: {
        'Accept': 'application/json',
        'Content-type': 'application/json',
      },
      body: JSON.stringify({
        email: this.state.user.email,
        password: this.state.user.password
      })
    })
    .then(response => {
      if (response.status === 200) {
        this.setState({
          errors: {}
        });

        response.json().then(function(json) {
          console.log('LoginPage : json - ' + json);
          Auth.authenticateUser(json.token, email);
          // jump to the root page
          this.context.router.replace('/');
        }.bind(this));
      }
      else {
        response.json().then(function(json) {
          const errors = json.errors ? json.errors : {};
          errors.summary = json.message;
          console.log('LoginPage : Login Failed - ' + this.state.errors);
          this.setState({
            errors
          });
        }.bind(this));
      } // end of if..else..
    }); // end of fetch
  }

  changeUserInformation(event) {
    // this function is for when user email or password is changed
    const field = event.target.name; // email or password
    const user = this.state.user;
    user[field] = event.target.value;

    // don't forget to setState
    this.setState({
      user
    });
  }

  render() {
    return (
      <LoginForm
        onSubmit={this.processForm}
        onChange={this.changeUserInformation}
        errors={this.state.errors}
      />
    );
  }
}

// To make react-router work
LoginPage.contextTypes = {
  router: PropTypes.object.isRequired
};


export default LoginPage;

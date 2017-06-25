import React, {PropTypes} from 'react';
import SignUpForm from './SignUpForm';

class SignUpPage extends React.Component {
  constructor(props, context) {
    super(props, context);

    this.state = {
      errors: {},
      user: {
        email: '',
        password: '',
        confirm_password: ''
      }
    };

    this.processForm = this.processForm.bind(this);
    this.changeUserInformation = this.changeUserInformation.bind(this);
  }

  processForm(event) {
    event.preventDefault();

    const email = this.state.user.email;
    const password = this.state.user.password;
    const confirm_password = this.state.user.confirm_password;

    console.log('SignUpPage : email - ' + email);
    console.log('SignUpPage : password - ' + password);
    console.log('SignUpPage : confirm_password - ' + password);

    if (password !== confirm_password) {
      return;
    }

    // post signup data and handle response
    // post registeration data
    fetch('http://localhost:3000/auth/signup', {
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
          console.log('SignUpPage : json - ' + json);
          // when signup, backend doesn't send token.
          // only gets the token when login. So jump to the login page
          this.context.router.replace('/login');
        }.bind(this));
      }
      else {
        response.json().then(function(json) {;
          const errors = json.errors ? json.errors : {};
          errors.summary = json.message;
          console.log('SignUpPage : Signup Failed - ' + this.state.errors);
          this.setState({
            errors
          });
        }.bind(this));
      } // end of if..else..
    }); // end of fetch
  }

  changeUserInformation(event) {
    const field = event.target.name;
    const user = this.state.user;
    user[field] = event.target.value;

    this.setState({
      user
    });

    if (this.state.user.password !== this.state.user.confirm_password) {
      const errors = this.state.errors;
      errors.password = "Password and Confirm Password don't match.";
      this.setState({errors});
    } else {
      const errors = this.state.errors;
      errors.password = '';
      this.setState({
        errors
      });
    }
  }

  render() {
    return (
      <SignUpForm
        onSubmit={this.processForm}
        onChange={this.changeUserInformation}
        errors={this.state.errors}
      />
    );
  }
}

// To make react-router work
SignUpPage.contextTypes = {
  router: PropTypes.object.isRequired
};

export default SignUpPage;

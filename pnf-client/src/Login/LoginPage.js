import React, {PropTypes} from 'react';

import LoginForm from './LoginForm';

class LoginPage extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      errors: {
        summary: 'Summary Error',
        email: 'Email isn\'t correct',
        password: 'Password isn\'t correct',
      },
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
    // Todo: post login data and handle response
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

export default LoginPage;

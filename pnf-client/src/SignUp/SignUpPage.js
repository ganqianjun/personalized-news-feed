import React, {PropTypes} from 'react';
import SignUpForm from './SignUpForm';

class SignUpPage extends React.Component {
  constructor(props) {
    super(props);

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

    // Todo : post signup data and handle response
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

export default SignUpPage;

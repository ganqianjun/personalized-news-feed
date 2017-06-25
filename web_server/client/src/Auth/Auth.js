class Auth {
  // because it's singleton, so use 'static'
  static authenticateUser(token, email) {
    localStorage.setItem('token', token);
    localStorage.setItem('email', email);
  }

  static isUserAuthenticated() {
    return localStorage.getItem('token') != null;
  }

  static deauthenticateUser() {
    localStorage.removeItem('token');
    localStorage.removeItem('email');
  }

  // when load more news, we need token
  static getToken() {
    return localStorage.getItem('token');
  }

  static getEmail() {
    return localStorage.getItem('email');
  }
}

export default Auth;

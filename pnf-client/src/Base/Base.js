import './Base.css';
import React, {PropTypes} from 'react';
import Auth from '../Auth/Auth';

// Base includes navigation bar and the web content
// the navbar should kepp the same
// but the page could be news, login form, signup form etc
const Base = ({children}) => (
  <div>
    <nav className="nav-bar indigo lighten-1">
       <div className="nav-wrapper">
         <a href="/" className="brand-logo">Personalized News Feed</a>
         <ul id="nav-mobile" className="right">
           {Auth.isUserAuthenticated() ?
             (<div>
                <li>{Auth.getEmail()}</li>
                <li><a href="/logout">Log Out</a></li>
              </div>)
              :
             (<div>
                <li><a href="/login">Log In</a></li>
                <li><a href="/signup">Sign Up</a></li>
              </div>)
           }
         </ul>
       </div>
     </nav>
   <br/>
   {children}
 </div>
)

Base.propTypes = {
  children: PropTypes.object.isRequired
}
export default Base;

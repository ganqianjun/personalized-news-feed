import './Base.css';
import React, {PropTypes} from 'react';
import { Link } from 'react-router';

import Auth from '../Auth/Auth';

// Base includes navigation bar and the web content
// the navbar should kepp the same
// but the page could be news, login form, signup form etc
const Base = ({children}) => (
  <div>
    <nav className="nav-bar blue lighten-1">
       <div className="nav-wrapper">
         <a href="/" className="brand-logo"> Personalized News Feed</a>
         <ul id="nav-mobile" className="right">
           {Auth.isUserAuthenticated() ?
             (<div>
                <li>{Auth.getEmail()}</li>
                <li><Link to="/logout">Log Out</Link></li>
              </div>)
              :
             (<div>
                <li><Link to="/login">Log in</Link></li>
                <li><Link to="/signup">Sign up</Link></li>
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

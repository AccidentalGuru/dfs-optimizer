import React, { Component } from 'react';
import { BrowserRouter as Router, Route, NavLink } from 'react-router-dom';
import Home from './Home';
import Login from './Login';
import AuthService from './AuthService';
import withAuth from './withAuth';
const Auth = new AuthService();

class Main extends Component {
  render() {
    return (
      <Router>
        <div>
          <h1>Simple SPA</h1>
          <ul className='header'>
            <li><NavLink exact to='/'>Home</NavLink></li>
            <li><NavLink to='/login'>Login</NavLink></li>
            <li>
              <button
                type="button"
                className="form-submit"
                onClick={this.handleLogout.bind(this)}>
                Logout
              </button>
            </li>
          </ul>
          <div className='content'>
            <Route exact path='/' component={Home}/>
            <Route exact path='/login' component={Login}/>
          </div>
        </div>
      </Router>
    );
  }

  handleLogout() {
    Auth.logout()
    this.props.history.replace('/login');
  }

}
 
export default withAuth(Main);

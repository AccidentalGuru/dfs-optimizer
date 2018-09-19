import React, { Component } from 'react';
import '../css/Login.css';
import AuthService from './AuthService';

class Login extends Component {
  constructor() {
    super();
    this.handleChange = this.handleChange.bind(this);
    this.handleFormSubmit = this.handleFormSubmit.bind(this);
    this.Auth = new AuthService();
  }

  componentWillMount() {
    if (this.Auth.loggedIn()) {
      this.props.history.replace('/');
    }
  }

  handleChange(e) {
    this.setState(
      {
        [e.target.name]: e.target.value
      }
    )
  }

  handleFormSubmit(e) {
    e.preventDefault();

    this.Auth.login(this.state.username, this.state.password)
    .then(res => {
      this.props.history.replace('/');
    })
    .catch(err => {
      alert(err);
    });
  }

  render() {
        return (
            <div className="center">
              <div className="card">
                <h1>Login</h1>
                <form>
                  <input
                    className="form-item"
                    placeholder="Username goes here..."
                    name="username"
                    type="text"
                    onChange={this.handleChange}
                  />
                  <input
                    className="form-item"
                    placeholder="Password goes here..."
                    name="password"
                    type="password"
                    onChange={this.handleChange}
                  />
                  <input
                    className="form-item"
                    value="SUBMIT"
                    type="submit"
                  />
                </form>
              </div>
            </div>
        );
    }
}

export default Login;

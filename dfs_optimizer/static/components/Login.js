import React, { Component } from 'react';
import '../styles/Login.css';
import AuthService from './AuthService';

class Login extends Component {
    constructor() {
        super();
        this.handleChange = this.handleChange.bind(this);
        this.handleFormSubmit = this.handleFormSubmit.bind(this);
        this.Auth = new AuthService();
        this.handleToRegister = this.handleToRegister.bind(this);
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
        );
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

    handleToRegister(e) {
        this.props.history.replace('/register');
    }

    render() {
        return (
            <form className="form-signin text-center" onSubmit={this.handleFormSubmit}>
                <h1 className="h3 mb-3 font-weight-normal">Please sign in</h1>
                <input
                    className="form-control"
                    placeholder="Username"
                    name="username"
                    type="text"
                    onChange={this.handleChange}
                />
                <input
                    className="form-control"
                    placeholder="Password"
                    name="password"
                    type="password"
                    onChange={this.handleChange}
                />
                <button className="btn btn-lg btn-primary btn-block" type="submit">Sign in</button>
                <a href="#" onClick={this.handleToRegister.bind(this)}>Register</a>
            </form>
        );
    }
}

export default Login;

import React, { Component } from 'react';
import '../styles/Login.css';
import AuthService from './AuthService';

class Register extends Component {
    constructor() {
        super();
        this.handleChange = this.handleChange.bind(this);
        this.handleFormSubmit = this.handleFormSubmit.bind(this);
        this.Auth = new AuthService();
        this.handleToLogin = this.handleToLogin.bind(this);
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

        this.Auth.register(this.state.email, this.state.username, this.state.password)
            .then(res => {
                this.props.history.replace('/login');
            })
            .catch(err => {
                alert(err);
            });
    }

    handleToLogin(e) {
        this.props.history.replace('/login');
    }

    render() {
        return (
            <form className="form-signin" onSubmit={this.handleFormSubmit}>
                <h1 className="h3 mb-3 font-weight-normal">Please register</h1>
                <input
                    className="form-control"
                    placeholder="Email"
                    name="email"
                    type="email"
                    onChange={this.handleChange}
                />
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
                <button className="btn btn-lg btn-primary btn-block" type="submit">Register</button>
                <a href="#" onClick={this.handleToLogin.bind(this)}>Back to login</a>
            </form>
        );
    }
}

export default Register;

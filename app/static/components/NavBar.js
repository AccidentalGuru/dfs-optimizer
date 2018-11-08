import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import AuthService from './AuthService';
const Auth = new AuthService();

class NavBar extends Component {
    constructor(props) {
        super(props);

        this.handleLogout = this.handleLogout.bind(this);
    }

    handleLogout() {
        Auth.logout();
        this.props.history.replace('/login');
    }

    render() {
        return (
            <ul>
                <li>
                    <Link to="/">
                        Home
                    </Link>
                </li>
                <li>
                    <a onClick={this.handleLogout.bind(this)}>
                        Logout
                    </a>
                </li>
            </ul>
        );
    }
}

export default NavBar;

import React, { Component } from 'react';
import '../styles/App.css';
import AuthService from './AuthService';
import NavBar from './NavBar';
import FileUpload from './FileUpload';
import withAuth from './withAuth';
const Auth = new AuthService();

class App extends Component {
    render() {
        return (
            <div class="text-center">
                <h2> Welcome {this.props.user.username}</h2>
            </div>
        );
    }
}

export default withAuth(App);

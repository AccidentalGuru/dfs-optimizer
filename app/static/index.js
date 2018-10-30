import 'bootstrap/dist/css/bootstrap.min.css';
import React from 'react';
import ReactDOM from 'react-dom';
import { Route, BrowserRouter as Router } from 'react-router-dom';
import App from './components/App';
import Login from './components/Login';
import Register from './components/Register';

ReactDOM.render(
    <Router>
        <div>
            <Route exact path='/' component={App} />
            <Route exact path='/login' component={Login} />
            <Route exact path='/register' component={Register} />
        </div>
    </Router>,
    document.getElementById('root')
);

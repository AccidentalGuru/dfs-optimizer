import React from 'react';
import ReactDOM from 'react-dom';
import { Route, BrowserRouter as Router } from 'react-router-dom';
import App from './components/App';
import Login from './components/Login';

ReactDOM.render(
    <Router>
        <div>
            <Route exact path='/' component={App} />
            <Route exact path='/login' component={Login} />
        </div>
    </Router>,
    document.getElementById('root')
);

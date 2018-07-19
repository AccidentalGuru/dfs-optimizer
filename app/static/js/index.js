var React = require('react');
var ReactDOM = require('react-dom');
//var $ = require('jquery');

var Hello = class Welcome extends React.Component {
  render() {
    return <h1>Hello, React</h1>;
  }
};

ReactDOM.render(<Hello />, document.getElementById('content'));

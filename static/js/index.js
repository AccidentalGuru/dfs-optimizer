var React = require('react');
var ReactDOM = require('react-dom');

var Hello = class Welcome extends React.Component {
  render() {
    return <h1>Hello, {this.props.name}</h1>;
  }
};

ReactDOM.render(<Hello />, document.getElementById('content'));

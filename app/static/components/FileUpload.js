import React, { Component } from 'react';
import '../styles/App.css';
import AuthService from './AuthService';
const Auth = new AuthService();

class FileUpload extends Component {
    constructor(props) {
        super(props);

        this.state = {
            projectionsURL: '',
            uploadStatus: false
        };

        this.handleUploadProjections = this.handleUploadProjections.bind(this);
    }

    componentWillMount() {
        if (!Auth.loggedIn()) {
            this.props.history.replace('/login');
        }
    }

    handleUploadProjections(e) {
        e.preventDefault();

        const data = new FormData();
        data.append('file', this.uploadInput.files[0]);

        Auth.fetch(`${Auth.domain}/api/upload`, {
            method: 'POST',
            headers: {'Authorization': 'Bearer ' + Auth.getToken()},
            body: data
        }).then(res => {
            res.json().then((body) => {
                this.setState({
                    projectionsURL: `${Auth.domain}/${body.file}`,
                    uploadStatus: true
                });
            });
        });
    }

    render() {
        return (
            <form onSubmit={this.handleUploadProjections}>
                <div>
                    <input ref={(ref) => { this.uploadInput = ref; }} type="file" />
                </div>
                <br />
                <div>
                    <button>Upload</button>
                </div>
            </form>
        );
    }
}

export default FileUpload;

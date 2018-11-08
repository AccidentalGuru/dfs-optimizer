import React, { Component } from 'react';
import '../styles/App.css';
import AuthService from './AuthService';
const Auth = new AuthService();

class FileUpload extends Component {
    constructor(props) {
        super(props);

        this.state = {
            projectionsURL: '',
        };

        this.handleUploadProjections = this.handleUploadProjections.bind(this);
    }

    handleUploadProjections(e) {
        e.preventDefault();

        const data = new FormData();
        data.appened('file', this.uploadInput.files[0]);
        data.append('filename', this.fileName.value);

        Auth.fetch(`${Auth.domain}/api/upload`, {
            method: 'POST',
            body: data
        }).then(res => {
            res.json().then((body) => {
                this.setState({ projectionsURL: `${Auth.domain}/${body.file}` });
            });
        });
    }

    render() {
        return (
            <form onSubmit={this.handleUploadImage}>
                <div>
                    <input ref={(ref) => { this.uploadInput = ref; }} type="file" />
                </div>
                <div>
                    <input ref={(ref) => { this.fileName = ref; }} type="text" placeholder="Enter the desired name of file" />
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

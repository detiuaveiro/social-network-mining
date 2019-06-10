import React from "react";
import {Row, Col } from 'reactstrap';
import axios from 'axios';

import {PanelHeader, Button} from "components";

class ExportData extends React.Component {

  downloadUsers() {
    axios.get('http://192.168.85.182:5000/twitter/users/export', {
        responseType: 'blob',
        timeout: 30000,
      })
    .then((response) => {
    })
  }

  downloadTweets() {
    axios.get('http://192.168.85.182:5000/twitter/tweets/export', {
        responseType: 'blob',
        timeout: 30000,
      })
    .then((response) => {
    })
  }

  downloadNetwork() {
    axios.get('http://192.168.85.182:5000/twitter/network/export', {
        responseType: 'blob',
        timeout: 30000,
      })
    .then((response) => {
    })
  }

  render() {
    return (
      <div>
        <PanelHeader
          size="sm"
          content={
            <div>
              <div className="header text-center">
                <h2 className="title">Create Tweet</h2>
              </div>
            </div>
          }
        />
        <div className="content text-center mt-5 pt-4">
            <Row>
                <Col xs={6} md={4}>
                    <Button color="primary" onClick={this.downloadUsers} size="lg">
                        Export Users
                    </Button>
                </Col>
                <Col xs={6} md={4}>
                    <Button color="primary" onClick={this.downloadTweets} size="lg">
                        Export Tweets
                    </Button>
                </Col>
                <Col xs={6} md={4}>
                    <Button color="primary" onClick={this.downloadNetwork} size="lg">
                        Export Network
                    </Button>
                </Col>
            </Row>
        </div>
      </div>
    );
  }
}

export default ExportData;

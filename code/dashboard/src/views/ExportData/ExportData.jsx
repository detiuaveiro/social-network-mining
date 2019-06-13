import React from "react";
import {Row, Col, Form, FormGroup, Label, Input } from 'reactstrap';
import axios from 'axios';
import download from 'downloadjs'

import {PanelHeader, Button} from "components";

class ExportData extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        formatUsers: "json",
        formatTweets: "json",
    }
    this.downloadUsers = this.downloadUsers.bind(this);
    this.downloadTweets = this.downloadTweets.bind(this);
  }
  handleFormatTweets = event => {
    this.setState({formatTweets: event.target.value});
  }

  handleFormatUsers = event => {
    this.setState({formatUsers: event.target.value});
  }

  downloadUsers() {
    axios.get('http://192.168.85.182:5000/twitter/users/export?type='+this.state.formatUsers, {
        responseType: 'blob',
        timeout: 30000,
      })
    .then((response) => {
        const content = response.headers['content-type'];
        download(response.data, "users."+this.state.formatUsers, content)
    })
  }

  downloadTweets() {
    axios.get('http://192.168.85.182:5000/twitter/tweets/export?type='+this.state.formatTweets, {
        responseType: 'blob',
        timeout: 30000,
      })
    .then((response) => {
        const content = response.headers['content-type'];
        download(response.data, "tweets."+this.state.formatTweets, content)
    })
  }

  downloadNetwork() {
    axios.get('http://192.168.85.182:5000/twitter/network/export', {
        responseType: 'blob',
        timeout: 30000,
      })
    .then((response) => {
        const content = response.headers['content-type'];
        download(response.data, "network.csv", content)
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
                <h2 className="title">Export Data</h2>
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
                  <Form>
                    <Label for="Users">Format:</Label>
                    <FormGroup required>
                        <FormGroup check className="form-check-radio" inline> 
                          <Label check>
                            <Input type="radio" name="formatUsers" value="json" checked={this.state.formatUsers === 'json'} onChange={this.handleFormatUsers} />{' '}
                            <span className="form-check-sign" />
                            JSON
                          </Label>
                        </FormGroup>
                        <FormGroup check className="form-check-radio" inline> 
                          <Label check>
                            <Input type="radio" name="formatUsers" value="csv" checked={this.state.formatUsers === 'csv'} onChange={this.handleFormatUsers} />{' '}
                            <span className="form-check-sign" />
                            CSV
                          </Label>
                        </FormGroup>
                    </FormGroup>
                  </Form>
                </Col>
                <Col xs={6} md={4}>
                  <Button color="primary" onClick={this.downloadTweets} size="lg">
                      Export Tweets
                  </Button>
                  <Form>
                    <Label for="Tweets">Format:</Label>
                    <FormGroup required>
                      <FormGroup check className="form-check-radio"inline> 
                        <Label check>
                          <Input type="radio" name="formatTweets" value="json" checked={this.state.formatTweets === 'json'} onChange={this.handleFormatTweets} />{' '}
                          <span className="form-check-sign" />
                          JSON
                        </Label>
                      </FormGroup>
                      <FormGroup check className="form-check-radio"inline> 
                        <Label check>
                          <Input type="radio" name="formatTweets" value="csv" checked={this.state.formatTweets === 'csv'} onChange={this.handleFormatTweets} />{' '}
                          <span className="form-check-sign" />
                          CSV
                        </Label>
                      </FormGroup>
                    </FormGroup>
                  </Form>
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

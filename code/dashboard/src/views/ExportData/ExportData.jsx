import React from "react";
import {Row, Col, Form, FormGroup, Label, Input, Card, CardHeader } from 'reactstrap';
import axios from 'axios';
import download from 'downloadjs'
import Select from 'react-select';
import {PanelHeader, Button} from "components";

class ExportData extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        formatUsers: "json",
        formatTweets: "json",
        fieldU: "all",
        fieldT: "all",
        fieldsUsersOpt: [
          {value:"contributors_enabled",label:"contributors_enabled"},
          {value:"default_profile",label:"default_profile"},
          {value:"default_profile_image",label:"default_profile_image"},
          {value:"description",label:"description"},
          {value:"favourites_count",label:"favourites_count"},
          {value:"follow_request_sent",label:"follow_request_sent"},
          {value:"followers_count",label:"followers_count"},
          {value:"following",label:"following"},
          {value:"friends_count",label:"friends_count"},
          {value:"has_extended_profile",label:"has_extended_profile"},
          {value:"id",label:"id"},
          {value:"id_str",label:"id_str"},
          {value:"lang",label:"lang"},
          {value:"listed_count",label:"listed_count"},
          {value:"location",label:"location"},
          {value:"name",label:"name"},
          {value:"notifications",label:"notifications"},
          {value:"profile_background_color",label:"profile_background_color"},
          {value:"profile_background_image_url",label:"profile_background_image_url"},
          {value:"profile_background_image_url_https",label:"profile_background_image_url_https"},
          {value:"profile_background_tile",label:"profile_background_tile"},
          {value:"profile_image_url",label:"profile_image_url"},
          {value:"profile_image_url_https",label:"profile_image_url_https"},
          {value:"profile_link_color",label:"profile_link_color"},
          {value:"profile_sidebar_border_color",label:"profile_sidebar_border_color"},
          {value:"profile_sidebar_fill_color",label:"profile_sidebar_fill_color"},
          {value:"profile_text_color",label:"profile_text_color"},
          {value:"profile_use_background_image",label:"profile_use_background_image"},
          {value:"protected",label:"protected"},
          {value:"screen_name",label:"screen_name"},
          {value:"statuses_count",label:"statuses_count"},
          {value:"suspended",label:"suspended"},
          {value:"url",label:"url"},
          {value:"verified",label:"verified"},
        ],
        fieldsUsers: [
          {value:"contributors_enabled",label:"contributors_enabled"},
          {value:"default_profile",label:"default_profile"},
          {value:"default_profile_image",label:"default_profile_image"},
          {value:"description",label:"description"},
          {value:"favourites_count",label:"favourites_count"},
          {value:"follow_request_sent",label:"follow_request_sent"},
          {value:"followers_count",label:"followers_count"},
          {value:"following",label:"following"},
          {value:"friends_count",label:"friends_count"},
          {value:"has_extended_profile",label:"has_extended_profile"},
          {value:"id",label:"id"},
          {value:"id_str",label:"id_str"},
          {value:"lang",label:"lang"},
          {value:"listed_count",label:"listed_count"},
          {value:"location",label:"location"},
          {value:"name",label:"name"},
          {value:"notifications",label:"notifications"},
          {value:"profile_background_color",label:"profile_background_color"},
          {value:"profile_background_image_url",label:"profile_background_image_url"},
          {value:"profile_background_image_url_https",label:"profile_background_image_url_https"},
          {value:"profile_background_tile",label:"profile_background_tile"},
          {value:"profile_image_url",label:"profile_image_url"},
          {value:"profile_image_url_https",label:"profile_image_url_https"},
          {value:"profile_link_color",label:"profile_link_color"},
          {value:"profile_sidebar_border_color",label:"profile_sidebar_border_color"},
          {value:"profile_sidebar_fill_color",label:"profile_sidebar_fill_color"},
          {value:"profile_text_color",label:"profile_text_color"},
          {value:"profile_use_background_image",label:"profile_use_background_image"},
          {value:"protected",label:"protected"},
          {value:"screen_name",label:"screen_name"},
          {value:"statuses_count",label:"statuses_count"},
          {value:"suspended",label:"suspended"},
          {value:"url",label:"url"},
          {value:"verified",label:"verified"},
        ],
        fieldUsersEmpty: false,
        fieldsTweetsOpt: [
          {value:"entities",label:"entities"},
          {value:"favorite_count",label:"favorite_count"},
          {value:"id",label:"id"},
          {value:"lang",label:"lang"},
          {value:"possibly_sensitive",label:"possibly_sensitive"},
          {value:"retweet_count",label:"retweet_count"},
          {value:"source",label:"source"},
          {value:"text",label:"text"},
          {value:"truncated",label:"truncated"},
          {value:"user",label:"user"},
          {value:"in_reply_to_screen_name",label:"in_reply_to_screen_name"},
          {value:"in_reply_to_status_id",label:"in_reply_to_status_id"},
          {value:"in_reply_to_user_id",label:"in_reply_to_user_id"},
          {value:"is_quote_status",label:"is_quote_status"},
          {value:"quoted_status_id",label:"quoted_status_id"},
        ],
        fieldsTweets: [
          {value:"entities",label:"entities"},
          {value:"favorite_count",label:"favorite_count"},
          {value:"id",label:"id"},
          {value:"lang",label:"lang"},
          {value:"possibly_sensitive",label:"possibly_sensitive"},
          {value:"retweet_count",label:"retweet_count"},
          {value:"source",label:"source"},
          {value:"text",label:"text"},
          {value:"truncated",label:"truncated"},
          {value:"user",label:"user"},
          {value:"in_reply_to_screen_name",label:"in_reply_to_screen_name"},
          {value:"in_reply_to_status_id",label:"in_reply_to_status_id"},
          {value:"in_reply_to_user_id",label:"in_reply_to_user_id"},
          {value:"is_quote_status",label:"is_quote_status"},
          {value:"quoted_status_id",label:"quoted_status_id"},
        ],
        fieldTweetsEmpty: false,
    }
    this.downloadUsers = this.downloadUsers.bind(this);
    this.downloadTweets = this.downloadTweets.bind(this);
    this.downloadNetwork = this.downloadNetwork.bind(this);
  }
  handleFormatTweets = event => {
    this.setState({formatTweets: event.target.value});
  }

  handleFormatUsers = event => {
    this.setState({formatUsers: event.target.value});
  }

  handleFieldTweets = event => {
    this.setState({fieldT: event.target.value});
  }

  handleFieldUsers = event => {
    this.setState({fieldU: event.target.value});
  }

  downloadUsers() {
    if (this.state.fieldsUsers.length===0){
      this.setState({
        fieldUsersEmpty: true
      })
    }
    else if (this.state.fieldU==="all"){
      window.open('http://192.168.85.182:5000/twitter/users/export?type='+this.state.formatUsers, "_blank");
    }
    else if (this.state.fieldU==="not_all"){
      const b = []
      this.state.fieldsUsers.forEach(function (field){
        b.push(field['value'])
      })
      window.open('http://192.168.85.182:5000/twitter/users/export?type='+this.state.formatUsers+'&&fields='+b, "_blank");
    }
  }

  downloadTweets() {
    if (this.state.fieldsTweets.length===0){
      this.setState({
        fieldTweetsEmpty: true
      })
    }
    else if (this.state.fieldT==="all"){
      window.open('http://192.168.85.182:5000/twitter/tweets/export?type='+this.state.formatTweets, "_blank");
    }
    else if (this.state.fieldT==="all"){
      const b = []
      this.state.fieldsTweets.forEach(function (field){
        b.push(field['value'])
      })
      window.open('http://192.168.85.182:5000/twitter/tweets/export?type='+this.state.formatTweets+'&&fields='+b, "_blank");
    }

  }

  downloadNetwork() {
    window.open('http://192.168.85.182:5000/twitter/network/export', "_blank");
  }

  handleUserFields = (fieldsUsers) => {
    this.setState({ fieldsUsers, fieldUsersEmpty: false});
  }

  handleTweetFields = (fieldsTweets) => {
    this.setState({ fieldsTweets, fieldTweetsEmpty: false});
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
                <Col xs={12} md={12}>
                  <Card>
                    <CardHeader>
                      <h6>Users</h6>
                    </CardHeader>
                    <Form>
                      <Row>
                        <Col xs={12} md={6}>
                          <Label for="FormatUsers">Format:</Label>
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
                        </Col>
                        <Col xs={12} md={6}>
                          <Label for="FieldsUsers">Fields:</Label>
                          <FormGroup required>
                              <FormGroup check className="form-check-radio" inline> 
                                <Label check>
                                  <Input type="radio" name="fieldUsers" value="all" checked={this.state.fieldU === 'all'} onChange={this.handleFieldUsers} />{' '}
                                  <span className="form-check-sign" />
                                  All
                                </Label>
                              </FormGroup>
                              <FormGroup check className="form-check-radio" inline> 
                                <Label check>
                                  <Input type="radio" name="fieldUsers" value="not_all" checked={this.state.fieldU === 'not_all'} onChange={this.handleFieldUsers} />{' '}
                                  <span className="form-check-sign" />
                                  Select Fields
                                </Label>
                              </FormGroup>
                          </FormGroup>
                        </Col>
                      </Row>
                      <Col xs={12} md={12} hidden={(this.state.fieldU==="all" ? true : false)}>
                        <FormGroup required>
                          <Label>Fields:</Label>
                            <Select
                              value={this.state.fieldsUsers}
                              onChange={this.handleUserFields}
                              options={this.state.fieldsUsersOpt}
                              isMulti
                              isSearchable
                              isDisabled={(this.state.fieldU==="all") ? true : false}
                              placeholder="Add Fields"
                              styles={{
                                control: (provided,state) => ({
                                  ...provided,
                                  borderRadius: 30,
                                  borderColor: state.isFocused ? "#f96332" : "#E3E3E3",
                                  boxShadow: state.isFocused ? "#f96332" : "#E3E3E3",
                                  '&:hover': {
                                    borderColor: state.isFocused ? "#f96332" : "#E3E3E3",
                                    boxShadow: state.isFocused ? "#f96332" : "#E3E3E3",
                                  },
                                }),
                                multiValue: (provided, state) => ({
                                  ...provided,
                                  backgroundColor: "#f96332",
                                  color: "white",
                                  borderRadius: 30,
                                }),
                              }}
                              className="primary"

                            />
                            <div hidden={!this.state.fieldUsersEmpty} className="alert-danger mt-2 p-2" style={{borderRadius: 30}}>
                                Field can't be empty!
                            </div>
                        </FormGroup>
                      </Col>
                    </Form>
                    <Button color="primary" onClick={this.downloadUsers} size="lg">
                        Export Users
                    </Button>
                  </Card>
                </Col>
                <Col xs={12} md={12}>
                  <Card>
                    <CardHeader>
                      <h6>Tweets</h6>
                    </CardHeader>
                    <Form>
                      <Row>
                        <Col xs={12} md={6}>
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
                        </Col>
                        <Col xs={12} md={6}>
                          <Label for="FieldsTweets">Fields:</Label>
                          <FormGroup required>
                              <FormGroup check className="form-check-radio" inline> 
                                <Label check>
                                  <Input type="radio" name="fieldTweets" value="all" checked={this.state.fieldT === 'all'} onChange={this.handleFieldTweets} />{' '}
                                  <span className="form-check-sign" />
                                  All
                                </Label>
                              </FormGroup>
                              <FormGroup check className="form-check-radio" inline> 
                                <Label check>
                                  <Input type="radio" name="fieldTweets" value="not_all" checked={this.state.fieldT === 'not_all'} onChange={this.handleFieldTweets} />{' '}
                                  <span className="form-check-sign" />
                                  Select Fields
                                </Label>
                              </FormGroup>
                          </FormGroup>
                        </Col>
                      </Row>
                      <Col xs={12} md={12} hidden={(this.state.fieldT==="all" ? true : false)}>
                        <FormGroup required>
                          <Label>Fields:</Label>
                            <Select
                              value={this.state.fieldsTweets}
                              onChange={this.handleTweetFields}
                              options={this.state.fieldsTweetsOpt}
                              isMulti
                              isSearchable
                              isDisabled={(this.state.fieldT==="all") ? true : false}
                              placeholder="Add Fields"
                              styles={{
                                control: (provided,state) => ({
                                  ...provided,
                                  borderRadius: 30,
                                  borderColor: state.isFocused ? "#f96332" : "#E3E3E3",
                                  boxShadow: state.isFocused ? "#f96332" : "#E3E3E3",
                                  '&:hover': {
                                    borderColor: state.isFocused ? "#f96332" : "#E3E3E3",
                                    boxShadow: state.isFocused ? "#f96332" : "#E3E3E3",
                                  },
                                }),
                                multiValue: (provided, state) => ({
                                  ...provided,
                                  backgroundColor: "#f96332",
                                  color: "white",
                                  borderRadius: 30,
                                }),
                              }}
                              className="primary"

                            />
                            <div hidden={!this.state.fieldTweetsEmpty} className="alert-danger mt-2 p-2" style={{borderRadius: 30}}>
                                Field can't be empty!
                            </div>
                        </FormGroup>
                      </Col>
                    </Form>
                    <Button color="primary" onClick={this.downloadTweets} size="lg">
                        Export Tweets
                    </Button>
                  </Card>
                </Col>
                <Col xs={12} md={12}>
                  <Card>
                    <CardHeader>
                      <h6>Network</h6>
                    </CardHeader>
                    <Button color="primary" onClick={this.downloadNetwork} size="lg">
                        Export Network
                    </Button>
                  </Card>
                </Col>
            </Row>
        </div>
      </div>
    );
  }
}

export default ExportData;

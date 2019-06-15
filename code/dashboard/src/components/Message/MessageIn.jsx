import React from "react";
import { Card, CardBody, Row, Col } from 'reactstrap';
//import PropTypes from "prop-types";
import axios from 'axios';

class MessageIn extends React.Component {
  state = {
    message: this.props.message,
    sender_info: ""
  }

  componentDidMount() {
    console.log(this.props.message)
    axios.get('http://192.168.85.182:5000/twitter/users/'+this.props.message["sender_id"])
      .then(res => {
        const sender_info = res.data[0];
        this.setState({ sender_info });
      })
  }

  render() {
    return (
      <Card style={{minHeight:"230px",maxHeight:"230px",borderRadius:"50px"}}>
        <CardBody>
          <Row>
              <Col xs={12} md={6}>
                <img
                  className="avatar border-gray"
                  src={this.state.sender_info["profile_image_url_https"]}
                  alt=""
                />
              </Col>
              <Col className="text-center my-auto" xs={12} md={6}>
                <a target="_blank" rel="noopener noreferrer" href={"https://twitter.com/"+this.state.sender_info["screen_name"]}>
                  <h6 className="title">{this.state.sender_info["name"]}</h6>
                  <p className="description">@{this.state.sender_info["screen_name"]}</p>
                </a>
              </Col>
          </Row>
          <Row>
            <Col xs={12} md={12} style={{minHeight:"80px",maxHeight:"80px"}}>
              <p className="text-center">{this.state.message["text"]}</p>
            </Col>
          </Row>
        </CardBody>
      </Card>
    );
  }
}



export default MessageIn;

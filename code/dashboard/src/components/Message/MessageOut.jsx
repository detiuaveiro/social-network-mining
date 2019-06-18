import React from "react";
import { Card, CardBody, Row, Col } from 'reactstrap';

class MessageOut extends React.Component {
  state = {
    message: this.props.message,
    bot_info: this.props.bot,
  }

  componentDidMount() {
  }

  render() {
    return (
      <Card style={{minHeight:"230px",maxHeight:"230px",borderRadius:"50px",backgroundColor: "#c0deed"}}>
        <CardBody>
          <Row>
              <Col xs={12} md={6}>
                <img
                  className="avatar border-gray"
                  src={this.state.bot_info["profile_image_url_https"]}
                  alt=""
                />
              </Col>
              <Col className="text-center my-auto" xs={12} md={6}>
                <a target="_blank" rel="noopener noreferrer" href={"https://twitter.com/"+this.state.bot_info["screen_name"]}>
                  <h6 className="title">{this.state.bot_info["name"]}</h6>
                  <p className="description">@{this.state.bot_info["screen_name"]}</p>
                </a>
              </Col>
          </Row>
          <Row>
            <Col xs={12} md={12} style={{minHeight:"80px",maxHeight:"80px"}}>
              <p className="text-center">{this.state.message["text"]}</p>
            </Col>
          </Row>
          <Row>
            <Col xs={12} md={12}>
              <p className="text-muted">{new Date(this.state.message["created_at"])}</p>
            </Col> 
          </Row>
        </CardBody>
      </Card>
    );
  }
}



export default MessageOut;

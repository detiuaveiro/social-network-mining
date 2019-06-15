import React from "react";
import { Card, CardBody, CardFooter, Row, Col, Badge } from 'reactstrap';
import {CardInteractions, Button, RepliesModal } from 'components';// used for making the prop types of this component
import axios from 'axios';

class Tweet extends React.Component {
  constructor(props) {
    super(props);
    this.state ={
      user_info: {},
      modalReply: false,
    }
    this.toggleModalReply = this.toggleModalReply.bind(this);
  }

  componentDidMount() {
      axios.get('http://192.168.85.182:5000/twitter/users/'+this.props.info["user"])
      .then(res => {
        const user_info = res.data[0];
        this.setState({user_info});
      })
  }

  toggleModalReply() {
    this.setState({
        modalReply: !this.state.modalReply
    });
  }

  render() {
    return (
        <Card style={{minHeight:"300px",maxHeight:"300px"}}>
          <CardBody>
            <Row>
              <Col xs={12} md={2}>
                <img
                  className="avatar border-gray"
                  src={this.state.user_info["profile_image_url_https"]}
                  alt=""
                />
              </Col>
              <Col className="text-left my-auto" xs={12} md={7}>
                <h6 className="title">{this.state.user_info["name"]}</h6>
                <p className="description">{"@"+this.state.user_info["screen_name"]}</p>
              </Col>
              <Col xs={12} md={2}>
              <a target="_blank" rel="noopener noreferrer" href={"https://twitter.com/statuses/"+this.props.info["id"]}>
                  <Badge color="light">
                    <i class="fas fa-2x fa-external-link-alt"></i>
                  </Badge>
                </a>
              </Col>
            </Row>
            <Row>
              <Col xs={12} md={2}>
              </Col>
              <Col xs={12} md={10} style={{minHeight:"70",maxHeight:"70"}}>
                <p className="text-left">{this.props.info["text"]}</p>
              </Col>
            </Row>
            <Row>
              <Col xs={12} md={2}>
              </Col>
              <Col className="text-left my-auto" xs={12} md={4}>
                <CardInteractions
                  size="sm"
                  socials={[
                    {
                      tipo: "icon",
                      icon: "fas fa-heart",
                      number: this.props.info["favorite_count"],
                    },
                    {
                      tipo: "icon",
                      icon: "fas fa-retweet",
                      number: this.props.info["retweet_count"],
                    },
                  ]}
                />
              </Col>
              <Col className="text-left my-auto" xs={12} md={6}>
                <p className="description">{"ID: "+this.props.info["id"]}</p>
              </Col>
            </Row>
          </CardBody>
          <CardFooter style={{position: "absolute",bottom: 0}}>
            <Button color="primary" onClick={this.toggleModalReply}>
              Replies
            </Button>
          </CardFooter>
          <RepliesModal status={this.state.modalReply} handleClose={this.toggleModalReply} tweetID={this.props.info["id"]}></RepliesModal>
        </Card>
    );
  }
}



export default Tweet;

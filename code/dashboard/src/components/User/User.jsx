import React from "react";
import { Card, CardBody, Row, Col, Badge } from 'reactstrap';
import {CardNumbers } from 'components';// used for making the prop types of this component
//import PropTypes from "prop-types";
import axios from 'axios';

class UserInfo extends React.Component {
  state = {
    id: this.props.userid,
    user_info: ""
  }

  componentDidMount() {
    axios.get('http://192.168.85.182:5000/twitter/users/'+this.props.userid)
      .then(res => {
        console.log(res.data)
        const user_info = res.data[0];
        this.setState({ user_info });
      })
  }
  render() {
    return (
      <Card style={{minHeight:"250px",maxHeight:"250px"}}>
        <CardBody>
          <Row>
            <Col xs={12} md={4}>
              <img
                className="avatar border-gray"
                src={this.state.user_info["profile_image_url_https"]}
              />
            </Col>
            <Col className="text-center my-auto" xs={12} md={6}>
              <h6 className="title">{this.state.user_info["name"]}</h6>
              <p className="description">@{this.state.user_info["screen_name"]}</p>
            </Col>
            <Col xs={12} md={2}>
              <a target="_blank" rel="noopener noreferrer" href={"https://twitter.com/"+this.state.user_info["screen_name"]}>
                <Badge color="light">
                  <i class="fas fa-2x fa-external-link-alt"></i>
                </Badge>
              </a>
            </Col>
          </Row>
          <Row>
            <Col xs={12} md={12} style={{minHeight:"80px",maxHeight:"80px"}}>
              <p className="text-center">{this.state.user_info["description"]}</p>
            </Col>
          </Row>
          <Row>
            <Col xs={12} md={12}>
            <CardNumbers
                  size="sm"
                  socials={[
                    {
                      text: "Favourites",
                      number:this.state.user_info["favourites_count"]
                    },
                    {
                      text: "Following",
                      number:this.state.user_info["friends_count"]
                    },
                    {
                      text: "Followers",
                      number:this.state.user_info["followers_count"]
                    }
                  ]}
                />
            </Col>
          </Row>
        </CardBody>
      </Card>
    );
  }
}



export default UserInfo;

import React from "react";
import { Card, CardHeader, CardBody, Nav, NavItem, NavLink, Row, Col, Badge } from 'reactstrap';
import {CardInteractions } from 'components';// used for making the prop types of this component

class Tweet extends React.Component {
  render() {
    return (
        <Card style={{minHeight:"350px",maxHeight:"350px"}}>
          <CardHeader>
              <Nav tabs>
                  <NavItem>
                      <NavLink href="#" active>Tweet</NavLink>
                  </NavItem>
                  <NavItem>
                      <NavLink href="#">Stats</NavLink>
                  </NavItem>
              </Nav>
          </CardHeader>
          <CardBody>
            <Row>
              <Col xs={12} md={2}>
                <img
                  className="avatar border-gray"
                  src={this.props.info["profile_image_url_https"]}
                />
              </Col>
              <Col className="text-left my-auto" xs={12} md={4}>
                <h6 className="title">{this.props.info["name"]}</h6>
                <p className="description">{"@"+this.props.info["screen_name"]}</p>
              </Col>
              <Col xs={12} md={3}>
                <p className="description text-left">
                  {this.props.info["created_at"]}
                </p>
              </Col>
              <Col xs={12} md={2}>
                <a href={this.props.info["entities"]["urls"]["url"]}>
                  <Badge color="light">
                    <i class="fas fa-2x fa-external-link-alt"></i>
                  </Badge>
                </a>
              </Col>
            </Row>
            <Row>
              <Col xs={12} md={2}>
              </Col>
              <Col xs={12} md={10}>
                <p className="text-left">{this.props.info["text"]}</p>
              </Col>
            </Row>
            <Row>
              <Col xs={12} md={2}>
              </Col>
              <Col className="text-left my-auto" xs={12} md={5}>
                <CardInteractions
                  size="sm"
                  socials={[
                    {
                      icon: "fas fa-heart",
                      number: this.props.info["favorite_count"],
                    },
                    {
                      icon: "fas fa-retweet",
                      number: this.props.info["retweet_count"],
                    },
                  ]}
                />
              </Col>
              <Col className="text-center my-auto" xs={12} md={5}>
                <a>
                  <i class="fas fa-map-marker-alt"></i> {this.props.info["geo"]}
                </a>
              </Col>
            </Row>
          </CardBody>
        </Card>
    );
  }
}



export default Tweet;

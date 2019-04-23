import React from "react";
import { Card, CardHeader, CardBody, Nav, NavItem, NavLink, Row, Col, Badge } from 'reactstrap';
import {CardInteractions } from 'components';// used for making the prop types of this component
//import PropTypes from "prop-types";
import userAvatar from "assets/img/mike.jpg";

class Tweet extends React.Component {
  render() {
    return (
      <Card >
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
                src={userAvatar}
              />
            </Col>
            <Col className="text-left my-auto" xs={12} md={6}>
              <h6 className="title">Afonso Silva</h6>
              <p className="description">@afonsosilva01</p>
            </Col>
            <Col xs={12} md={2}>
              <p className="description text-left">
                23/4
              </p>
            </Col>
            <Col xs={12} md={2}>
              <a>
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
              <p className="text-left">O pai da Lara @brunobiancoleal sabe tudo sobre a #NovaPrevid\u00eancia. E aproveitou para esclarecer alguns fatos sobre\u2026</p>
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
                    number: 123,
                  },
                  {
                    icon: "fas fa-retweet",
                    number: 43,
                  },
                  {
                    icon: "fas fa-comments",
                    number: 12,
                  },
                ]}
              />
            </Col>
            <Col className="text-center my-auto" xs={12} md={5}>
              <a>
                <i class="fas fa-map-marker-alt"></i> Location
              </a>
            </Col>
          </Row>
        </CardBody>
      </Card>
    );
  }
}



export default Tweet;

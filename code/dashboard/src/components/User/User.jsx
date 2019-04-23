import React from "react";
import { Card, CardBody, Row, Col, Badge } from 'reactstrap';
//import PropTypes from "prop-types";
import userAvatar from "assets/img/mike.jpg";

class UserInfo extends React.Component {
  render() {
    return (
      <Card >
        <CardBody>
          <Row>
            <Col xs={12} md={4}>
              <img
                className="avatar border-gray"
                src={userAvatar}
              />
            </Col>
            <Col className="text-center my-auto" xs={12} md={6}>
              <h6 className="title">Afonso Silva</h6>
              <p className="description">@afonsosilva01</p>
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
            <Col xs={12} md={3}>
            </Col>
            <Col xs={12} md={9}>
              <p className="text-center">O pai da Lara @brunobiancoleal sabe tudo sobre a #NovaPrevid\u00eancia. E aproveitou para esclarecer alguns fatos sobre\u2026</p>
            </Col>
          </Row>
        </CardBody>
      </Card>
    );
  }
}



export default UserInfo;

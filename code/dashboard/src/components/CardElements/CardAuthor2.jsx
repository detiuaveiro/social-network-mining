import React from "react";
// used for making the prop types of this component
import {
  Row,
  Col,
} from "reactstrap";
import { Link } from 'react-router-dom'
import PropTypes from "prop-types";

class CardAuthor2 extends React.Component {
  render() {
    return (
      <div className="author">
        <Link to={this.props.link ? this.props.link : "/dashboard"}>
          <Row>
            <Col xs={12} md={4}>
              <img
                className="avatar border-gray"
                src={this.props.avatar}
                alt={this.props.avatarAlt}
              />
            </Col>
            <Col className="text-left my-auto" xs={12} md={8}>
              <h6 className="title">{this.props.title}</h6>
              <p className="description">{this.props.description}</p>
            </Col>
          </Row>
        </Link>
      </div>
    );
  }
}

CardAuthor2.propTypes = {
  // Where the user to be redirected on clicking the avatar
  link: PropTypes.string,
  avatar: PropTypes.string,
  avatarAlt: PropTypes.string,
  title: PropTypes.oneOfType([PropTypes.string, PropTypes.node]),
  description: PropTypes.oneOfType([PropTypes.string, PropTypes.node])
};

export default CardAuthor2;

import React from "react";
// used for making the prop types of this component
import { Link } from 'react-router-dom'
import PropTypes from "prop-types";

class CardAuthor extends React.Component {
  render() {
    return (
      <div className="author">
        <Link to={this.props.link ? this.props.link : "/bots/1"}>
          <img
            className="avatar border-gray"
            src={this.props.avatar}
            alt={this.props.avatarAlt}
          />
          <h5 className="title">{this.props.title}</h5>
        </Link>
        <p className="description">{this.props.description}</p>
      </div>
    );
  }
}

CardAuthor.propTypes = {
  // Where the user to be redirected on clicking the avatar
  link: PropTypes.string,
  avatar: PropTypes.string,
  avatarAlt: PropTypes.string,
  title: PropTypes.oneOfType([PropTypes.string, PropTypes.node]),
  description: PropTypes.oneOfType([PropTypes.string, PropTypes.node])
};

export default CardAuthor;

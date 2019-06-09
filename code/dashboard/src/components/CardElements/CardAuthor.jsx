import React from "react";
// used for making the prop types of this component
import PropTypes from "prop-types";

class CardAuthor extends React.Component {
  render() {
    return (
      <div className="author">
        <a target="_blank" rel="noopener noreferrer" href={"https://twitter.com/"+this.props.username}>
          <img
            className="avatar small border-gray"
            src={this.props.avatar}
            alt={this.props.avatarAlt}
          />
          <h5 className="title text-decoration-none" style={{color:"#f96332"}}>{this.props.title}</h5>
        </a>
        <p className="description text-decoration-none">@{this.props.username}</p>
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
  username: PropTypes.oneOfType([PropTypes.string, PropTypes.node])
};

export default CardAuthor;

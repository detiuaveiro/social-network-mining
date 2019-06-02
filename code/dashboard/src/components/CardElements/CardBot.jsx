import React from "react";
// used for making the prop types of this component
import PropTypes from "prop-types";

import {CardAuthor2, CardInteractions} from "components";
import {Card, CardHeader, CardBody, Badge } from 'reactstrap';


class CardBot extends React.Component {
  state = {
    bot_id: this.props.info["id"],
    title: this.props.info["name"],
    image: this.props.info["profile_image_url_https"],
    username: this.props.info["screen_name"],
    favorites: this.props.info["favourites_count"],
    followers: this.props.info["friends_count"],
    following: this.props.info["followers_count"]
  }
  render() {
    return (
      <Card>
        <CardHeader>
          <CardAuthor2
            avatar={this.state.image}
            avatarAlt="..."
            title={this.state.title}
            description={"@"+this.state.username}
            link={"bots/"+this.state.bot_id}
          />
          <p className="description text-center">
          <Badge color="light"><i className="fab fa-2x fa-twitter"></i></Badge>
            <br/>
            Twitter
          </p>
        </CardHeader>
        <CardBody>
          <CardInteractions
            size="xs"
            socials={[
              {
                icon: "fas fa-2x fa-heart",
                number: this.state.favorites,
              },
              {
                icon: "fas fa-2x fa-user",
                number: this.state.followers,
              },
            ]}
          />
        </CardBody>
      </Card>
    );
  }
}

CardBot.propTypes = {
  // size of all social buttons
  size: PropTypes.oneOf(["sm", "lg"]),
  // example: [{icon: "name of icon", href="href of icon"},...]
  info: PropTypes.objectOf(PropTypes.object),
  socials: PropTypes.arrayOf(PropTypes.object)
};

export default CardBot;

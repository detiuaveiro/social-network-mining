import React from "react";
// used for making the prop types of this component
import PropTypes from "prop-types";

import {CardAuthor2, CardInteractions, Stats} from "components";
import {Card, CardHeader, CardBody, CardFooter, Badge } from 'reactstrap';

import userAvatar from "assets/img/mike.jpg";


class CardBot extends React.Component {
  render() {
    return (
      <Card>
        <CardHeader>
          <CardAuthor2
            avatar={userAvatar}
            avatarAlt="..."
            title="Afonso Silva"
            description="@afonsosilva01"
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
                icon: "fas fa-2x fa-quote-left",
                number: 123,
              },
              {
                icon: "fas fa-2x fa-retweet",
                number: 43,
              },
              {
                icon: "fas fa-2x fa-comments",
                number: 12,
              },
            ]}
          />
        </CardBody>
        <CardFooter>
          <Stats>
            {[
              {
                i: "now-ui-icons arrows-1_refresh-69",
                t: "Just Updated"
              }
            ]}
          </Stats>
        </CardFooter>
      </Card>
    );
  }
}

CardBot.propTypes = {
  // size of all social buttons
  size: PropTypes.oneOf(["sm", "lg"]),
  // example: [{icon: "name of icon", href="href of icon"},...]
  socials: PropTypes.arrayOf(PropTypes.object)
};

export default CardBot;

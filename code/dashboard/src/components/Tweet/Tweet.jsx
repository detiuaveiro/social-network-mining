import React from "react";
import { Card, CardHeader, CardBody, CardTitle, CardText, Nav, NavItem, NavLink } from 'reactstrap';
import { Button, CardAuthor } from 'components';// used for making the prop types of this component
import PropTypes from "prop-types";
import userAvatar from "assets/img/mike.jpg";

class Tweet extends React.Component {
  render() {
    return (
      <Card >
          <CardHeader>
              <Nav pills>
                  <NavItem>
                      <NavLink href="#" active>Tweet</NavLink>
                  </NavItem>
                  <NavItem>
                      <NavLink href="#">Stats</NavLink>
                  </NavItem>
              </Nav>
          </CardHeader>
          <CardBody>
              <CardAuthor
                  avatar={userAvatar}
                  avatarAlt="..."
                  title="Afonso Silva"
                  description="@afonsosilva01"
                />
              <CardTitle>Special title treatment</CardTitle>
              <CardText>With supporting text below as a natural lead-in to additional content.</CardText>
              <Button href="/#" color="primary">Go somewhere</Button>
          </CardBody>
      </Card>
    );
  }
}



export default Tweet;

import React from "react";

import { PanelHeader, Stats, CardAuthor, CardCategory, CardInteractions, Button } from "components";
import {
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  CardTitle,
  Row,
  Col,
  UncontrolledDropdown,
  DropdownToggle,
  DropdownMenu,
  DropdownItem,
} from "reactstrap";
import userAvatar from "assets/img/mike.jpg";

class BotsPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        activeTab: '1',
    };
    this.toggle = this.toggle.bind(this);
  }
  toggle(tab) {
      if (this.state.activeTab !== tab) {
          this.setState({
              activeTab: tab
          });
      }
  }
  render() {
    return (
      <div>
        <PanelHeader
          size="md"
          content={
            <div className="header text-center">
              <h2 className="title">Bots</h2>
            </div>
          }
        />
        <div className="content">
          <Row>
            <Col xs={12} md={4}>
              <Card className="card-chart">
                <CardHeader>
                  <CardCategory>Twitter</CardCategory>
                  <CardAuthor
                    avatar={userAvatar}
                    avatarAlt="..."
                    title="Afonso Silva"
                    description="@afonsosilva01"
                  />
                </CardHeader>
                <CardBody>
                  <CardInteractions
                    size="sm"
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
            </Col>
            <Col xs={12} md={4}>
              <Card className="card-chart">
                <CardHeader>
                  <CardCategory>Twitter</CardCategory>
                  <CardAuthor
                    avatar={userAvatar}
                    avatarAlt="..."
                    title="Afonso Silva"
                    description="@afonsosilva01"
                  />
                </CardHeader>
                <CardBody>
                  <CardInteractions
                    size="sm"
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
            </Col>
            <Col xs={12} md={4}>
              <Card className="card-chart">
                <CardHeader>
                  <CardCategory>Twitter</CardCategory>
                  <CardAuthor
                    avatar={userAvatar}
                    avatarAlt="..."
                    title="Afonso Silva"
                    link="1"
                    description="@afonsosilva01"
                  />
                </CardHeader>
                <CardBody>
                  <CardInteractions
                    size="sm"
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
            </Col>
          </Row>
        </div>
      </div>
    );
  }
}

export default BotsPage;

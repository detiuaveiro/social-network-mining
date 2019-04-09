import React from "react";

import { PanelHeader, FormInputs, CardAuthor, CardNumbers, Tweet} from "components";
import { Nav, NavItem, NavLink, Card, CardHeader, CardBody, TabPane, TabContent, Row, Col } from 'reactstrap';

import userAvatar from "assets/img/mike.jpg";

class User extends React.Component {
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
        <PanelHeader size="sm" />
        <div className="content">
          <Row>
            <Col md={4} xs={12}>
              <Card className="card-user">
                <CardBody>
                  <CardAuthor
                    avatar={userAvatar}
                    avatarAlt="..."
                    title="Afonso Silva"
                    description="@afonsosilva01"
                  />
                  <p className="description text-center">
                    Description<br />
                  </p>
                </CardBody>
                <hr />
                <CardNumbers
                  size="sm"
                  socials={[
                    {
                      text: "Tweets",
                    },
                    {
                      text: "Following",
                    },
                    {
                      text: "Followers",
                    }
                  ]}
                />
              </Card>
            </Col>
            <Col md={8} xs={12}>
              <Card>
                <CardHeader>
                  <h5 className="title"><i className="fab fa-2x fa-twitter"></i> Profile</h5>
                </CardHeader>
                <CardBody>
                  <form>
                    <FormInputs
                      ncols={[
                        "col-md-6 pr-1",
                        "col-md-6 px-1",
                      ]}
                      proprieties={[
                        {
                          label: "Nome",
                          inputProps: {
                            type: "text",
                            disabled: true,
                          }
                        },
                        {
                          label: "Username",
                          inputProps: {
                            type: "text",
                            disabled: true,
                          }
                        },
                      ]}
                    />
                    <FormInputs
                      ncols={["col-md-6 pr-1", "col-md-6 pl-1"]}
                      proprieties={[
                        {
                          label: "Birthday",
                          inputProps: {
                            type: "date",
                            disabled: true,
                          }
                        },
                        {
                          label: "Location",
                          inputProps: {
                            type: "text",
                            disabled: true,
                          }
                        }
                      ]}
                    />
                    <FormInputs
                      ncols={[
                        "col-md-12 pr-1"
                      ]}
                      proprieties={[
                        {
                          label: "Email",
                          inputProps: {
                            type: "email",
                            disabled: true,
                          }
                        },
                      ]}
                    />
                    <FormInputs
                      ncols={["col-md-12"]}
                      proprieties={[
                        {
                          label: "Description",
                          inputProps: {
                            type: "textarea",
                            rows: "4",
                            cols: "80",
                            defaultValue:
                              "Description.",
                            disabled: true,
                            }
                        }
                      ]}
                    />
                  </form>
                </CardBody>
              </Card>
            </Col>
            <Col md={12} xs={12}>
              <Card className="card-plain">
                <CardHeader>
                    <Nav className="justify-content-center" tabs>
                        <NavItem>
                            <NavLink
                                className={this.state.activeTab === '1' ? 'active':''}
                                onClick={() => { this.toggle('1'); }}
                                >
                                  Tweets
                            </NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink
                                className={this.state.activeTab === '2' ? 'active':''}
                                onClick={() => { this.toggle('2'); }}
                            >
                              Followers
                            </NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink
                                className={this.state.activeTab === '3' ? 'active':''}
                                onClick={() => { this.toggle('3'); }}
                            >
                              Following
                            </NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink
                                className={this.state.activeTab === '4' ? 'active':''}
                                onClick={() => { this.toggle('4'); }}
                            >
                              Statistics
                            </NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink
                                className={this.state.activeTab === '5' ? 'active':''}
                                onClick={() => { this.toggle('5'); }}
                            >
                              Policies
                            </NavLink>
                        </NavItem>
                    </Nav>
                </CardHeader>
                <CardBody>
                    <TabContent activeTab={this.state.activeTab} className="text-center">
                        <TabPane tabId="1">
                          <Tweet></Tweet>
                        </TabPane>
                        <TabPane tabId="2">
                            <p> I will be the leader of a company that ends up being worth billions of dollars, because I got the answers. I understand culture. I am the nucleus. I think that's a responsibility that I have, to push possibilities, to show people, this is the level that things could be at. I think that's a responsibility that I have, to push possibilities, to show people, this is the level that things could be at. </p>
                        </TabPane>
                        <TabPane tabId="3">
                            <p> I think that's a responsibility that I have, to push possibilities, to show people, this is the level that things could be at. I will be the leader of a company that ends up being worth billions of dollars, because I got the answers. I understand culture. I am the nucleus. I think that's a responsibility that I have, to push possibilities, to show people, this is the level that things could be at.</p>
                        </TabPane>
                    </TabContent>
                </CardBody>
            </Card>
            </Col>
          </Row>
        </div>
      </div>
    );
  }
}

export default User;

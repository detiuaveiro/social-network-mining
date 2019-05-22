import React from "react";
import axios from 'axios';

import {FormInputs, CardAuthor, CardNumbers, Tweet, UserInfo, PanelHeader} from "components";
import {Nav, NavItem, NavLink, Card, CardHeader, CardBody, TabPane, TabContent, Row, Col, Badge } from 'reactstrap';

import userAvatar from "assets/img/mike.jpg";

class User extends React.Component {
  state = {
    tweets: [],
    profile_data: [],
    activeTab: '1',
  };
  componentDidMount() {
    axios.get('/twitter/tweets')
      .then(res => {
        const tweets = res.data;
        this.setState({ tweets });
        console.log(this.state.tweets)
      });
    const url = window.location.pathname.substring(window.location.pathname.lastIndexOf('/') + 1)
    axios.get('/twitter/users/'+url)
      .then(res => {
        const profile_data = res.data[0];
        this.setState({ profile_data });
      })
  }

  constructor(props) {
    super(props);
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
          size="sm"
        />
        <div className="content">
          <Row>
            <Col md={4} xs={12}>
              <Card className="card-user">
                <CardBody>
                  <CardAuthor
                    avatar={this.state.profile_data["profile_image_url_https"]}
                    avatarAlt="..."
                    title={this.state.profile_data["name"]}
                    description={"@"+this.state.profile_data["screen_name"]}
                  />
                  <p className="description text-center">
                    {this.state.profile_data["description"]}<br />
                  </p>
                </CardBody>
                <hr />
                <CardNumbers
                  size="sm"
                  socials={[
                    {
                      text: "Following",
                      number:this.state.profile_data["friends_count"]
                    },
                    {
                      text: "Followers",
                      number:this.state.profile_data["followers_count"]
                    }
                  ]}
                />
              </Card>
            </Col>
            <Col md={8} xs={12}>
              <Card>
                <CardHeader>
                  <h5 className="title">Profile <Badge color="light"><i className="fab fa-1x fa-twitter"></i></Badge>
</h5>
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
                            defaultValue: this.state.profile_data["name"]
                          }
                        },
                        {
                          label: "Username",
                          inputProps: {
                            type: "text",
                            disabled: true,
                            defaultValue: this.state.profile_data["screen_name"]
                          }
                        },
                      ]}
                    />
                    <FormInputs
                      ncols={["col-md-6 pr-1", "col-md-6 pl-1"]}
                      proprieties={[
                        {
                          label: "ID",
                          inputProps: {
                            type: "number",
                            disabled: true,
                            defaultValue: this.state.profile_data["id"]
                          }
                        },
                        {
                          label: "Location",
                          inputProps: {
                            type: "text",
                            disabled: true,
                            defaultValue: this.state.profile_data["location"]
                          }
                        }
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
                            defaultValue: this.state.profile_data["description"],
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
                        <NavItem>
                            <NavLink
                                className={this.state.activeTab === '6' ? 'active':''}
                                onClick={() => { this.toggle('6'); }}
                            >
                              Logs
                            </NavLink>
                        </NavItem>
                    </Nav>
                </CardHeader>
                <CardBody>
                    <TabContent activeTab={this.state.activeTab} className="text-center">
                        <TabPane tabId="1">
                          <Row>
                            {this.state.tweets.map(tweet => 
                              <Col xs={12} md={6}>
                                <Tweet info={tweet}/>
                              </Col>
                            )}
                          </Row>
                        </TabPane>
                        <TabPane tabId="2">
                          <Row>
                            {this.state.tweets.map(tweet => 
                            <Col xs={12} md={6}>
                              <UserInfo info={tweet}/>
                            </Col>
                            )}
                          </Row>
                        </TabPane>
                        <TabPane tabId="3">
                          <Row>
                            {this.state.tweets.map(tweet => 
                            <Col xs={12} md={6}>
                              <UserInfo info={tweet}/>
                            </Col>
                            )}
                          </Row>
                        </TabPane>
                        <TabPane tabId="4">
                            <p>Not ready 4</p>
                        </TabPane>
                        <TabPane tabId="5">
                            <p>Not ready 5</p>
                        </TabPane>
                        <TabPane tabId="6">
                            <p>Not ready 6</p>
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

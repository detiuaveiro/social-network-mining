import React from "react";
import { Card, CardHeader, CardBody, Row, Col } from "reactstrap";

import { PanelHeader, FormInputs, CardAuthor, CardNumbers } from "components";

import userAvatar from "assets/img/mike.jpg";
import CardInteractions from "../../components/CardElements/CardInteractions";

class User extends React.Component {
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
                  <h5 className="title">Profile</h5>
                </CardHeader>
                <CardBody>
                  <form>
                    <i className="fab fa-3x fa-twitter"></i>
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
              <div class="card card-nav-tabs card-plain">
                <div class="card-header card-header-danger">
                    <div class="nav-tabs-navigation">
                        <div class="nav-tabs-wrapper">
                            <ul class="nav nav-tabs" data-tabs="tabs">
                                <li class="nav-item">
                                    <a class="nav-link active" href="#home" data-toggle="tab">Home</a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link" href="#updates" data-toggle="tab">Updates</a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link" href="#history" data-toggle="tab">History</a>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div><div class="card-body ">
                    <div class="tab-content text-center">
                        <div class="tab-pane active" id="home">
                            <p>I think that&#x2019;s a responsibility that I have, to push possibilities, to show people, this is the level that things could be at. So when you get something that has the name Kanye West on it, it&#x2019;s supposed to be pushing the furthest possibilities. I will be the leader of a company that ends up being worth billions of dollars, because I got the answers. I understand culture. I am the nucleus.</p>
                        </div>
                        <div class="tab-pane" id="updates">
                            <p> I will be the leader of a company that ends up being worth billions of dollars, because I got the answers. I understand culture. I am the nucleus. I think that&#x2019;s a responsibility that I have, to push possibilities, to show people, this is the level that things could be at. I think that&#x2019;s a responsibility that I have, to push possibilities, to show people, this is the level that things could be at. </p>
                        </div>
                        <div class="tab-pane" id="history">
                            <p> I think that&#x2019;s a responsibility that I have, to push possibilities, to show people, this is the level that things could be at. I will be the leader of a company that ends up being worth billions of dollars, because I got the answers. I understand culture. I am the nucleus. I think that&#x2019;s a responsibility that I have, to push possibilities, to show people, this is the level that things could be at.</p>
                        </div>
                    </div>
                </div>
              </div>
            </Col>
          </Row>
        </div>
      </div>
    );
  }
}

export default User;

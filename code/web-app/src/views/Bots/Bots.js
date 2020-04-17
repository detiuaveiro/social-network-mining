import React, { Component } from 'react';
import baseURL from '../../variables/baseURL'
import { Container, Row, Col, Button } from 'reactstrap';

import Table from "../../components/Table/Table.js";

import Card from "../../components/Card/Card";
import CardHeader from "../../components/Card/CardHeader";
import CardBody from "../../components/Card/CardBody";
import CardFooter from "../../components/Card/CardFooter";
import CardIcon from "../../components/Card/CardIcon";

import BotProfile from './BotProfile';

class Bots extends Component {
  constructor() {
    super();
  }

  state = {
    error: false,
    bots: [],
    bot: null
  };

  componentDidMount() {
    fetch(baseURL + "twitter/bots", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      }
    }).then(response => {
      if (response.ok) return response.json();
      else {
        throw new Error(response.status);
      }
    }).then(data => {
      if (data != null && data != {}) {
        data = data.data

        var tempBots = []

        data.forEach(bot => {
          var tempInfo = []
          tempInfo.push("" + bot.screen_name);
          tempInfo.push("" + bot.name);
          tempInfo.push("" + bot.followers_count);
          tempInfo.push("" + bot.friends_count);

          tempInfo.push("Active"); // Add wether its active or not


          tempInfo.push(
            <Button block outline color="primary"
              onClick={() => this.handleOpenProfile(bot)}
            >
              <i class="far fa-user-circle"></i>
              <strong style={{ marginLeft: "3px" }}>Profile</strong>
            </Button>
          )

          tempInfo.push(
            <Button block outline color="danger"
              onClick={() =>
                this.handleDelete(bot)
              }
            >
              <i class="far fa-trash-alt"></i>
            </Button>
          )

          tempBots.push(tempInfo);
        })

        tempBots.sort((bot1, bot2) =>
          bot1.screen_name > bot2.screen_name ? 1 : -1
        );

        this.setState({
          error: false,
          bots: tempBots,
          bot : null
        })
      }
    }).catch(error => {
      console.log("error: " + error);
      this.setState({
        error: true,
        bots: [],
        bot: null
      })
    });
  }

  handleDelete(bot) {
    console.log(bot)
  }

  handleOpenProfile(bot) {
    console.log(bot)
    this.setState({
      error: this.state.error,
      bots: this.state.bots,
      bot: bot
    })
  }

  loading = () => <div className="animated fadeIn pt-1 text-center">Loading...</div>

  render() {
    if (this.state.error) {
      return (
        <div className="animated fadeIn">
          <Container fluid>
            <Row>
              <Col xs="12" sm="12" md="9">
                <Card>
                  <CardHeader color="primary">
                    <h3 style={{ color: "white" }}>
                      <strong>Bots</strong>
                    </h3>
                    <h5 style={{ color: "white" }}>
                      List with all registered bot accounts and their status
                  </h5>
                  </CardHeader>
                  <CardBody>
                  </CardBody>
                </Card>
              </Col>
            </Row>
            <Row>
              <Col xs="12" sm="12" md="12">
                <Card>
                  <CardHeader color="primary">
                    <h4 style={{
                      color: "#FFFFFF",
                      marginTop: "0px",
                      minHeight: "auto",
                      marginBottom: "3px",
                      textDecoration: "none",
                      "& small": {
                        color: "#777",
                        fontSize: "65%",
                        fontWeight: "400",
                        lineHeight: "1"
                      }
                    }} > Registered Accounts</h4>
                  </CardHeader>
                  <CardBody>
                    <p>Sorry, an error has occured! Please try again shortly</p>
                  </CardBody>
                </Card>
              </Col>
            </Row>
          </Container>
        </div >
      )
    } else if(this.state.bot == null) {
      return (
        <div className="animated fadeIn">
          <Container fluid>
            <Row>
              <Col xs="12" sm="12" md="9">
                <Card>
                  <CardHeader color="primary">
                    <h3 style={{ color: "white" }}>
                      <strong>Bots</strong>
                    </h3>
                    <h5 style={{ color: "white" }}>
                      List with all registered bot accounts and their status
                    </h5>
                  </CardHeader>
                  <CardBody>
                  </CardBody>
                </Card>
              </Col>

              <Col xs="12" sm="12" md="3">
                <Card>
                  <CardHeader color="primary" stats icon>
                    <CardIcon color="primary">
                      <i class="fab fa-twitter"></i>
                    </CardIcon>
                    <p style={{
                      color: '#999',
                      margin: "0",
                      fontSize: "14px",
                      marginTop: "0",
                      paddingTop: "10px",
                      marginBottom: "0"
                    }}>Active accounts</p>
                    <h3 style={{
                      color: "#23282c",
                      minHeight: "auto",
                      marginBottom: "3px",
                      "& small": {
                        color: "#777",
                        fontWeight: "400",
                        lineHeight: "1"
                      }
                    }} >
                      49 / 50 < small > Bots</small>
                    </h3>
                  </CardHeader>
                  <CardBody style={{ minHeight: "38px" }}>
                  </CardBody>
                </Card>
              </Col>
            </Row>
            <Row>
              <Col xs="12" sm="12" md="12">
                <Card>
                  <CardHeader color="primary">
                    <h4 style={{
                      color: "#FFFFFF",
                      marginTop: "0px",
                      minHeight: "auto",
                      marginBottom: "3px",
                      textDecoration: "none",
                      "& small": {
                        color: "#777",
                        fontSize: "65%",
                        fontWeight: "400",
                        lineHeight: "1"
                      }
                    }} > Registered Accounts</h4>
                    <Button block outline color="light" style={{
                      width: "150px", marginTop:"15px"
                    }}>Add new</Button>
                  </CardHeader>
                  <CardBody>
                    <Table
                      tableHeaderColor="primary"
                      tableHead={["Username", "Name", "Followers", "Following", "Status", "", ""]}
                      tableData={this.state.bots}
                    />
                  </CardBody>
                </Card>
              </Col>
            </Row>
          </Container>
        </div >
      );
    }else{
      return(
        <BotProfile bot={this.state.bot}></BotProfile>
      )
    }
  }
}

export default Bots;

import React, { Component } from 'react';
import baseURL from '../../variables/baseURL'
import {
  Container, Row, Col, Button, Badge, Form,
  FormGroup,
  FormText,
  FormFeedback,
  Input,
  InputGroup,
  InputGroupAddon,
  InputGroupButtonDropdown,
  InputGroupText,
  Label,
} from 'reactstrap';

import Table from "../../components/Table/Table.js";

import Card from "../../components/Card/Card";
import CardHeader from "../../components/Card/CardHeader";
import CardBody from "../../components/Card/CardBody";
import CardIcon from "../../components/Card/CardIcon";

import Dialog from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogTitle from "@material-ui/core/DialogTitle";

import { ToastContainer, toast, Flip } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import ReactLoading from "react-loading";

import CreatableSelect from 'react-select/creatable';

class Users extends Component {
  constructor() {
    super();
  }

  state = {
    error: false,
    users: [],
    user: null,
    loading: false,
    
    noPages: 0,
    curPage: 0
  };

  getUserList() {
    fetch(baseURL + "/twitter/users/10/" + this.state.curPage, {
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
        this.setState({
          error: false,
          users: [],
          user: null,
          loading: true
        })

        data = data.data

        var tempUsers = []

        data.forEach(bot => {
          var tempInfo = []
          tempInfo.push("" + bot.screen_name);
          tempInfo.push("" + bot.name);
          tempInfo.push("" + bot.followers_count);
          tempInfo.push("" + bot.friends_count);

          tempInfo.push(
            <Button block outline color="primary"
              onClick={() => this.handleOpenProfile(bot)}
            >
              <i class="far fa-user-circle"></i>
              <strong style={{ marginLeft: "3px" }}>Profile</strong>
            </Button>
          )

          //TODO: change for if active
          if (true) {
            tempInfo.push(
              <Button block outline color="warning"
                onClick={() =>
                  this.handleOpenDeactivate(bot)
                }
              >
                <i class="fas fa-pause"></i>
              </Button>
            )
          } else {
            tempInfo.push(
              <Button block outline color="success"
                onClick={() =>
                  this.handleOpenActivate(bot)
                }
              >
                <i class="fas fa-play"></i>
              </Button>
            )
          }

          tempInfo.push(
            <Button block outline color="danger"
              onClick={() =>
                this.handleOpenDelete(bot)
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
          bot: null,
          loading: false
        })
      }
    }).catch(error => {
      console.log("error: " + error);
      this.setState({
        error: true,
        bots: [],
        bot: null,
        loading: false
      })
    });
  }

  componentDidMount() {
    this.getUserList()
  }


  // Methods //////////////////////////////////////////////////////////

  handleOpenProfile(bot) {
    console.log(bot)
    this.setState({
      error: this.state.error,
      bots: this.state.bots,
      bot: bot
    })
  }

  /////////////////////////////////////////////////////////////////////

  loading = () => <div className="fadeIn pt-1 text-center"><ReactLoading type={"cubes"} color="#1da1f2" /></div>

  render() {

    return (
      <div className="animated fadeIn">

        <Container fluid>
          <ToastContainer
            position="top-center"
            autoClose={2500}
            hideProgressBar={false}
            transition={Flip}
            newestOnTop={false}
            closeOnClick
            rtl={false}
            pauseOnVisibilityChange
            draggable
            pauseOnHover
          />
          <Row>
            <Col xs="12" sm="12" md="9">
              <Card>
                <CardHeader color="primary">
                  <h3 style={{ color: "white" }}>
                    <strong>Twitter Users</strong>
                  </h3>
                  <h5 style={{ color: "white" }}>
                    List with all Twitter users the bots have found and gathered data on
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
                    <i class="fas fa-users"></i>
                  </CardIcon>
                  <p style={{
                    color: '#999',
                    margin: "0",
                    fontSize: "14px",
                    marginTop: "0",
                    paddingTop: "10px",
                    marginBottom: "0"
                  }}>Total number of users</p>
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
                    10
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
                  }} > Registered Users</h4>

                </CardHeader>
                <CardBody>
                  <Table
                    tableHeaderColor="primary"
                    tableHead={["Username", "Name", "Followers", "Following", "Status", "", "", ""]}
                    tableData={this.state.bots}
                  />
                </CardBody>
              </Card>
            </Col>
          </Row>
        </Container>
      </div >
    );
  }
}

export default Users;

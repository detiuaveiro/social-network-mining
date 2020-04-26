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
  CardFooter,
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
import Pagination from '@material-ui/lab/Pagination';

import UserProfile from './UserProfile';

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
    curPage: 1
  };

  getUserList(currentPage) {
    document.getElementById("loadedTable").style.visibility = "hidden"
    document.getElementById("loadingTable").style.display = ""

    fetch(baseURL + "twitter/users/15/" + currentPage + "/", {
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
        console.log(data)
        this.setState({
          error: false,
          users: [],
          user: null,
          loading: true
        })

        data = data.data

        var tempUsers = []

        data.entries.forEach(user => {
          var tempInfo = []
          tempInfo.push("@" + user.screen_name);
          tempInfo.push("" + user.name);
          tempInfo.push("" + user.followers_count);
          tempInfo.push("" + user.friends_count);

          tempInfo.push(
            <Button block outline color="primary"
              onClick={() => this.handleOpenProfile(user)}
            >
              <i class="far fa-user-circle"></i>
              <strong style={{ marginLeft: "3px" }}>Profile</strong>
            </Button>
          )

          tempUsers.push(tempInfo);
        })

        this.setState({
          error: false,
          users: tempUsers,
          user: null,
          loading: false,

          noPages: data.num_pages,
          curPage: currentPage,
        })
      }
    }).catch(error => {
      console.log("error: " + error);
      this.setState({
        error: true,
        users: [],
        user: null,
        loading: false
      })
    });

    document.getElementById("loadedTable").style.visibility = "visible"
    document.getElementById("loadingTable").style.display = "none"
  }

  componentDidMount() {
    this.getUserList(1)
  }


  // Methods //////////////////////////////////////////////////////////

  handleOpenProfile(user) {
    this.setState({
      user: user
    })
  }

  changePage = (event, value) => {
    this.setState({
      curPage: value
    })

    this.getUserList(value)
  };

  /////////////////////////////////////////////////////////////////////

  loading = () => <div className="fadeIn pt-1 text-center"><ReactLoading type={"cubes"} color="#1da1f2" /></div>

  render() {

    if (this.state.user == null) {
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
                      150
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
                    <div style={{ position: "relative" }}>
                      <div
                        id="loadedTable"
                        style={{
                          width: "100%",
                          height: "100%",
                          position: "relative",
                          top: 0,
                          left: 0,
                          visibility: ""
                        }}>
                        <Table
                          tableHeaderColor="primary"
                          tableHead={["Username", "Name", "Followers", "Following", ""]}
                          tableData={this.state.users}
                        />

                      </div>
                      <div
                        id="loadingTable"
                        style={{
                          zIndex: 10,
                          position: "absolute",
                          top: "45%",
                          left: "45%",
                          display: ""
                        }}>
                        <ReactLoading width={"150px"} type={"cubes"} color="#1da1f2" />
                      </div>
                    </div>

                    <div style={{
                      marginTop: "25px",
                      width: "100%",
                      textAlign: "center"
                    }}>
                      <div style={{ display: "inline-block" }}>
                        <Pagination count={this.state.noPages} page={this.state.curPage} onChange={this.changePage} variant="outlined" color="primary" showFirstButton showLastButton shape="rounded" />

                      </div>
                    </div>
                  </CardBody>
                </Card>
              </Col>
            </Row>
          </Container>
        </div >
      );
    } else {
      return (
        <UserProfile user={this.state.user}></UserProfile>
      )
    }


  }
}

export default Users;

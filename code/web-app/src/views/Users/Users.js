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

import { ToastContainer, toast, Flip } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import ReactLoading from "react-loading";
import Pagination from '@material-ui/lab/Pagination';

import UserProfile from './UserProfile';

import FadeIn from "react-fade-in";
import Lottie from "react-lottie";

import * as loadingAnim from "../../assets/animations/squares_1.json";


class Users extends Component {
  constructor() {
    super();
  }

  state = {
    error: false,
    users: [],
    user: null,
    doneLoading: false,

    animationOptions: {
      loop: true, autoplay: true, animationData: loadingAnim.default, rendererSettings: {
        preserveAspectRatio: "xMidYMid slice"
      }
    },

    noPages: 0,
    curPage: 1,
    noUsers: 0,
    empty: false,

    searchQuery: ""
  };

  async getUserList(currentPage) {
    var tempUsers = []
    await fetch(baseURL + "twitter/users/15/" + currentPage + "/", {
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
        })

        data = data.data

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

        var empty = false
        if (tempUsers.length == 0) {
          empty = true
        }

        this.setState({
          error: false,
          users: tempUsers,
          user: null,
          loading: false,

          noPages: data.num_pages,
          curPage: currentPage,
          empty: empty
        })
      }
    }).catch(error => {
      console.log("error: " + error);
      this.setState({
        error: true,
        users: [],
        user: null,
      })
    });
  }

  async searchUsers(currentPage) {
    var tempUsers = []
    await fetch(baseURL + "twitter/users/search/" + this.state.searchQuery + "/15/" + currentPage + "/", {
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
        })

        data = data.data

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

        var empty = false
        if (tempUsers.length == 0) {
          empty = true
        }

        this.setState({
          error: false,
          users: tempUsers,
          user: null,
          loading: false,

          noPages: data.num_pages,
          curPage: currentPage,
          empty: empty
        })
      }
    }).catch(error => {
      console.log("error: " + error);
      this.setState({
        error: true,
        users: [],
        user: null,
      })
    });
  }

  async getUserCount() {
    await fetch(baseURL + "entities/counter", {
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


        this.setState({
          noUsers: data.User
        })
      }
    }).catch(error => {
      console.log("error: " + error);
      this.setState({
        error: true,
      })
    });
  }

  async componentDidMount() {
    var page = 1
    if (this.props.page != null) {
      page = this.props.page
    }
    if (this.props.searchQuery != null && this.props.searchQuery != "") {
      await this.setState({ searchQuery: this.props.searchQuery })
      await this.searchUsers(page)

    } else {
      await this.getUserList(page)
    }
    await this.getUserCount()

    await this.setState({
      doneLoading: true
    })

    if (document.getElementById("searchUser") != null) {
      document.getElementById("searchUser").value = this.state.searchQuery
    }
  }


  // Methods //////////////////////////////////////////////////////////

  handleOpenProfile(user) {
    this.setState({
      user: user
    })
  }

  changePage = async (event, value) => {
    document.getElementById("loadedTable").style.visibility = "hidden"
    document.getElementById("loadingTable").style.display = ""

    this.setState({
      curPage: value
    })

    if (this.state.searchQuery.length == 0) {
      await this.getUserList(value)
    } else {
      await this.searchUsers(value)
    }

    document.getElementById("loadedTable").style.visibility = "visible"
    document.getElementById("loadingTable").style.display = "none"
  };


  async search() {
    if (document.getElementById("searchUser").value != null &&  document.getElementById("searchUser").value!="" && !document.getElementById("searchUser").value.match("^[A-Za-z0-9]+$")) {
      toast.error('Sorry, the search parameter can\'t include characters like @ or #. Please use only letters and numbers', {
        position: "top-center",
        autoClose: 7500,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true
      });
    } else {
      document.getElementById("loadedTable").style.visibility = "hidden"
      document.getElementById("loadingTable").style.display = ""

      await this.setState({
        curPage: 1,
        searchQuery: document.getElementById("searchUser").value
      })

      if (this.state.searchQuery.length == 0) {
        await this.getUserList(1)
      } else {
        await this.searchUsers(1)
      }

      if (document.getElementById("loadedTable") != null) {
        document.getElementById("loadedTable").style.visibility = "visible"
        document.getElementById("loadingTable").style.display = "none"
      }
    }
  }

  keydown(e) {
    if (e.keyCode == 13) {
      document.getElementById("searchButton").click()
    }
  }
  /////////////////////////////////////////////////////////////////////

  loading = () => <div className="fadeIn pt-1 text-center"><ReactLoading type={"cubes"} color="#1da1f2" /></div>

  render() {

    if (this.state.user == null) {
      if (!this.state.doneLoading) {
        return (
          <div className="animated fadeOut animated" style={{ width: "100%", marginTop: "10%" }}>
            <FadeIn>
              <Lottie options={this.state.animationOptions} height={"30%"} width={"30%"} />
            </FadeIn>
          </div>
        )
      } else if (this.state.error) {
        return (
          <Container fluid>
            <Row>
              <Col xs="12" sm="12" md="12">
                <div style={{ width: "100%", alignContent: "center" }}>
                  <img style={{ width: "50%", display: "block", marginLeft: "auto", marginRight: "auto" }} src={require("../../assets/img/error.png")}></img>
                </div>
              </Col>
            </Row>
          </Container>
        )
      } else {
        var users = <CardBody></CardBody>
        var table = <div></div>
        if (this.state.empty) {
          if (this.state.searchQuery == "") {
            table =
              <div
                id="loadedTable"
                style={{
                  width: "100%",
                  height: "100%",
                  position: "relative",
                  top: 0,
                  paddingTop: 0,
                  marginTop: "25px",
                  left: 0,
                  visibility: "",
                }}>
                <h5 style={{ color: "#999" }}>
                  Hmmm... there don't seem to be any users in our databases 🤔
                </h5>
              </div>
          } else {
            table =
              <div
                id="loadedTable"
                style={{
                  width: "100%",
                  height: "100%",
                  position: "relative",
                  top: 0,
                  paddingTop: 0,
                  marginTop: "25px",
                  left: 0,
                  visibility: "",
                }}>
                <h5 style={{ color: "#999" }}>
                  Hmmm... we couldn't find any users with either a name or username matching <strong>{this.state.searchQuery}</strong> 🤔
                </h5>
              </div>
          }

        } else {
          table = <div
            id="loadedTable"
            style={{
              width: "100%",
              height: "100%",
              position: "relative",
              top: 0,
              paddingTop: 0,
              marginTop: "0px",
              left: 0,
              visibility: "",
            }}>
            <Table
              tableHeaderColor="primary"
              tableHead={["Username", "Name", "Followers", "Following", ""]}
              tableData={this.state.users}
            />

          </div>
        }

        users =
          <CardBody>
            <div style={{ position: "relative" }}>
              <div class="row" style={{ marginTop: "15px" }}>
                <div class="col-md-4 col-sm-12 form-group">
                  <input type="text" placeholder="Search by name or username" class="form-control" id="searchUser" onKeyDown={this.keydown} />
                </div>
                <div class="col-md-2 col-sm-12">
                  <Button outline color="primary" id="searchButton"
                    onClick={() => this.search()}
                  >

                    <i class="fas fa-search"></i>
                    <strong style={{ marginLeft: "3px" }}>Search</strong>
                  </Button>
                </div>
              </div>
              {table}
              <div
                id="loadingTable"
                style={{
                  zIndex: 10,
                  position: "absolute",
                  top: "45%",
                  left: "45%",
                  display: "none"
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
                        <span style={{color:"#999"}}>~</span>{this.state.noUsers}
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
                    {users}
                  </Card>
                </Col>
              </Row>
            </Container>
          </div >
        );
      }
    } else {
      return (
        <UserProfile user={this.state.user} redirection={[{ "type": "USERS", "info": { "page": this.state.curPage, "query": this.state.searchQuery } }]}></UserProfile>
      )
    }


  }
}

export default Users;

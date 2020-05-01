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

import BotProfile from './BotProfile';

class OldBots extends Component {
  constructor() {
    super();
  }

  state = {
    error: false,
    bots: [],
    bot: null,
    loading: true,
    modal: false,
    modalType: null,
    modalBot: null
  };

  getBotList() {
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
        this.setState({
          error: false,
          bots: [],
          bot: null,
          loading: true
        })

        data = data.data

        var tempBots = []

        data.forEach(bot => {
          var tempInfo = []
          tempInfo.push("" + bot.screen_name);
          tempInfo.push("" + bot.name);
          tempInfo.push("" + bot.followers_count);
          tempInfo.push("" + bot.friends_count);

          // Add wether its active or not
          tempInfo.push(<Badge pill color="success" style={{ fontSize: "11px" }}>Active</Badge>);


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
    this.getBotList()
  }


  // Methods //////////////////////////////////////////////////////////

  handleOpenDeactivate(bot) {
    this.setState({
      modal: true,
      modalType: "DEACTIVATE",
      modalBot: bot
    });
  }

  handleOpenAdd() {
    this.setState({
      modal: true,
      modalType: "ADD",
      modalBot: ""
    });
  }

  handleOpenActivate(bot) {
    this.setState({
      modal: true,
      modalType: "ACTIVATE",
      modalBot: bot
    });
  }

  handleOpenDelete(bot) {
    this.setState({
      modal: true,
      modalType: "DELETE",
      modalBot: bot
    });
  }

  handleAdd() {
    var name = document.getElementById("name").value;
    var pass = document.getElementById("pass").value;

    if(name == "" || pass == ""){
      document.getElementById("error").style.display = ""
      return
    }

    document.getElementById("error").style.display = "None";

    //TODO: ADD BOT

    this.getBotList()

    //TODO: ADD FAILURE OPTION
    if (true) {
      toast.success('🤖 New bot added succesfully!', {
        position: "top-center",
        autoClose: 2500,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true
      });
    } else {
      toast.error('Sorry, there was an error registering the bot! Please try again later.', {
        position: "top-center",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true
      });
    }

    this.handleClose()
  }

  handleDeactivate(bot) {
    //TODO: DEACTIVATE BOT

    this.getBotList()

    //TODO: ADD FAILURE OPTION
    if (true) {
      toast.info('⏸️ Bot successfully deactivated!', {
        position: "top-center",
        autoClose: 2500,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true
      });
    } else {
      toast.error('Sorry, there was an error deactivating the bot! Please try again later.', {
        position: "top-center",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true
      });
    }


    this.handleClose()
  }

  handleActivate(bot) {
    //TODO: ACTIVATE BOT

    this.getBotList()

    //TODO: ADD FAILURE OPTION
    if (true) {
      toast.success('▶️ Bot successfully activated', {
        position: "top-center",
        autoClose: 2500,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true
      });
    } else {
      toast.error('Sorry, there was an error activating the bot! Please try again later.', {
        position: "top-center",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true
      });
    }


    this.handleClose()
  }

  handleDelete(bot) {
    //TODO: DELETE BOT

    this.getBotList()

    //TODO: ADD FAILURE OPTION
    if (true) {
      toast.info('🗑️ Bot successfully deleted', {
        position: "top-center",
        autoClose: 2500,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true
      });
    } else {
      toast.error('Sorry, there was an error deleting the bot! Please try again later.', {
        position: "top-center",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true
      });
    }


    this.handleClose()
  }

  handleClose() {
    this.setState({
      modal: false,
      modalType: null,
      modalBot: null
    });
  }

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
    }

    if (this.state.bot == null) {
      var modal = null
      if (this.state.modalBot != null) {
        if (this.state.modalType == "DELETE") {
          modal = <Dialog class="fade-in"
            open={this.state.modal}
            onClose={() => this.handleClose()}
            aria-labelledby="alert-dialog-title"
            aria-describedby="alert-dialog-description"
          >
            <DialogTitle id="alert-dialog-title">
              {"🗑️ Are you sure you want to completely unregister this bot?"}
            </DialogTitle>
            <DialogContent>
              <DialogContentText id="alert-dialog-description">
                Bot <b>{this.state.modalBot.name}</b> (@{this.state.modalBot.screen_name}) will be permanently unregistered from our service and will stop being a bot. You can always add this account back later.
            </DialogContentText>
            </DialogContent>
            <DialogActions>
              <Button onClick={() => this.handleClose()} color="info">
                Cancel
            </Button>
              <Button
                onClick={() => this.handleDelete()}
                color="danger"
                autoFocus
              >
                Confirm
            </Button>
            </DialogActions>
          </Dialog>
        } else if (this.state.modalType == "ACTIVATE") {
          modal = <Dialog class="fade-in"
            open={this.state.modal}
            onClose={() => this.handleClose()}
            aria-labelledby="alert-dialog-title"
            aria-describedby="alert-dialog-description"
          >
            <DialogTitle id="alert-dialog-title">
              {"▶️ Are you sure you want to activate this bot?"}
            </DialogTitle>
            <DialogContent>
              <DialogContentText id="alert-dialog-description">
                Bot <b>{this.state.modalBot.name}</b> (@{this.state.modalBot.screen_name}) will be activated. This means the account will start behaving like a bot, following it's set policies. In extreme cases, this may lead to the account being banned. Proceed at your own caution.
            </DialogContentText>
            </DialogContent>
            <DialogActions>
              <Button onClick={() => this.handleClose()} color="info">
                Cancel
            </Button>
              <Button
                onClick={() => this.handleActivate()}
                color="success"
                autoFocus
              >
                Confirm
            </Button>
            </DialogActions>
          </Dialog>
        } else if (this.state.modalType == "DEACTIVATE") {
          modal = <Dialog class="fade-in"
            open={this.state.modal}
            onClose={() => this.handleClose()}
            aria-labelledby="alert-dialog-title"
            aria-describedby="alert-dialog-description"
          >
            <DialogTitle id="alert-dialog-title">
              {"⏸️ Are you sure you want to deactivate this bot?"}
            </DialogTitle>
            <DialogContent>
              <DialogContentText id="alert-dialog-description">
                Bot <b>{this.state.modalBot.name}</b> (@{this.state.modalBot.screen_name}) will be deactivated. This means all bot scripts will be deactivated for this account and it'll go back to being a normal account.
            </DialogContentText>
            </DialogContent>
            <DialogActions>
              <Button onClick={() => this.handleClose()} color="info">
                Cancel
            </Button>
              <Button
                onClick={() => this.handleDeactivate()}
                color="warning"
                autoFocus
              >
                Confirm
            </Button>
            </DialogActions>
          </Dialog>
        } else if (this.state.modalType == "ADD") {
          modal = <Dialog class="fade-in"
            open={this.state.modal}
            onClose={() => this.handleClose()}
            aria-labelledby="alert-dialog-title"
            aria-describedby="alert-dialog-description"
          >
            <DialogTitle id="alert-dialog-title">
              {"🤖 Add a new bot"}
            </DialogTitle>
            <DialogContent style={{minWidth: "600px"}}>
              <Container fluid>
                <Row>
                  <Col xs="12" md="12">
                    <FormGroup>
                      <Label htmlFor="name">Name</Label>
                      <Input type="text" id="name" placeholder="Enter the Twitter account's username" required />
                    </FormGroup>
                  </Col>
                </Row>
                <Row>
                  <Col xs="12" md="12">
                    <FormGroup>
                      <Label htmlFor="name">Password</Label>
                      <Input type="password" id="pass" placeholder="Enter the Twitter account's password" required />
                    </FormGroup>
                  </Col>
                </Row>

                <DialogContentText>
                  <span id="error" style={{display:"None", color:"#f86c6b"}}>You need to fill both fields to register a new bot!</span>
                </DialogContentText>
              </Container>

            </DialogContent>
            <DialogActions>
              <Button onClick={() => this.handleClose()} color="info">
                Cancel
            </Button>
              <Button
                onClick={() => this.handleAdd()}
                color="success"
                autoFocus
              >
                Confirm
            </Button>
            </DialogActions>
          </Dialog>
        }

      }


      if (this.state.loading) {
        return (
          <div className="animated fadeIn">
            <Container fluid>
              <ToastContainer
                position="top-center"
                autoClose={2500}
                hideProgressBar={false}
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
                      <div style={{
                        minHeight: "auto",
                        float: "right",
                        marginBottom: "3px",
                      }}>
                        <ReactLoading type={"cubes"} color="#1da1f2" />
                      </div>
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
                        width: "150px", marginTop: "15px"
                      }} onClick={() => this.handleOpenAdd()}
                      >Add new</Button>
                    </CardHeader>
                    <CardBody>
                      <ReactLoading type={"cubes"} color="#1da1f2" />
                    </CardBody>
                  </Card>
                </Col>
              </Row>
            </Container>
          </div >
        );
      }
      else {
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
                        <i class="fas fa-robot"></i>
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
                        1/1< small > Bots</small>
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
                        width: "150px", marginTop: "15px"
                      }} onClick={() => this.handleOpenAdd()}>Add new</Button>
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
            {modal}
          </div >
        );
      }

    } else {
      return (
        <BotProfile bot={this.state.bot}></BotProfile>
      )
    }
  }
}

export default OldBots;

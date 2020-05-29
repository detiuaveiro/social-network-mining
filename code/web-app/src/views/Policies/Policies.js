import React, { Component } from 'react';
import baseURL from '../../variables/baseURL'
import {
  FormGroup, Label, Input,
  Container, Row, Col, Button, Badge, Form,
} from 'reactstrap';

import Table from "@material-ui/core/Table";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
// core components
import { withStyles } from "@material-ui/core/styles";

import Card from "../../components/Card/Card";
import CardHeader from "../../components/Card/CardHeader";
import CardBody from "../../components/Card/CardBody";
import CardIcon from "../../components/Card/CardIcon";

import { ToastContainer, toast, Flip } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import ReactLoading from "react-loading";
import Pagination from '@material-ui/lab/Pagination';

import FadeIn from "react-fade-in";
import Lottie from "react-lottie";

import Dialog from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogTitle from "@material-ui/core/DialogTitle";

import Select from 'react-select';
import CreatableSelect from 'react-select/creatable';
import makeAnimated from 'react-select/animated';

import ReactTooltip from "react-tooltip";

import * as loadingAnim from "../../assets/animations/squares_1.json";

import NewPolicy from './NewPolicy';


import {
  warningColor,
  primaryColor,
  dangerColor,
  successColor,
  infoColor,
  roseColor,
  grayColor,
  defaultFont
} from "../../assets/jss/material-dashboard-react.js";

const useStyles = theme => ({
  warningTableHeader: {
    color: warningColor[0]
  },
  primaryTableHeader: {
    color: primaryColor[0]
  },
  dangerTableHeader: {
    color: dangerColor[0]
  },
  successTableHeader: {
    color: successColor[0]
  },
  infoTableHeader: {
    color: infoColor[0]
  },
  roseTableHeader: {
    color: roseColor[0]
  },
  grayTableHeader: {
    color: grayColor[0]
  },
  table: {
    marginBottom: "0",
    width: "100%",
    maxWidth: "100%",
    backgroundColor: "transparent",
    borderSpacing: "0",
    borderCollapse: "collapse"
  },
  tableHeadCell: {
    color: "inherit",
    ...defaultFont,
    "&, &$tableCell": {
      fontSize: "1em"
    }
  },
  tableCell: {
    ...defaultFont,
    lineHeight: "1.42857143",
    padding: "12px 8px",
    verticalAlign: "middle",
    fontSize: "0.8125rem"
  },
  tableResponsive: {
    width: "100%",
    marginTop: theme.spacing(3),
    overflowX: "auto"
  },
  tableHeadRow: {
    height: "56px",
    color: "inherit",
    display: "table-row",
    outline: "none",
    verticalAlign: "middle"
  },
  tableBodyRow: {
    height: "48px",
    color: "inherit",
    display: "table-row",
    outline: "none",
    verticalAlign: "middle"
  }
});

class Policies extends Component {
  constructor() {
    super();
  }

  state = {
    error: false,

    policies: [],
    policy: null,

    noPages: 1,
    curPage: 1,

    doneLoading: false,

    animationOptions: {
      loop: true, autoplay: true, animationData: loadingAnim.default, rendererSettings: {
        preserveAspectRatio: "xMidYMid slice"
      }
    },

    noPolicies: 0,
    empty: false,

    filter: null,
    tags: [],
    bots: [],
    allBots: [],
    processing: false,

    noPolicies: 0,
    noActivePolicies: 0,
    addNew: false
  };

  async getPolicies(page) {
    await fetch(baseURL + "policies/6/" + page + "/", {
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

        var tempPolicies = []

        data.entries.forEach(policy => {
          var tempInfo = []

          tempInfo.push(policy['name'])
          tempInfo.push(policy['filter'])

          var tags = ""
          policy.tags.forEach(tag => {
            tags += tag
            tags += ", "
          })

          tags = tags.substr(0, tags.length - 2)
          if (tags.length > 30) {
            tags = tags.substr(0, 30) + "..."
          }

          tempInfo.push(tags)

          var bots = ""
          policy.bots.forEach(bot => {
            bots += "@" + bot.bot_name

            bots += ", "
          })

          bots = bots.substr(0, bots.length - 2)
          if (bots.length > 45) {
            bots = bots.substr(0, 45) + "..."
          } else if (bots.length == "") {
            bots = <span style={{ color: "#999" }}><i class="fas fa-minus"></i></span>
          }

          tempInfo.push(bots)

          if (policy.active) {
            tempInfo.push(<Badge pill color="success" style={{ fontSize: "11px" }}>Active</Badge>)
            tempInfo.push(
              <Button block outline color="warning"
                onClick={() =>
                  this.handleOpenDeactivate(policy)
                }
              >
                <i class="fas fa-pause"></i>
              </Button>
            )
          } else {
            tempInfo.push(<Badge pill color="danger" style={{ fontSize: "11px" }}>Inactive</Badge>)
            tempInfo.push(
              <Button block outline color="success"
                onClick={() =>
                  this.handleOpenActivate(policy)
                }
              >
                <i class="fas fa-play"></i>
              </Button>
            )
          }

          tempInfo.push(<Button block outline color="danger"
            onClick={() =>
              this.handleOpenDelete(policy)
            }
          >
            <i class="fas fa-times"></i>
          </Button>)

          tempInfo.push(policy)

          tempPolicies.push(tempInfo);
        })

        var empty = false
        if (tempPolicies.length == 0) {
          empty = true
        }

        this.setState({
          policies: tempPolicies,
          noPages: data.num_pages,
          curPage: page,
          empty: empty,
          policy: this.state.policy
        })
      }
    }).catch(error => {
      console.log("error: " + error);
      this.setState({
        error: error
      })
    });
  }

  async getBotList() {
    await fetch(baseURL + "twitter/bots", {
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
          tempBots.push({ label: "@" + bot.screen_name, value: bot.user_id });
        })

        this.setState({
          allBots: tempBots
        })
      }
    }).catch(error => {
      console.log("error: " + error);
      this.setState({
        error: true,
      })
    });
  }

  async getNumbers() {
    await fetch(baseURL + "policies/numbers/", {
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
        console.log(data)

        this.setState({
          noPolicies: data.total,
          noActivePolicies: data.active
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
    await this.getPolicies(1, true)
    await this.getBotList(1)
    await this.getNumbers()

    await this.setState({
      doneLoading: true
    })

    if (!this.state.error) {
      this.changeSelected(this.state.policies[0])
    }

    console.log(this.props.success)

    if (this.props.success != null && this.props.success) {
      toast.success('🏷️ New policy succesfully assigned!', {
        position: "top-center",
        autoClose: 2500,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true
      });
    }
  }


  // Methods //////////////////////////////////////////////////////////
  handleOpenDeactivate(policy) {
    this.setState({
      modal: true,
      modalType: "DEACTIVATE",
      modalPolicy: policy
    });
  }

  handleOpenActivate(policy) {
    this.setState({
      modal: true,
      modalType: "ACTIVATE",
      modalPolicy: policy
    });
  }

  handleOpenDelete(policy) {
    this.setState({
      modal: true,
      modalType: "DELETE",
      modalPolicy: policy
    });
  }

  handleDeactivate() {
    //TODO: DEACTIVATE BOT

    //TODO: ADD FAILURE OPTION
    if (true) {
      toast.warning('⏸️ Policy successfully deactivated!', {
        position: "top-center",
        autoClose: 2500,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true
      });
    } else {
      toast.error('Sorry, there was an error deactivating the policy! Please try again later.', {
        position: "top-center",
        autoClose: 7500,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true
      });
    }


    this.handleClose()
  }

  handleActivate() {
    //TODO: ACTIVATE BOT

    //TODO: ADD FAILURE OPTION
    if (true) {
      toast.success('▶️ Policy successfully activated', {
        position: "top-center",
        autoClose: 2500,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true
      });
    } else {
      toast.error('Sorry, there was an error activating the policy! Please try again later.', {
        position: "top-center",
        autoClose: 7500,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true
      });
    }


    this.handleClose()
  }

  async handleDelete() {
    var policy = this.state.modalPolicy
    this.handleClose()

    await this.setState({
      processing: true
    })

    await fetch(baseURL + "policies/remove/" + policy.id + "/", {
      method: "DELETE",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
    }).then(response => {
      if (response.ok) return response.json();
      else {
        throw new Error(response.status);
      }
    }).then(data => {

      this.getPolicies(this.state.curPage)
      this.changeSelected(this.state.policies[0])

      toast.warning('🗑️ Policy successfully deleted', {
        position: "top-center",
        autoClose: 2500,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true
      });

      this.setState({
        processing: false
      })

    }).catch(error => {
      console.log("error: " + error);
      this.setState({
        processing: false,
      })
      toast.error('Sorry, there was an error deleting the policy! Please try again later.', {
        position: "top-center",
        autoClose: 7500,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true
      });
    });
  }

  handleClose() {
    this.setState({
      modal: false,
      modalType: null,
      modalPolicy: null
    });
  }

  handleOpenAdd() {
    this.setState({
      addNew: true
    })
  }

  async confirmEdit() {
    if (!this.checkForChange()) {
      toast.info('No changes have been made!', {
        position: "top-center",
        autoClose: 2500,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true
      });
      document.getElementById("error").style.visibility = "hidden"

    } else if (document.getElementById("name").value == null || document.getElementById("name").value == "" || this.state.tags == null || this.state.tags.length == 0) {
      document.getElementById("error").style.visibility = ""
    } else {
      document.getElementById("error").style.visibility = "hidden"

      var bots = []
      for (var i = 0; i < this.state.bots.length; i++) {
        bots.push(this.state.bots[i].value)
      }

      var tags = []
      for (var i = 0; i < this.state.tags.length; i++) {
        tags.push(this.state.tags[i].value)
      }

      var filter = this.state.filter.value

      var name = document.getElementById("name").value

      var success = false
      var tempInfo = []

      await this.setState({
        processing: true
      })

      await fetch(baseURL + "policies/update/" + this.state.policy[7].id + "/", {
        method: "PUT",
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          bots: bots,
          tags: tags,
          filter: filter,
          name: name
        })
      }).then(response => {
        if (response.ok) return response.json();
        else {
          if (response.status === 403) {
            return { error: response.json(), code: 403 }
          } else if (response.status === 409) {
            return { error: response.json(), code: 409 }
          } else {
            throw new Error(response.status);
          }
        }
      }).then(data => {
        if (data.code != null) {
          if (data.code == 403) {
            toast.error('There already exists a policy with that name!', {
              position: "top-center",
              autoClose: 7500,
              hideProgressBar: false,
              closeOnClick: true,
              pauseOnHover: true,
              draggable: true
            });
          } else {
            toast.error('There already exists a policy with those tags! (Two policies can\'t share more than 1 tag in common)', {
              position: "top-center",
              autoClose: 7500,
              hideProgressBar: false,
              closeOnClick: true,
              pauseOnHover: true,
              draggable: true
            });
          }
        } else {
          document.getElementById("loadedTable").style.visibility = "hidden"
          document.getElementById("loadingTable").style.display = ""

          /////////////////////////////////////////////////////////////////////

          this.setState({ policy: null, policies: [] })

          var policy = data.data

          tempInfo.push(policy['name'])
          tempInfo.push(policy['filter'])

          var tags = ""
          policy.tags.forEach(tag => {
            tags += tag
            tags += ", "
          })

          tags = tags.substr(0, tags.length - 2)
          if (tags.length > 30) {
            tags = tags.substr(0, 30) + "..."
          }

          tempInfo.push(tags)

          var bots = ""
          policy.bots.forEach(bot => {
            bots += "@" + bot.bot_name
            bots += ", "
          })

          bots = bots.substr(0, bots.length - 2)
          if (bots.length > 45) {
            bots = bots.substr(0, 45) + "..."
          } else if (bots.length == "") {
            bots = <span style={{ color: "#999" }}><i class="fas fa-minus"></i></span>
          }

          tempInfo.push(bots)

          if (policy.active) {
            tempInfo.push(<Badge pill color="success" style={{ fontSize: "11px" }}>Active</Badge>)
            tempInfo.push(
              <Button block outline color="warning"
                onClick={() =>
                  this.handleOpenDeactivate(policy)
                }
              >
                <i class="fas fa-pause"></i>
              </Button>
            )
          } else {
            tempInfo.push(<Badge pill color="danger" style={{ fontSize: "11px" }}>Inactive</Badge>)
            tempInfo.push(
              <Button block outline color="success"
                onClick={() =>
                  this.handleOpenActivate(policy)
                }
              >
                <i class="fas fa-play"></i>
              </Button>
            )
          }

          tempInfo.push(<Button block outline color="danger"
            onClick={() =>
              this.handleOpenDelete(policy)
            }
          >
            <i class="fas fa-times"></i>
          </Button>)

          tempInfo.push(policy)

          /////////////////////////////////////////////////////////////////////

          success = true
        }

      }).catch(error => {
        console.log("error: " + error);
        success = false
      });

      if (success) {
        await this.getPolicies(this.state.curPage)
        await this.changeSelected(tempInfo)

        document.getElementById("loadedTable").style.visibility = ""
        document.getElementById("loadingTable").style.display = "none"

        toast.info('Policy succesfully altered!', {
          position: "top-center",
          autoClose: 2500,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true
        });
      } else {
        toast.error('Sorry, there was an error updating the policy! Please try again later.', {
          position: "top-center",
          autoClose: 7500,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true
        })
      }
      this.setState({
        processing: false,
      })
    }
  }



  ////////////////////////////////////////////////////////

  changePage = async (event, value) => {
    document.getElementById("loadedTable").style.visibility = "hidden"
    document.getElementById("loadingTable").style.display = ""

    this.setState({
      curPage: value
    })

    if (this.state.policy != null) {
      if (document.getElementsByName(this.state.policy[7].id) != null) {
        console.log(document.getElementsByName(this.state.policy[0]).length)

        for (var i = 0; i < 4; i++) {
          document.getElementsByName(this.state.policy[7].id)[i].style.color = ""
          document.getElementsByName(this.state.policy[7].id)[i].style.fontWeight = ""
        }
      }
    }
    await this.setState({
      policy: null,
    })

    await this.getPolicies(value)
    this.changeSelected(this.state.policies[0])

    document.getElementById("loadedTable").style.visibility = "visible"
    document.getElementById("loadingTable").style.display = "none"
  };

  changeSelectedFilter = async (selectedOption) => {
    if (selectedOption != null) {
      await this.setState({ filter: selectedOption });

    } else {
      await this.setState({ filter: null });
    }

    if (this.checkForChange()) {
      document.getElementById("changed").style.visibility = ""
    } else {
      document.getElementById("changed").style.visibility = "hidden"
    }
  }

  addNewTags = async (newValue, actionMeta) => {
    var tags = []
    if (newValue != null && newValue.length > 0) {
      tags = newValue
    }

    await this.setState({
      tags: tags
    })

    if (this.checkForChange()) {
      document.getElementById("changed").style.visibility = ""
    } else {
      document.getElementById("changed").style.visibility = "hidden"
    }
  };

  addNewBots = async (newValue, actionMeta) => {
    var bots = []
    if (newValue != null && newValue.length > 0) {
      bots = newValue
    }

    await this.setState({
      bots: bots
    })

    if (this.checkForChange()) {
      document.getElementById("changed").style.visibility = ""
    } else {
      document.getElementById("changed").style.visibility = "hidden"
    }
  };

  changeText = () => {
    try {
      if (this.checkForChange()) {
        document.getElementById("changed").style.visibility = ""
      } else {
        document.getElementById("changed").style.visibility = "hidden"
      }
    } catch (err) {
      console.log()
    }
  };


  checkForChange() {
    if (this.state.policy[7].name != document.getElementById("name").value) {
      return true
    }

    ///////////////////
    var bots = []
    var botsOriginal = []
    this.state.bots.forEach(bot => {
      bots.push(bot.value)
    })

    this.state.policy[7].bots.forEach(bot => {
      botsOriginal.push(bot.bot_id)
    })

    bots = bots.sort().join()
    botsOriginal = botsOriginal.sort().join()

    if (bots != botsOriginal) {
      return true
    }

    ///////////////////
    var tags = []
    var tagsOriginal = []
    this.state.tags.forEach(tag => {
      tags.push(tag.value)
    })

    this.state.policy[7].tags.forEach(tag => {
      tagsOriginal.push(tag)
    })

    tags = tags.sort().join()
    tagsOriginal = tagsOriginal.sort().join()
    if (tags != tagsOriginal) {
      return true
    }

    if (this.state.policy[7].filter != this.state.filter.value) {
      return true
    }

    return false
  }

  async changeSelected(selected) {
    if (this.state.policy != null) {
      if (document.getElementsByName(this.state.policy[7].id) != null) {
        console.log(document.getElementsByName(this.state.policy[0]).length)

        for (var i = 0; i < 4; i++) {
          document.getElementsByName(this.state.policy[7].id)[i].style.color = ""
          document.getElementsByName(this.state.policy[7].id)[i].style.fontWeight = ""
        }
      }
    }
    await this.setState({
      policy: selected,
    })

    if (this.state.policy != null) {
      if (document.getElementsByName(this.state.policy[7].id) != null) {
        for (var i = 0; i < 4; i++) {
          document.getElementsByName(this.state.policy[7].id)[i].style.color = "#1da1f2"
          document.getElementsByName(this.state.policy[7].id)[i].style.fontWeight = "bold"
        }
      }

      document.getElementById("name").value = this.state.policy[7].name
      document.getElementById("title").textContent = this.state.policy[7].name
      document.getElementById("changed").style.visibility = "hidden"

      var bots = []
      this.state.policy[7].bots.forEach(bot => {
        bots.push({ label: bot.bot_name, value: bot.bot_id })
      })

      var tags = []
      this.state.policy[7].tags.forEach(tag => {
        tags.push({ label: tag, value: tag })
      })

      await this.setState({
        filter: { label: this.state.policy[7].filter, value: this.state.policy[7].filter },
        bots: bots,
        tags: tags
      })
    }
  };

  /////////////////////////////////////////////////////////////////////

  loading = () => <div className="fadeIn pt-1 text-center"><ReactLoading type={"cubes"} color="#1da1f2" /></div>

  render() {

    if (!this.state.addNew) {
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
        var modal = null
        if (this.state.modalPolicy != null) {
          if (this.state.modalType == "DELETE") {
            modal = <Dialog class="fade-in"
              open={this.state.modal}
              onClose={() => this.handleClose()}
              aria-labelledby="alert-dialog-title"
              aria-describedby="alert-dialog-description"
            >
              <DialogTitle id="alert-dialog-title">
                {"❌ 🏷️ Are you sure you want to completely delete this policy?"}
              </DialogTitle>
              <DialogContent>
                <DialogContentText id="alert-dialog-description">
                  Policy <strong>{this.state.modalPolicy.name}</strong> will cease to exist and its assigned bots will stop following its rules. This action is non-reversible
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
                {"▶️ Are you sure you want to activate this policy?"}
              </DialogTitle>
              <DialogContent>
                <DialogContentText id="alert-dialog-description">
                  Policy <b>{this.state.modalPolicy.name}</b> will be activated. This means that all bots assigned to it will start following its rules. Proceed at your own caution.
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
                {"⏸️ Are you sure you want to deactivate this policy?"}
              </DialogTitle>
              <DialogContent>
                <DialogContentText id="alert-dialog-description">
                  Policy <b>{this.state.modalPolicy.name}</b> will be activated. This means that all bots assigned to it will stop following its rules.
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
          }
        }

        var policies = <CardBody></CardBody>
        var table = <div></div>
        if (this.state.empty) {
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
                Hmmm... there don't seem to be any defined policies, how about creating a new one? 🤔
                </h5>
            </div>


        } else {
          var { classes } = this.props;

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
            <div className={classes.tableResponsive}>
              <Table className={classes.table}>
                <TableHead className={classes["primaryTableHeader"]}>
                  <TableRow className={classes.tableHeadRow}>
                    {["Name", "Type", "Tags", "Bots", "Status", "", "", ""].map((prop, key) => {
                      return (
                        <TableCell
                          className={classes.tableCell + " " + classes.tableHeadCell}
                          key={key}
                        >
                          {prop}
                        </TableCell>
                      );
                    })}
                  </TableRow>
                </TableHead>

                <TableBody>
                  {this.state.policies.map((prop, key) => {
                    var id = prop[7].id
                    return (
                      <TableRow hover key={key} className={classes.tableBodyRow} style={{ cursor: "pointer" }} onClick={() => this.changeSelected(prop)}>
                        {prop.map((prop, key) => {
                          if (key != 7) {
                            return (
                              <TableCell name={id} className={classes.tableCell} key={key}>
                                {prop}
                              </TableCell>
                            );
                          }
                        })}
                      </TableRow>
                    );
                  })}
                </TableBody>
              </Table>
            </div>
          </div>
        }

        policies =
          <CardBody>
            <div style={{ position: "relative" }}>
              {table}
              <div
                id="loadingTable"
                style={{
                  zIndex: 10,
                  position: "absolute",
                  top: "10%",
                  left: "42%",
                  display: "none"
                }}>
                <ReactLoading width={"150px"} type={"cubes"} color="#1da1f2" />
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
            </div>
          </CardBody>



        var processing = <div></div>
        if (this.state.processing) {
          processing = <div id="loading">
            <div className="animated fadeOut animated" style={{ width: "100%", height: "100%", top: 0, left: 0, position: "absolute", backgroundColor: "white", opacity: 0.6, zIndex: 11 }}>
            </div>
            <div style={{ zIndex: 11, position: "relative" }}>
              <div className="animated fadeOut animated" style={{ width: "100%", marginTop: "10%", position: "absolute", zIndex: 12 }}>
                <FadeIn>
                  <Lottie options={this.state.animationOptions} height={"30%"} width={"30%"} />
                </FadeIn>
              </div>
            </div>
          </div>
        }
        return (
          <div className="animated fadeIn">
            {processing}
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
              <ReactTooltip
                place="right"
                effect="solid"
              />
              <Row>
                <Col xs="12" sm="12" md="9">
                  <Card>
                    <CardHeader color="primary">
                      <h3 style={{ color: "white" }}>
                        <strong>Policies</strong>
                      </h3>
                      <h5 style={{ color: "white" }}>
                        List with all created Policies
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
                        <i class="fas fa-tags"></i>
                      </CardIcon>
                      <p style={{
                        color: '#999',
                        margin: "0",
                        fontSize: "14px",
                        marginTop: "0",
                        paddingTop: "10px",
                        marginBottom: "0"
                      }}>Total number of active policies</p>
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
                        {this.state.noActivePolicies} / {this.state.noPolicies}
                      </h3>
                    </CardHeader>
                    <CardBody style={{ minHeight: "38px" }}>
                    </CardBody>
                  </Card>
                </Col>
              </Row>
              <Row>
                <Col xs="12" sm="12" md="8">
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
                      }} > Defined Policies</h4>
                      <Button block outline color="light" style={{
                        width: "150px", marginTop: "15px"
                      }} onClick={() => this.handleOpenAdd()}
                      >Add new</Button>

                    </CardHeader>
                    {policies}
                  </Card>
                </Col>
                <Col xs="12" sm="12" md="4">
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
                      }} > Policy Info - <strong id="title"></strong></h4>

                    </CardHeader>
                    <CardBody>
                      <Row style={{ marginTop: "25px" }}>
                        <Col md="8">
                          <FormGroup>
                            <Input type="text" id="name" placeholder="Policy name" onChange={() => { this.changeText() }} required />
                          </FormGroup>
                        </Col>
                        <Col md="4">
                          <FormGroup>
                            <Select
                              defaultValue={[]}
                              id="filter"
                              onChange={this.changeSelectedFilter}
                              value={this.state.filter || ''}
                              options={[{ value: "Target", label: "Target" }, { value: "Keywords", label: "Keywords" }]}
                              className="basic-single"
                              classNamePrefix="select"
                              placeholder="Filter"
                            />
                            <i data-tip="Target specifies the twitter name of users you want the bot to attempt to follow, whilst Keywords define tags that a tweet should be classified as for the bot to have interest in" style={{ color: "#1da1f2", float: "right", marginTop: "10px", marginRight: "5px" }} class="fas fa-info-circle"></i>
                          </FormGroup>
                        </Col>
                      </Row>

                      <Row style={{ marginTop: "30px", minHeight: "48px" }}>
                        <Col md="12">
                          <CreatableSelect
                            isMulti
                            id="tags"
                            value={this.state.tags}
                            onChange={this.addNewTags}
                            options={this.state.tags}
                            components={makeAnimated()}
                            placeholder="Tags"
                          />
                        </Col>
                      </Row>

                      <Row style={{ marginTop: "30px", minHeight: "48px" }}>
                        <Col md="12">
                          <Select
                            isMulti
                            id="bots"
                            value={this.state.bots}
                            onChange={this.addNewBots}
                            options={this.state.allBots}
                            components={makeAnimated()}
                            placeholder="Bots"
                          />
                        </Col>
                      </Row>

                      <Row style={{ marginTop: "30px" }}>
                        <Col sm="12" md="12" xs="12">
                          <span id="changed" style={{ visibility: "hidden", color: "#999" }}>*Changes made but still not applied. Please click confirm to save changes.</span>
                        </Col>
                      </Row>
                      <Row>
                        <Col sm="12" md="12" xs="12">
                          <span id="error" style={{ visibility: "hidden", color: "#f86c6b" }}>Sorry, you can't leave the name empty and must define at least one tag!</span>
                        </Col>
                      </Row>


                      <Row style={{ marginTop: "10px" }}>
                        <Col sm="12" md="12" xs="12">
                          <Button block outline color="success" onClick={() => this.confirmEdit()} style={{
                            width: "150px", marginTop: "15px", borderWidth: "2px", float: "right"
                          }}>                  <i class="fas fa-edit"></i> <strong style={{ marginLeft: "3px" }}>Confirm</strong>
                          </Button>
                        </Col>
                      </Row>
                    </CardBody>

                  </Card>
                </Col>
              </Row>

              {modal}
            </Container>
          </div >
        );
      }
    } else {
      return (<NewPolicy />)
    }
  }
}


export default withStyles(useStyles)(Policies);

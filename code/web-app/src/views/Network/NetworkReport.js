import React, { Component, lazy, Suspense } from 'react';

import baseURL from '../../variables/baseURL'
import {
  Container, Row, Col, Button,
  Input,
  FormGroup, Label,
} from 'reactstrap';

import Card from "../../components/Card/Card";
import CardHeader from "../../components/Card/CardHeader";
import CardBody from "../../components/Card/CardBody";

import 'react-toastify/dist/ReactToastify.css';

import FadeIn from "react-fade-in";
import Lottie from "react-lottie";

import ReactTooltip from "react-tooltip";

import * as loadingAnim from "../../assets/animations/squares_1.json";

import Select from 'react-select';
import AsyncSelect from 'react-select/async';
import CreatableSelect from 'react-select/creatable';
import makeAnimated from 'react-select/animated';

import 'react-toastify/dist/ReactToastify.css';
import { ToastContainer, toast, Flip } from 'react-toastify';

import ToggleButton from '@material-ui/lab/ToggleButton';
import ToggleButtonGroup from '@material-ui/lab/ToggleButtonGroup';

import Dialog from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogTitle from "@material-ui/core/DialogTitle";

import Network from "./Network";

class NetworkReport extends Component {
  constructor() {
    super();
  }

  state = {
    error: null,
    doneLoading: false,
    processing: false,

    animationOptions: {
      loop: true, autoplay: true, animationData: loadingAnim.default, rendererSettings: {
        preserveAspectRatio: "xMidYMid slice"
      }
    },

    start: {
      type: null,
      nodes: null,
      relation: null,
      direction: null
    },

    intermediate: {
      type: [],
      nodes: [],
      relation: [],
      direction: []
    },

    end: {
      type: null,
      nodes: null
    },

    modal: false,

    fileType: "json",

    returnValues: null,

    intermediateRelOptions: [{ value: "a_0", label: "All Relations" }, { value: "FOLLOWS_1", label: "Follows" }, { value: "QUOTED_1", label: "Quoted" }, { value: "REPLIED_1", label: "Replied" }, { value: "RETWEETED_1", label: "Retweeted" }, { value: "WROTE_1", label: "Wrote" }],
    intermediateTypeOptions: [{ value: "a_0", label: "All Types" }, { value: "Bot_1", label: "Bot" }, { value: "User_1", label: "User" }, { value: "Tweet_1", label: "Tweet" }],
    intermediateDirectionOptions: [{ value: "Outgoing_1", label: "Outgoing" }, { value: "Ingoing_1", label: "Ingoing" }, { value: "Bisexual_1", label: "Bidirectional" }]
  };

  async componentDidMount() {
    this.setState({
      doneLoading: true
    })
  }

  // Search ///////////////////////////////////////////////////////////


  loadOptions = inputValue =>
    new Promise(resolve => {
      if (inputValue == "" || inputValue == null) {
        var requestValues = [{ "value": "aaaaaaaaaaaaaaa_" + Date.now(), "label": "All Nodes" }]
        resolve(requestValues)
      } else {
        if (!inputValue.match("^[A-Za-z0-9 ]+$")) {
          return
        } else {
          var type = this.state.start.type
          if (type == null || type.value == "" || type.value.split("_").length == 2) {
            type = null
          } else {
            type = type.value
          }
          var requestValues = this.search(inputValue, type)
          resolve(requestValues)
        }
      }
    });

  loadOptions2 = inputValue =>
    new Promise(resolve => {
      if (inputValue == "" || inputValue == null) {
        var requestValues = [{ "value": "aaaaaaaaaaaaaaa_" + Date.now(), "label": "All Nodes" }]
        resolve(requestValues)
      } else {
        if (!inputValue.match("^[A-Za-z0-9 ]+$")) {
          return
        } else {
          var type = this.state.end.type
          if (type == null || type.value == "" || type.value.split("_").length == 2) {
            type = null
          } else {
            type = type.value
          }
          var requestValues = this.search(inputValue, type)
          resolve(requestValues)
        }
      }
    });


  loadOptions3 = inputValue =>
    new Promise(resolve => {
      if (inputValue == "" || inputValue == null) {
        var requestValues = [{ "value": "aaaaaaaaaaaaaaa_" + Date.now(), "label": "All Nodes" }]
        resolve(requestValues)
      } else {
        if (!inputValue.match("^[A-Za-z0-9 ]+$")) {
          return
        } else {
          toast.dismiss(this.firstErrorToast)
          var requestValues = this.search(inputValue, null)
          resolve(requestValues)
        }
      }
    });

  async search(input, type) {
    var tempData = []

    if (type == null) {
      await fetch(baseURL + "twitter/strict/search/" + input + "/", {
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
        tempData.push({ "value": "aaaaaaaaaaaaaaa_" + Date.now(), "label": "All Nodes" })

        if (data != null && data != {}) {
          data = data.data

          data.User.forEach(user => {
            tempData.push({ "value": user.id, "label": "(User) " + user.name + " - @" + user.screen_name })
          })

          data.Bot.forEach(user => {
            tempData.push({ "value": user.id, "label": "(Bot) " + user.name + " - @" + user.screen_name })
          })

          data.Tweet.forEach(user => {
            tempData.push({ "value": user.id, "label": "(Tweet) #" + user })
          })

        }
      }).catch(error => {
        console.log("error: " + error);
        this.setState({
          error: true,
        })
      });

    } else if (type != "Tweet") {
      if (input != "") {
        await fetch(baseURL + "twitter/users/strict/search/" + type + "/" + input + "/", {
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
            tempData.push({ "value": null, "label": "All Nodes" })
            data.forEach(user => {
              tempData.push({ "value": user.id, "label": "(" + type + ") " + user.name + " - @" + user.screen_name })
            })

          }
        }).catch(error => {
          console.log("error: " + error);
          this.setState({
            error: true,
          })
        });
      }
      else {
        if (type == "Bot") {
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
              tempData.push({ "value": "aaaaaaaaaaaaaaa_" + Date.now(), "label": "All Nodes" })

              data.forEach(user => {
                tempData.push({ "value": user.user_id, "label": "(" + type + ") " + user.name + " - @" + user.screen_name })
              })
            }
          }).catch(error => {
            console.log("error: " + error);
            this.setState({
              error: true,
            })
          });
        } else {
          await fetch(baseURL + "twitter/users/30/1", {
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
              tempData.push({ "value": "aaaaaaaaaaaaaaa_" + Date.now(), "label": "All Nodes" })

              data.entries.forEach(user => {
                tempData.push({ "value": user.user_id, "label": "(" + type + ") " + user.name + " - @" + user.screen_name })
              })

            }
          }).catch(error => {
            console.log("error: " + error);
            this.setState({
              error: true,
            })
          });
        }
      }
    } else {
      if (input == "") {
        await fetch(baseURL + "twitter/tweets/all/30/1/", {
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
            tempData.push({ "value": "aaaaaaaaaaaaaaa_" + Date.now(), "label": "All Nodes" })
            data.entries.forEach(tweet => {
              tempData.push({ "value": tweet.tweet_id, "label": "(Tweet) #" + tweet.tweet_id })
            })

          }
        }).catch(error => {
          console.log("error: " + error);
          this.setState({
            error: true,
          })
        });
      } else {
        await fetch(baseURL + "twitter/tweets/strict/search/" + input + "/", {
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
            tempData.push({ "value": "aaaaaaaaaaaaaaa_" + Date.now(), "label": "All Nodes" })
            data.forEach(tweet => {
              tempData.push({ "value": tweet.id, "label": "(Tweet) #" + tweet })
            })

          }
        }).catch(error => {
          console.log("error: " + error);
          this.setState({
            error: true,
          })
        });
      }
    }

    return tempData
  }

  // Methods //////////////////////////////////////////////////////////
  changeSelectedStartType = (selectedOption) => {
    if (selectedOption != null) {
      this.setState({ start: { type: selectedOption, nodes: [], relation: this.state.start.relation } });
    } else {
      this.setState({ start: { type: { value: "a_0", label: "All Types" }, nodes: [], relation: this.state.start.relation } });
    }
  }


  changeSelectedStartNodes = (selectedOption) => {
    if (selectedOption != null) {
      this.setState({ start: { type: this.state.start.type, nodes: selectedOption, relation: this.state.start.relation, direction: this.state.start.direction } });
    } else {
      this.setState({ start: { type: this.state.start.type, nodes: [], relation: this.state.start.relation, direction: this.state.start.direction } });
    }
  }

  changeSelectedStartRelationType = (selectedOption) => {
    if (selectedOption != null) {
      this.setState({ start: { type: this.state.start.type, nodes: this.state.start.nodes, relation: selectedOption, direction: this.state.start.direction } });
    } else {
      this.setState({ start: { type: this.state.start.type, nodes: this.state.start.nodes, relation: { value: "FOLLOWS", label: "Follows" }, direction: this.state.start.direction } });
    }
  }

  changeSelectedStartDirectionType = (selectedOption) => {
    if (selectedOption != null) {
      this.setState({ start: { type: this.state.start.type, nodes: this.state.start.nodes, relation: this.state.start.relation, direction: selectedOption } });
    } else {
      this.setState({ start: { type: this.state.start.type, nodes: this.state.start.nodes, relation: this.state.start.relation, direction: [{ value: "Outgoing", label: "Outgoing" }, { value: "Ingoing", label: "Ingoing" }, { value: "Bisexual", label: "Any Direction" }] } });
    }
  }

  changeSelectedEndType = (selectedOption) => {
    if (selectedOption != null) {
      this.setState({ end: { type: selectedOption, nodes: this.state.end.nodes } });
    } else {
      this.setState({ end: { type: { value: "a_0", label: "All Types" }, nodes: [] } });
    }
  }

  changeSelectedEndType = (selectedOption) => {
    if (selectedOption != null) {
      this.setState({ end: { type: selectedOption, nodes: this.state.end.nodes } });
    } else {
      this.setState({ end: { type: { value: "a_0", label: "All Types" }, nodes: [] } });
    }
  }

  changeSelectedEndNodes = (selectedOption) => {
    if (selectedOption != null) {
      this.setState({ end: { type: this.state.end.type, nodes: selectedOption } });
    } else {
      this.setState({ end: { type: this.state.end.type, nodes: [] } });
    }
  }

  changeSelectedIntermediateType = (selectedOption) => {
    if (selectedOption != null) {
      if (selectedOption.length + 4 > this.state.intermediateTypeOptions.length) {
        var newPush = selectedOption[selectedOption.length - 1]
        var newValue = newPush.value
        var newNumber = parseInt(newValue.split("_")[1]) + 1
        newValue = newValue.split("_")[0] + "_" + newNumber

        var newElement = { value: newValue, label: newPush.label }

        var newTypes = this.state.intermediateTypeOptions
        newTypes.push(newElement)
        this.setState({ intermediate: { type: selectedOption, nodes: this.state.intermediate.nodes, relation: this.state.intermediate.relation }, intermediateTypeOptions: newTypes.sort((a, b) => a.label > b.label) });

      } else {
        this.setState({ intermediate: { type: selectedOption, nodes: this.state.intermediate.nodes, relation: this.state.intermediate.relation } });
      }

    } else {
      this.setState({ intermediate: { type: [], nodes: this.state.intermediate.nodes, relation: this.state.intermediate.relation }, intermediateTypeOptions: [{ value: "a_0", label: "All Relations" }, { value: "Bot_1", label: "Bot" }, { value: "User_1", label: "User" }, { value: "Tweet_1", label: "Tweet" }] });
    }
  }

  changeSelectedIntermediateRelation = (selectedOption) => {
    if (selectedOption != null) {

      if (selectedOption.length + 6 > this.state.intermediateRelOptions.length) {
        var newPush = selectedOption[selectedOption.length - 1]
        var newValue = newPush.value
        var newNumber = parseInt(newValue.split("_")[1]) + 1
        newValue = newValue.split("_")[0] + "_" + newNumber

        var newElement = { value: newValue, label: newPush.label }

        var newTypes = this.state.intermediateRelOptions
        newTypes.push(newElement)
        this.setState({ intermediate: { type: this.state.intermediate.type, nodes: this.state.intermediate.nodes, direction: this.state.intermediate.direction, relation: selectedOption }, intermediateRelOptions: newTypes.sort((a, b) => a.label > b.label) });

      } else {
        this.setState({ intermediate: { type: this.state.intermediate.type, nodes: this.state.intermediate.nodes, direction: this.state.intermediate.direction, relation: selectedOption } });
      }

    } else {
      this.setState({ intermediate: { type: this.state.intermediate.type, nodes: this.state.intermediate.nodes, direction: this.state.intermediate.direction, relation: [] }, intermediateRelOptions: [{ value: "a_0", label: "All Relations" }, { value: "FOLLOWS_1", label: "Follows" }, { value: "QUOTED_1", label: "Quoted" }, { value: "REPLIED_1", label: "Replied" }, { value: "RETWEETED_1", label: "Retweeted" }, { value: "WROTE_1", label: "Wrote" }] });
    }
  }

  changeSelectedIntermediateDirection = (selectedOption) => {
    if (selectedOption != null) {

      if (selectedOption.length + 3 > this.state.intermediateDirectionOptions.length) {
        var newPush = selectedOption[selectedOption.length - 1]
        var newValue = newPush.value
        var newNumber = parseInt(newValue.split("_")[1]) + 1
        newValue = newValue.split("_")[0] + "_" + newNumber

        var newElement = { value: newValue, label: newPush.label }

        var newTypes = this.state.intermediateDirectionOptions
        newTypes.push(newElement)
        this.setState({ intermediate: { type: this.state.intermediate.type, nodes: this.state.intermediate.nodes, relation: this.state.intermediate.relation, direction: selectedOption }, intermediateDirectionOptions: newTypes.sort((a, b) => a.label > b.label) });

      } else {
        this.setState({ intermediate: { type: this.state.intermediate.type, nodes: this.state.intermediate.nodes, relation: this.state.intermediate.relation, direction: selectedOption } });
      }

    } else {
      this.setState({ intermediate: { type: this.state.intermediate.type, nodes: this.state.intermediate.nodes, relation: this.state.intermediate.relation, direction: [] }, intermediateDirectionOptions: [{ value: "Outgoing_1", label: "Outgoing" }, { value: "Ingoing_1", label: "Ingoing" }, { value: "Bisexual_1", label: "Bidirectional" }] });
    }
  }

  changeIntermediateNodes = (selectedOption) => {
    if (selectedOption != null) {
      this.setState({ intermediate: { type: this.state.intermediate.type, nodes: selectedOption, relation: this.state.intermediate.relation } });
    } else {
      this.setState({ intermediate: { type: this.state.intermediate.type, nodes: [], relation: this.state.intermediate.relation } });
    }
  }

  changeType = async (event, value) => {
    await this.setState({
      fileType: value
    })
  };

  clearStart = async () => {
    await this.setState({
      start: {
        type: null,
        nodes: null,
        relation: null
      },
    })
  };

  clearEnd = async () => {
    await this.setState({
      end: {
        type: null,
        nodes: null,
        relation: null
      },
    })
  };

  confirm() {
    var search = {}

    var error = false

    /*
    if (this.state.end.nodes == null || this.state.end.nodes.length == 0) {
      toast.error('You need to specify the finishing node!', {
        position: "top-center",
        autoClose: 7500,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true
      });

      error = true
      document.getElementById("errorNothing").style.display = ""

    } else {
      document.getElementById("errorNothing").style.display = "none"
    }
    */

    if (document.getElementById("limit") == null || (document.getElementById("limit").value != "" && document.getElementById("limit").value.match("^[0-9]+$") == null)) {
      toast.error('The specified limit must be a number!', {
        position: "top-center",
        autoClose: 7500,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true
      });

      error = true
      document.getElementById("errorNumber").style.display = ""

    } else {
      document.getElementById("errorNumber").style.display = "none"
    }

    if (this.state.intermediate.type.length != 0 || this.state.intermediate.nodes.length != 0 || this.state.intermediate.relation.length != 0 || this.state.intermediate.direction.length != 0) {
      try {
        if (this.state.intermediate.type.length != this.state.intermediate.nodes.length || this.state.intermediate.type.length != this.state.intermediate.relation.length || this.state.intermediate.nodes.length != this.state.intermediate.relation.length || this.state.intermediate.type.relation != this.state.intermediate.direction.length) {
          error = true
          toast.error('You need to specify the same amount of intermediate nodes, node types, relation types and relation directions!', {
            position: "top-center",
            autoClose: 7500,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true
          });
          document.getElementById("errorOops").style.visibility = ""
        } else {
          document.getElementById("errorOops").style.visibility = "hidden"
        }
      } catch (erro) {
        error = true
        toast.error('You need to specify the same amount of intermediate nodes, node types, relation types and relation directions!', {
          position: "top-center",
          autoClose: 7500,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true
        });

        document.getElementById("errorOops").style.visibility = ""
      }
    } else {
      document.getElementById("errorOops").style.visibility = "hidden"
    }

    if (!error) {
      //////////////////////////////////////////////////
      var checkboxes = document.querySelectorAll('input[name=option-check]:checked')
      var fields = { "Bot": [], "Tweet": [], "User": [] }
      checkboxes.forEach(checked => {
        if (checked.id.split("_")[0] == "b") {
          fields["Bot"].push(checked.id)
        } else if (checked.id.split("_")[0] == "t") {
          fields["Tweet"].push(checked.id)
        } else {
          fields["User"].push(checked.id)
        }
      })

      search["fields"] = fields

      //////////////////////////////////////////////////

      var start = {}
      var startType = this.state.start.type
      if (startType != null && startType != "") {
        if (startType.value.split("_").length == 2) {
          startType = null
        } else {
          startType = startType.value
        }
      }
      start["type"] = startType

      var startNode = this.state.start.nodes
      if (startNode != null) {
        startNode = startNode.value
        if (startNode != null && startNode.length > 15 && startNode[0] == "a") {
          startNode = null
        }

        start["node"] = startNode
      }

      var startRel = this.state.start.relation
      if (startRel != null && startRel != "") {
        if (startRel.value.split("_").length == 2) {
          startRel = null
        } else {
          startRel = startRel.value
        }
      }

      start["relation"] = startRel

      var startDir = this.state.start.direction
      if (startDir != null && startDir != "") {
        if (startDir.value.split("_").length == 2) {
          startDir = null
        } else {
          startDir = startDir.value
        }
      }

      start["direction"] = startDir

      search["start"] = start

      //////////////////////////////////////////////////

      var end = {}
      var endType = this.state.end.type
      if (endType != null && endType != "") {
        if (endType.value.split("_").length == 2) {
          endType = null
        } else {
          endType = endType.value
        }
      }
      end["type"] = endType

      var endNode = this.state.end.nodes
      if (endNode != null) {
        endNode = endNode.value
        if (endNode != null && endNode.length > 15 && endNode[0] == "a") {
          endNode = null
        }
      }
      end["node"] = endNode

      search["end"] = end

      //////////////////////////////////////////////////

      var intermediate = {}

      var intermediateTypes = []
      if (this.state.intermediate.type != null && this.state.intermediate.type.length > 0) {
        this.state.intermediate.type.forEach(type => {
          var value = type["value"].split("_")[0]
          if (value == "a") {
            value = null
          }

          intermediateTypes.push(value)
        })
      }
      intermediate["types"] = intermediateTypes

      var intermediateRels = []
      if (this.state.intermediate.relation != null && this.state.intermediate.relation.length > 0) {
        this.state.intermediate.relation.forEach(type => {
          var value = type["value"].split("_")[0]
          if (value == "a") {
            value = null
          }

          intermediateRels.push(value)
        })
      }
      intermediate["relations"] = intermediateRels

      var intermediateDir = []
      if (this.state.intermediate.direction != null && this.state.intermediate.direction.length > 0) {
        this.state.intermediate.direction.forEach(type => {
          var value = type["value"].split("_")[0]
          if (value == "a") {
            value = null
          }

          intermediateDir.push(value)
        })
      }
      intermediate["directions"] = intermediateDir

      var intermediateNodes = []
      if (this.state.intermediate.nodes != null && this.state.intermediate.nodes.length > 0) {
        this.state.intermediate.nodes.forEach(type => {
          var value = type["value"]
          if (value != null && value.length > 15 && value[0] == "a") {
            value = null
          }
          intermediateNodes.push(value)
        })
      }
      intermediate["nodes"] = intermediateNodes

      search["intermediate"] = intermediate

      //////////////////////////////////////////////////
      var fileType = this.state.fileType
      search["fileType"] = fileType

      //////////////////////////////////////////////////

      var limit = null
      if (document.getElementById("limit") != null && document.getElementById("limit").value != "" && document.getElementById("limit").value != null) {
        limit = document.getElementById("limit").value
      }

      search["limit"] = limit

      this.startDownload(search, fileType)
    }

  }

  async startDownload(search, fileType) {
    this.setState({
      processing: true
    })

    await fetch(baseURL + "twitter/sub_network", {
      method: "POST",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(search)
    }).then(response => {
      if (response.ok) return response.json();
      else {
        throw new Error(response.status);
      }
    }).then(data => {
      this.setState({
        processing: false,
        redirect: true,
        returnValues: data.data
      })

    }).catch(error => {
      console.log("error: " + error);
      this.setState({
        processing: false,
      })

      toast.error('Sorry, something went wrong on our end. Please try again later!', {
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
    });
  }

  handleOpen() {
    this.setState({
      modal: true,
    })
  }

  handleGoBack() {
    this.setState({
      redirect: true
    })
  }
  /////////////////////////////////////////////////////////////////////

  render() {

    if (this.state.redirect) {
      return (<Network returnValues={this.state.returnValues}></Network>)
    }

    if (!this.state.doneLoading) {
      return (
        <div className="animated fadeOut animated" style={{ width: "100%", marginTop: "10%" }}>
          <FadeIn>
            <Lottie options={this.state.animationOptions} height={"30%"} width={"30%"} />
          </FadeIn>
        </div>
      )
    } else if (this.state.error != null) {
      if (this.state.error == "NOT FOUND") {
        return (
          <Container fluid>
            <Row>
              <Col xs="12" sm="12" md="12">
                <div style={{ width: "100%", alignContent: "center" }}>
                  <img style={{ width: "50%", display: "block", marginLeft: "auto", marginRight: "auto" }} src={require("../../assets/img/error_not_found.png")}></img>
                </div>
              </Col>
            </Row>
          </Container>
        )
      } else {
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
      }
    } else {
      var processing = <div></div>
      if (this.state.processing) {
        processing =
          <div id="loading">
            <div className="animated fadeOut animated" style={{ width: "100%", height: "100%", top: 0, left: 0, position: "fixed", backgroundColor: "white", opacity: 0.8, zIndex: 11 }}>
            </div>
            <div style={{ zIndex: 11, position: "relative" }}>
              <div className="animated fadeOut animated" style={{ width: "100%", top: "25%", left: "5%", position: "fixed", zIndex: 12 }}>
                <FadeIn>
                  <Lottie options={this.state.animationOptions} height={"30%"} width={"30%"} />
                </FadeIn>
              </div>
            </div>
          </div>
      }

      var modal
      if (this.state.modal) {

        modal = <Dialog class="fade-in"
          open={this.state.modal}
          onClose={() => this.handleClose()}
          aria-labelledby="alert-dialog-title"
          aria-describedby="alert-dialog-description"
        >
          <DialogTitle id="alert-dialog-title">
            {"Tutorial"}
            <hr />
          </DialogTitle>
          <DialogContent
          >
            <Container fluid>
              <Col xs="12" md="12">
                <div style={{ textAlign: "left", width: "100%" }}>
                  <h5 style={{ color: "#1da1f2" }}>
                    <i><b>1. Define a Starting Node (Optional)</b></i>
                  </h5>
                  <h6 style={{ marginLeft: "15px" }}>
                    <span>You can start by defining the starting node, its type, what type of relation connects it to other nodes and the direction of said relation.</span>
                  </h6>
                  <h6 style={{ marginLeft: "15px" }}>
                    <span>You can choose to not specify any of these fields: Not specifying the type implies you want any type of node, not specifying the node means you want any node, not specifying the relation means you want any type of relation and not specifying the direction means you want outgoing relations.</span>
                  </h6>
                  <h6 style={{ marginLeft: "15px" }}>
                    <span>If you don't specify any of the fields, or specify only the direction, however, we'll assume you don't want a starting node</span>
                  </h6>
                </div>
              </Col>
              <Col xs="12" md="12">
                <div style={{ textAlign: "left", width: "100%", marginTop: "30px" }}>
                  <h5 style={{ color: "#1da1f2" }}>
                    <i><b>2. Define the Intermediate Nodes (Optional)</b></i>
                  </h5>
                  <h6 style={{ marginLeft: "15px" }}>
                    <span>You can then define intermediate nodes, their types, types of relationships and their respective directions.</span>
                  </h6>
                  <h6 style={{ marginLeft: "15px" }}>
                    <span>Note that for each intermediate node you need to explicitly specify all of its fields (type, node, relationship and direction). Note also that the order of specifications is important, i.e, the first type you specify will correspond to the first node, relation and direction, the second type to the second node, and so on.</span>
                  </h6>
                </div>
              </Col>

              <Col xs="12" md="12">
                <div style={{ textAlign: "left", width: "100%", marginTop: "30px" }}>
                  <h5 style={{ color: "#1da1f2" }}>
                    <i><b>3. Define the End Node (OBLIGATORY)</b></i>
                  </h5>
                  <h6 style={{ marginLeft: "15px" }}>
                    <span>To finish off, you have to specify the node you want to end on.</span>
                  </h6>
                  <h6 style={{ marginLeft: "15px" }}>
                    <span>In case nothing else is specified (in terms of start and intermediate nodes), the system will simply return the nodes that match what you input on this end node section.</span>
                  </h6>
                  <h6 style={{ marginLeft: "15px" }}>
                    <span>In case you don't specify any property of the last node we return all nodes in our databases</span>
                  </h6>
                </div>
              </Col>

              <Col xs="12" md="12">
                <div style={{ textAlign: "left", width: "100%", marginTop: "30px" }}>
                  <h5 style={{ color: "#1da1f2" }}>
                    <i><b>Please note that...</b></i>
                  </h5>
                  <h6 style={{ marginLeft: "15px" }}>
                    <span>Due to the high number of data our system processes, some query generations might take longer than others. We ask that you be patient and reasonable <i class="far fa-heart" style={{ color: "#fd1d1d" }}></i></span>
                  </h6>
                </div>
              </Col>

              <Col xs="12" md="12">
                <div style={{ textAlign: "left", width: "100%", marginTop: "30px" }}>
                  <h5 style={{ color: "#1da1f2" }}>
                    <i><b>Example of usage</b></i>
                  </h5>
                  <h6 style={{ marginLeft: "15px" }}>
                    <span>Imagining you want to get <i>every user who has interacted with user X's tweets</i></span>
                  </h6>
                  <h6 style={{ marginLeft: "15px" }}>
                    <span>1. Set the <b>Start Node Type</b> as "User" (You can leave the other Start Node fields as empty since we assume this means you want any Nodes and Relations starting on a User Node)</span>
                  </h6>
                  <h6 style={{ marginLeft: "15px" }}>
                    <span>2. Set the <b>Intermediate Node Type</b> as "Tweet", <b>Intermediate Node</b> as "Any Node", <b>Intermediate Relation</b> as "Wrote" and <b>Intermediate Relation Direction</b> as "Ingoing"</span>
                  </h6>
                  <h6 style={{ marginLeft: "15px" }}>
                    <span>3. Set the <b>End Node</b> as user X's name (You can leave the End Node Type empty in this case)</span>
                  </h6>
                </div>
              </Col>
            </Container>

          </DialogContent>
          <DialogActions>
            <Button onClick={() => this.handleClose()} color="info">
              Cancel
            </Button>
          </DialogActions>
        </Dialog>
      }
      return (
        <div className="animated fadeIn">
          {processing}
          <Container fluid>
            <ReactTooltip
              place="right"
              effect="solid"
            />
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
              <Col xs="12" sm="12" md="12">
                <Card>
                  <CardHeader color="primary">
                    <h3 style={{ color: "white" }}>
                      <strong>Network Query</strong>
                    </h3>
                    <h5 style={{ color: "white" }}>
                      Generate a new graph for analysis
                    </h5>
                    <Button block outline color="light" style={{
                      width: "150px", marginTop: "15px"
                    }} onClick={() => this.handleOpen()}
                    ><i class="far fa-question-circle"></i> Help</Button>
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
                    <h3 style={{ color: "white" }}>
                      Query Parameters
                    </h3>
                  </CardHeader>
                  <CardBody>
                    <Row style={{ marginTop: "25px" }}>
                      <Col md="12">
                        <h5 style={{ color: "#999" }}>Start Node</h5>
                      </Col>
                    </Row>

                    <Row style={{ marginTop: "5px" }}>
                      <Col md="2">
                        <FormGroup>
                          <Select
                            defaultValue={[]}
                            id="startType" onChange={this.changeSelectedStartType}
                            value={this.state.start.type}
                            options={[{ value: "a_0", label: "All Types" }, { value: "Bot", label: "Bot" }, { value: "User", label: "User" }, { value: "Tweet", label: "Tweet" }]}
                            className="basic-single"
                            classNamePrefix="select"
                            placeholder="Node Type"
                          />
                          <i data-tip="Specify the starting nodes and their type" style={{ color: "#1da1f2", float: "left", marginTop: "10px", marginRight: "5px" }} class="fas fa-info-circle"></i>
                        </FormGroup>
                      </Col>
                      <Col md="10">
                        <FormGroup>

                          <AsyncSelect
                            placeholder="User/Bot Username or Tweet ID"
                            components={makeAnimated()}
                            defaultOptions
                            value={this.state.start.nodes || ''}
                            loadOptions={this.loadOptions}
                            onChange={this.changeSelectedStartNodes}
                            cacheOptions
                          />
                          <i data-tip="Specify the starting node. Leave empty if you don't want a starting node or pick All Nodes if you don't wanna specify what node it is." style={{ color: "#1da1f2", float: "left", marginTop: "10px", marginRight: "5px" }} class="fas fa-info-circle"></i>

                        </FormGroup>
                      </Col>
                    </Row>

                    <Row style={{ marginTop: "25px" }}>
                      <Col md="2">
                        <FormGroup>
                          <Select
                            defaultValue={[]}
                            id="startRelType" onChange={this.changeSelectedStartRelationType}
                            value={this.state.start.relation}
                            options={[{ value: "a_0", label: "All Relations" }, { value: "FOLLOWS", label: "Follows" }, { value: "QUOTED", label: "Quoted" }, { value: "REPLIED", label: "Replied" }, { value: "RETWEETED", label: "Retweeted" }, { value: "WROTE", label: "Wrote" }]}
                            className="basic-single"
                            classNamePrefix="select"
                            placeholder="Relation Type"
                          />
                          <i data-tip="Specify the relation type" style={{ color: "#1da1f2", float: "left", marginTop: "10px", marginRight: "5px" }} class="fas fa-info-circle"></i>
                        </FormGroup>
                      </Col>
                      <Col md="2">
                        <FormGroup>
                          <Select
                            defaultValue={[]}
                            id="startRelType" onChange={this.changeSelectedStartDirectionType}
                            value={this.state.start.direction}
                            options={[{ value: "Outgoing", label: "Outgoing" }, { value: "Ingoing", label: "Ingoing" }, { value: "Bisexual", label: "Any Direction" }]
                            }
                            className="basic-single"
                            classNamePrefix="select"
                            placeholder="Relation Direction"
                          />
                          <i data-tip="Specify the relation's direction. Outgoing means that the relation starts on this node, Ingoing means that the relation ends on this node and Any Direction shows all relations, either leaving or entering this node" style={{ color: "#1da1f2", float: "left", marginTop: "10px", marginRight: "5px" }} class="fas fa-info-circle"></i>
                        </FormGroup>
                      </Col>
                      <Col md="2">
                        <Button outline color="danger" onClick={() => this.clearStart()} style={{

                        }}><i class="fas fa-times"></i> Reset</Button>
                      </Col>
                    </Row>

                    <hr />
                    <Row style={{ marginTop: "25px" }}>
                      <Col md="12">
                        <h5 style={{ color: "#999" }}>Intermediate Node</h5>
                      </Col>
                    </Row>

                    <Row style={{ marginTop: "5px" }}>
                      <Col md="12">
                        <FormGroup>
                          <Select
                            defaultValue={[]}
                            id="interType" onChange={this.changeSelectedIntermediateType}
                            value={this.state.intermediate.type || ''}
                            options={this.state.intermediateTypeOptions}
                            className="basic-single"
                            classNamePrefix="select"
                            placeholder="Node Types"
                            components={makeAnimated()}
                            isMulti
                          />
                          <i data-tip="Specify the intermediate nodes' types. Please mind the order." style={{ color: "#1da1f2", float: "left", marginTop: "10px", marginRight: "5px" }} class="fas fa-info-circle"></i>
                        </FormGroup>
                      </Col>
                    </Row>

                    <Row style={{ marginTop: "25px" }}>
                      <Col md="12">
                        <FormGroup>
                          <AsyncSelect
                            placeholder="User/Bot Username or Tweet ID"
                            components={makeAnimated()}
                            loadOptions={this.loadOptions3}
                            onChange={this.changeIntermediateNodes}
                            isMulti
                            defaultOptions
                          />
                          <i data-tip="Specify the intermediate nodes. Please mind the order." style={{ color: "#1da1f2", float: "left", marginTop: "10px", marginRight: "5px" }} class="fas fa-info-circle"></i>
                        </FormGroup>
                      </Col>
                    </Row>

                    <Row style={{ marginTop: "25px" }}>
                      <Col md="12">
                        <FormGroup>
                          <Select
                            defaultValue={[]}
                            id="startRelType" onChange={this.changeSelectedIntermediateRelation}
                            value={this.state.intermediate.relation || ''}
                            options={this.state.intermediateRelOptions}
                            className="basic-single"
                            classNamePrefix="select"
                            placeholder="Relation Type"
                            isMulti
                          />
                          <i data-tip="Specify the nodes' relation type. Please mind the order" style={{ color: "#1da1f2", float: "left", marginTop: "10px", marginRight: "5px" }} class="fas fa-info-circle"></i>
                        </FormGroup>
                      </Col>
                    </Row>

                    <Row style={{ marginTop: "25px" }}>
                      <Col md="12">
                        <FormGroup>
                          <Select
                            defaultValue={[]}
                            id="startDirType" onChange={this.changeSelectedIntermediateDirection}
                            value={this.state.intermediate.direction || ''}
                            options={this.state.intermediateDirectionOptions}
                            className="basic-single"
                            classNamePrefix="select"
                            placeholder="Relation Direction"
                            isMulti
                          />
                          <i data-tip="Specify the relation's direction. Outgoing means that the relation starts on this node, Ingoing means that the relation ends on this node and Any Direction shows all relations, either leaving or entering this node" style={{ color: "#1da1f2", float: "left", marginTop: "10px", marginRight: "5px" }} class="fas fa-info-circle"></i>
                        </FormGroup>
                      </Col>
                    </Row>

                    <hr />
                    <Row style={{ marginTop: "25px" }}>
                      <Col md="12">
                        <h5 style={{ color: "#999" }}>End Node</h5>
                      </Col>
                    </Row>

                    <Row style={{ marginTop: "5px" }}>
                      <Col md="2">
                        <FormGroup>
                          <Select
                            defaultValue={[]}
                            id="endType" onChange={this.changeSelectedEndType}
                            value={this.state.end.type}
                            options={[{ value: "a_0", label: "All Types" }, { value: "Bot", label: "Bot" }, { value: "User", label: "User" }, { value: "Tweet", label: "Tweet" }]}
                            className="basic-single"
                            classNamePrefix="select"
                            placeholder="Node Type"
                            components={makeAnimated()}
                          />
                          <i data-tip="Specify the ending nodes and their type" style={{ color: "#1da1f2", float: "left", marginTop: "10px", marginRight: "5px" }} class="fas fa-info-circle"></i>
                        </FormGroup>
                      </Col>
                      <Col md="10">
                        <FormGroup>

                          <AsyncSelect
                            placeholder="User/Bot Username or Tweet ID"
                            components={makeAnimated()}
                            loadOptions={this.loadOptions2}
                            onChange={this.changeSelectedEndNodes}
                            defaultOptions
                            value={this.state.end.nodes || ''}
                          />

                        </FormGroup>
                      </Col>
                    </Row>
                    <Row style={{ marginTop: "25px" }}>
                      <Col md="2">
                        <Button outline color="danger" onClick={() => this.clearEnd()} style={{

                        }}><i class="fas fa-times"></i> Reset</Button>
                      </Col>
                    </Row>

                    <Row>
                      <Col sm="12" md="12" xs="12">
                        <span id="errorNothing" style={{ display: "none", color: "#f86c6b", marginTop: "50px" }}>You need to pick the finishing node!</span>
                      </Col>
                    </Row>

                    <hr />

                    <Row style={{ marginTop: "30px" }}>
                      <Col md="12">
                        <h5 style={{ color: "#999" }}>Entity Limit</h5>
                      </Col>
                    </Row>
                    <Row style={{ marginTop: "10px" }}>
                      <Col md="2">
                        <FormGroup>
                          <Input type="text" id="limit" placeholder="Max number of entities" />
                          <i data-tip="Specify the max number of entities to be included. By default all entities resulting from the other parameters get returned" style={{ color: "#1da1f2", float: "left", marginTop: "10px", marginRight: "5px" }} class="fas fa-info-circle"></i>
                        </FormGroup>
                      </Col>
                    </Row>
                    <Row>
                      <Col sm="12" md="12" xs="12">
                        <span id="errorNumber" style={{ display: "none", color: "#f86c6b", marginTop: "50px" }}>The limit must be a number!</span>
                      </Col>
                    </Row>

                    <hr />

                    <Row style={{ marginTop: "35px" }}>
                      <Col sm="12" md="12" xs="12">
                        <span id="errorOops" style={{ visibility: "hidden", color: "#f86c6b" }}>The intermediate node's list must have the same number of elements as the intermediate nodes' and relations' types!</span>
                      </Col>
                    </Row>


                    <Row style={{ marginTop: "10px" }}>
                      <Col sm="12" md="12" xs="12">
                        <Button block outline color="success" onClick={() => this.confirm()} style={{
                          width: "150px", marginTop: "15px", borderWidth: "2px", float: "right"
                        }}>Confirm</Button>
                        <Button block outline color="danger" onClick={() => this.handleGoBack()} style={{
                          width: "150px", marginTop: "15px", borderWidth: "2px", float: "right", marginRight: "15px"
                        }}><i class="fas fa-chevron-left"></i> Go Back</Button>
                      </Col>
                    </Row>
                  </CardBody>
                </Card>
              </Col>
            </Row>

            {modal}
          </Container>
        </div>
      )
    }
  }
}

export default NetworkReport;

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


class Reports extends Component {
  constructor() {
    super();
  }

  state = {
    error: null,
    doneLoading: false,

    animationOptions: {
      loop: true, autoplay: true, animationData: loadingAnim.default, rendererSettings: {
        preserveAspectRatio: "xMidYMid slice"
      }
    },

    start: {
      type: [],
      nodes: [],
      relation: []
    },

    intermediate: {
      type: [],
      nodes: [],
      relation: []
    },

    end: {
      type: [],
      nodes: []
    },

    intermediateRelOptions: [{ value: "FOLLOWS_1", label: "Follows" }, { value: "QUOTED_1", label: "Quoted" }, { value: "REPLIED_1", label: "Replied" }, { value: "WROTE_1", label: "Wrote" }, { value: "FOLLOWS_1", label: "Follows" }, { value: "a_0", label: "Non Specified" }],
    intermediateTypeOptions: [{ value: "Bot_1", label: "Bot" }, { value: "User_1", label: "User" }, { value: "Tweet_1", label: "Tweet" }, { value: "a_0", label: "Non Specified" }]
  };

  async componentDidMount() {
    this.setState({
      doneLoading: true
    })

  }

  // Search ///////////////////////////////////////////////////////////
  loadOptions = async (inputValue, callback) => {
    if (inputValue == "" || inputValue == null) {
      return
    } else {
      if (!inputValue.match("^[A-Za-z0-9 ]+$")) {
        return
      } else {
        var type = this.state.start.type.value
        if (type == null || type == "" || type.split("_").length == 2) {
          type = null
        }
        var requestValues = await this.search(inputValue, type)
        callback(requestValues)
      }
    }
  }

  loadOptions2 = async (inputValue, callback) => {
    if (inputValue == "" || inputValue == null) {
      return
    } else {
      if (!inputValue.match("^[A-Za-z0-9 ]+$")) {
        return
      } else {
        var type = this.state.end.type.value
        if (type == null || type == "" || type.split("_").length == 2) {
          type = null
        }
        var requestValues = await this.search(inputValue, type)
        callback(requestValues)
      }
    }
  }

  loadOptions3 = async (inputValue, callback) => {
    if (inputValue == "" || inputValue == null) {
      return
    } else {
      if (!inputValue.match("^[A-Za-z0-9 ]+$")) {
        return
      } else {
        toast.dismiss(this.firstErrorToast)
        var requestValues = await this.search(inputValue, null)
        callback(requestValues)
      }
    }
  }

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
      this.setState({ start: { type: { value: "a_0", label: "Non Specified" }, nodes: [], relation: this.state.start.relation } });
    }
  }


  changeSelectedStartNodes = (selectedOption) => {
    if (selectedOption != null) {
      this.setState({ start: { type: this.state.start.type, nodes: selectedOption, relation: this.state.start.relation } });
    } else {
      this.setState({ start: { type: this.state.start.type, nodes: [], relation: this.state.start.relation } });
    }
  }

  changeSelectedStartRelationType = (selectedOption) => {
    if (selectedOption != null) {
      this.setState({ start: { type: this.state.start.type, nodes: this.state.start.nodes, relation: selectedOption } });
    } else {
      this.setState({ start: { type: this.state.start.type, nodes: this.state.start.nodes, relation: { value: "FOLLOWS", label: "Follows" } } });
    }
  }

  changeSelectedEndType = (selectedOption) => {
    if (selectedOption != null) {
      this.setState({ end: { type: selectedOption, nodes: this.state.end.nodes } });
    } else {
      this.setState({ end: { type: { value: "a_0", label: "Non Specified" }, nodes: [] } });
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
        this.setState({ intermediate: { type: selectedOption, nodes: this.state.intermediate.nodes, relation: this.state.intermediate.relation }, intermediateTypeOptions: newTypes.sort((a, b) => a.value > b.value) });

      } else {
        this.setState({ intermediate: { type: selectedOption, nodes: this.state.intermediate.nodes, relation: this.state.intermediate.relation } });
      }

    } else {
      this.setState({ intermediate: { type: [], nodes: this.state.intermediate.nodes, relation: this.state.intermediate.relation }, intermediateTypeOptions: [{ value: "Bot_1", label: "Bot" }, { value: "User_1", label: "User" }, { value: "Tweet_1", label: "Tweet" }] });
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
        this.setState({ intermediate: { type: this.state.intermediate.type, nodes: this.state.intermediate.nodes, relation: selectedOption }, intermediateRelOptions: newTypes.sort((a, b) => a.value > b.value) });

      } else {
        this.setState({ intermediate: { type: this.state.intermediate.type, nodes: this.state.intermediate.nodes, relation: selectedOption } });
      }

    } else {
      this.setState({ intermediate: { type: this.state.intermediate.type, nodes: this.state.intermediate.nodes, relation: [] }, intermediateTypeOptions: [{ value: "FOLLOWS_1", label: "Follows" }, { value: "QUOTED_1", label: "Quoted" }, { value: "REPLIED_1", label: "Replied" }, { value: "RETWEETED_1", label: "Retweeted" }, { value: "WROTE_1", label: "Wrote" }] });
    }
  }

  changeIntermediateNodes = (selectedOption) => {
    if (selectedOption != null) {
      this.setState({ intermediate: { type: this.state.intermediate.type, nodes: selectedOption, relation: this.state.intermediate.relation } });
    } else {
      this.setState({ intermediate: { type: this.state.intermediate.type, nodes: [], relation: this.state.intermediate.relation } });
    }
  }

  confirm() {
    var search = {}

    var error = false

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

    if (document.getElementById("limit") != null && document.getElementById("limit").value != "" && !document.getElementById("limit").value.match("^[0-9]+$")) {
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

    if (this.state.intermediate.type != null || this.state.intermediate.nodes != null || this.state.intermediate.relation != null) {
      try {
        if (this.state.intermediate.type.length != this.state.intermediate.nodes.length || this.state.intermediate.type.length != this.state.intermediate.relation.length || this.state.intermediate.nodes.length != this.state.intermediate.relation.length) {
          error = true
          toast.error('You need to specify the same amount of intermediate nodes, node types and relation types!', {
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
        toast.error('You need to specify the same amount of intermediate nodes, node types and relation types!', {
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
      var fields = {"Bots": [], "Tweets": [], "Users": []}
      checkboxes.forEach(checked => {
        if(checked.id.split("_")[0] == "b"){
          fields["Bots"].push(checked.id)
        }else if(checked.id.split("_")[0] == "t"){
          fields["Tweets"].push(checked.id)
        }{
          fields["Users"].push(checked.id)
        }
      })

      search["fields"] = fields

      //////////////////////////////////////////////////

      var start = {}
      var startType = this.state.start.type.value
      if (startType == null || startType == "" || startType.split("_").length == 2) {
        startType = null
      }
      start["type"] = startType

      var startNode = this.state.start.nodes
      if (startNode != null) {
        startNode = startNode.value
      }
      start["node"] = startNode

      search["start"] = start

      //////////////////////////////////////////////////

      var end = {}
      var endType = this.state.end.type.value
      if (endType == null || endType == "" || endType.split("_").length == 2) {
        endType = null
      }
      end["type"] = endType

      var endNode = this.state.end.nodes
      if (endNode != null) {
        endNode = endNode.value
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
            value = ""
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
            value = ""
          }

          intermediateRels.push(value)
        })
      }
      intermediate["relations"] = intermediateRels

      var intermediateNodes = []
      if (this.state.intermediate.nodes != null && this.state.intermediate.nodes.length > 0) {
        this.state.intermediate.nodes.forEach(type => {
          intermediateNodes.push(type.value)
        })
      }
      intermediate["nodes"] = intermediateNodes

      search["intermediate"] = intermediate

      //////////////////////////////////////////////////

      var limit = null
      if (document.getElementById("limit") != null && document.getElementById("limit").value != "" && document.getElementById("limit").value != null){
        limit = document.getElementById("limit").value
      }

      search["limit"] = limit
    }

    console.log(search)
  }

  /////////////////////////////////////////////////////////////////////

  render() {

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
                      <strong>Reports</strong>
                    </h3>
                    <h5 style={{ color: "white" }}>
                      Generate a new report for analysis
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
                    <h3 style={{ color: "white" }}>
                      Report Parameters
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
                            options={[{ value: "Bot", label: "Bot" }, { value: "User", label: "User" }, { value: "Tweet", label: "Tweet" }, { value: "a_0", label: "Non Specified" }]}
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
                            loadOptions={this.loadOptions}
                            onChange={this.changeSelectedStartNodes}
                            cacheOptions
                            defaultOptions
                          />

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
                            options={[{ value: "FOLLOWS", label: "Follows" }, { value: "QUOTED", label: "Quoted" }, { value: "REPLIED", label: "Replied" }, { value: "RETWEETED", label: "Retweeted" }, { value: "WROTE", label: "Wrote" }, { value: "a_0", label: "Non Specified" }]}
                            className="basic-single"
                            classNamePrefix="select"
                            placeholder="Relation Type"
                          />
                          <i data-tip="Specify the relation type" style={{ color: "#1da1f2", float: "left", marginTop: "10px", marginRight: "5px" }} class="fas fa-info-circle"></i>
                        </FormGroup>
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

                    <hr />
                    <Row style={{ marginTop: "25px" }}>
                      <Col md="12">
                        <h5 style={{ color: "#999" }}>End Node *</h5>
                      </Col>
                    </Row>

                    <Row style={{ marginTop: "5px" }}>
                      <Col md="2">
                        <FormGroup>
                          <Select
                            defaultValue={[]}
                            id="endType" onChange={this.changeSelectedEndType}
                            value={this.state.end.type}
                            options={[{ value: "Bot", label: "Bot" }, { value: "User", label: "User" }, { value: "Tweet", label: "Tweet" }, { value: "a_0", label: "Non Specified" }]}
                            className="basic-single"
                            classNamePrefix="select"
                            placeholder="Node Type"
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
                          />

                        </FormGroup>
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
                          <Input type="number" id="limit"  value="" placeholder="Max number of entities"/>
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

                    <Row style={{ marginTop: "30px" }}>
                      <Col md="12">
                        <h5 style={{ color: "#999" }}>User Fields</h5>
                      </Col>
                    </Row>
                    <Row style={{ marginTop: "10px" }}>
                      <Col md="2">
                        <FormGroup check>
                          <Input className="form-check-input" type="checkbox" id="u_name" name="option-check" defaultChecked value="option2" />
                          <Label className="form-check-label" check htmlFor="inline-checkbox2">Name</Label>
                        </FormGroup>
                      </Col>
                      <Col md="2">
                        <FormGroup check>
                          <Input className="form-check-input" type="checkbox" id="u_username" name="option-check" defaultChecked value="option2" />
                          <Label className="form-check-label" check htmlFor="inline-checkbox2">Username</Label>
                        </FormGroup>
                      </Col>
                      <Col md="2">
                        <FormGroup check>
                          <Input className="form-check-input" type="checkbox" id="u_location" name="option-check" defaultChecked value="option2" />
                          <Label className="form-check-label" check htmlFor="inline-checkbox2">Location</Label>
                        </FormGroup>
                      </Col>
                      <Col md="2">
                        <FormGroup check>
                          <Input className="form-check-input" type="checkbox" id="u_description" name="option-check" defaultChecked value="option2" />
                          <Label className="form-check-label" check htmlFor="inline-checkbox2">Description</Label>
                        </FormGroup>
                      </Col>
                      <Col md="2">
                        <FormGroup check>
                          <Input className="form-check-input" type="checkbox" id="u_tweets" name="option-check" defaultChecked value="option2" />
                          <Label className="form-check-label" check htmlFor="inline-checkbox2">Number of Tweets</Label>
                        </FormGroup>
                      </Col>
                      <Col md="2">
                        <FormGroup check>
                          <Input className="form-check-input" type="checkbox" id="u_followers" name="option-check" defaultChecked />
                          <Label className="form-check-label" check htmlFor="inline-checkbox1">Number of Followers</Label>
                        </FormGroup>
                      </Col>
                    </Row>

                    <Row style={{ marginTop: "10px" }}>

                      <Col md="2">
                        <FormGroup check>
                          <Input className="form-check-input" type="checkbox" id="u_following" name="option-check" defaultChecked />
                          <Label className="form-check-label" check htmlFor="inline-checkbox1">Number of Followings</Label>
                        </FormGroup>
                      </Col>

                      <Col md="2">
                        <FormGroup check>
                          <Input className="form-check-input" type="checkbox" id="u_protected" name="option-check" defaultChecked />
                          <Label className="form-check-label" check htmlFor="inline-checkbox1">Is Protected</Label>
                        </FormGroup>
                      </Col>
                    </Row>


                    <Row style={{ marginTop: "30px" }}>
                      <Col md="12">
                        <h5 style={{ color: "#999" }}>Bot Fields</h5>
                      </Col>
                    </Row>
                    <Row style={{ marginTop: "10px" }}>
                      <Col md="2">
                        <FormGroup check>
                          <Input className="form-check-input" type="checkbox" id="b_name" name="option-check" defaultChecked value="option2" />
                          <Label className="form-check-label" check htmlFor="inline-checkbox2">Name</Label>
                        </FormGroup>
                      </Col>
                      <Col md="2">
                        <FormGroup check>
                          <Input className="form-check-input" type="checkbox" id="b_username" name="option-check" defaultChecked value="option2" />
                          <Label className="form-check-label" check htmlFor="inline-checkbox2">Username</Label>
                        </FormGroup>
                      </Col>
                      <Col md="2">
                        <FormGroup check>
                          <Input className="form-check-input" type="checkbox" id="b_location" name="option-check" defaultChecked value="option2" />
                          <Label className="form-check-label" check htmlFor="inline-checkbox2">Location</Label>
                        </FormGroup>
                      </Col>
                      <Col md="2">
                        <FormGroup check>
                          <Input className="form-check-input" type="checkbox" id="b_description" name="option-check" defaultChecked value="option2" />
                          <Label className="form-check-label" check htmlFor="inline-checkbox2">Description</Label>
                        </FormGroup>
                      </Col>
                      <Col md="2">
                        <FormGroup check>
                          <Input className="form-check-input" type="checkbox" id="b_tweets" name="option-check" defaultChecked value="option2" />
                          <Label className="form-check-label" check htmlFor="inline-checkbox2">Number of Tweets</Label>
                        </FormGroup>
                      </Col>
                      <Col md="2">
                        <FormGroup check>
                          <Input className="form-check-input" type="checkbox" id="b_followers" name="option-check" defaultChecked />
                          <Label className="form-check-label" check htmlFor="inline-checkbox1">Number of Followers</Label>
                        </FormGroup>
                      </Col>
                    </Row>

                    <Row style={{ marginTop: "10px" }}>

                      <Col md="2">
                        <FormGroup check>
                          <Input className="form-check-input" type="checkbox" id="b_following" name="option-check" defaultChecked />
                          <Label className="form-check-label" check htmlFor="inline-checkbox1">Number of Followings</Label>
                        </FormGroup>
                      </Col>

                      <Col md="2">
                        <FormGroup check>
                          <Input className="form-check-input" type="checkbox" id="b_protected" name="option-check" defaultChecked />
                          <Label className="form-check-label" check htmlFor="inline-checkbox1">Is Protected</Label>
                        </FormGroup>
                      </Col>
                    </Row>


                    <Row style={{ marginTop: "30px" }}>
                      <Col md="12">
                        <h5 style={{ color: "#999" }}>Tweet Fields</h5>
                      </Col>
                    </Row>
                    <Row style={{ marginTop: "10px" }}>
                      <Col md="2">
                        <FormGroup check>
                          <Input className="form-check-input" type="checkbox" id="t_creation" name="option-check" defaultChecked />
                          <Label className="form-check-label" check htmlFor="inline-checkbox1">Creation Date</Label>
                        </FormGroup>
                      </Col>

                      <Col md="2">
                        <FormGroup check>
                          <Input className="form-check-input" type="checkbox" id="t_text" name="option-check" defaultChecked />
                          <Label className="form-check-label" check htmlFor="inline-checkbox1">Text</Label>
                        </FormGroup>
                      </Col>

                      <Col md="2">
                        <FormGroup check>
                          <Input className="form-check-input" type="checkbox" id="t_lang" name="option-check" defaultChecked />
                          <Label className="form-check-label" check htmlFor="inline-checkbox1">Lang</Label>
                        </FormGroup>
                      </Col>

                      <Col md="2">
                        <FormGroup check>
                          <Input className="form-check-input" type="checkbox" id="t_noRetweets" name="option-check" defaultChecked />
                          <Label className="form-check-label" check htmlFor="inline-checkbox1">Number of Retweets</Label>
                        </FormGroup>
                      </Col>

                      <Col md="2">
                        <FormGroup check>
                          <Input className="form-check-input" type="checkbox" id="t_noLikes" name="option-check" checked />
                          <Label className="form-check-label" check htmlFor="inline-checkbox1">Number of Likes</Label>
                        </FormGroup>
                      </Col>

                      <Col md="2">
                        <FormGroup check>
                          <Input className="form-check-input" type="checkbox" id="t_sensitive" name="option-check" defaultChecked />
                          <Label className="form-check-label" check htmlFor="inline-checkbox1">Is Sensitive Content</Label>
                        </FormGroup>
                      </Col>
                    </Row>

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
                      </Col>
                    </Row>
                  </CardBody>
                </Card>
              </Col>
            </Row>



          </Container>
        </div>
      )
    }
  }
}

export default Reports;

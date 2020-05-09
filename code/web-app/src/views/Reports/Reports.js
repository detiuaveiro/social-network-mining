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

  firstErrorToast = null;

  state = {
    error: null,
    doneLoading: false,

    animationOptions: {
      loop: true, autoplay: true, animationData: loadingAnim.default, rendererSettings: {
        preserveAspectRatio: "xMidYMid slice"
      }
    },

    start: {
      type: { value: "Bot", label: "Bot" },
      nodes: [],
      relation: { value: "FOLLOWS", label: "Follows" }
    },

    intermediate: {
      type: [],
      nodes: [],
      relation: []
    },

    end: {
      type: { value: "Bot", label: "Bot" },
      nodes: []
    },

    intermediateRelOptions: [{ value: "FOLLOWS_1", label: "Follows" }, { value: "QUOTED_1", label: "Quoted" }, { value: "REPLIED_1", label: "Replied" }, { value: "RETWEETED_1", label: "Retweeted" }, { value: "WROTE_1", label: "Wrote" }],
    intermediateTypeOptions: [{ value: "Bot_1", label: "Bot" }, { value: "User_1", label: "User" }, { value: "Tweet_1", label: "Tweet" }]
  };

  async componentDidMount() {
    this.setState({
      doneLoading: true
    })

  }

  // Search ///////////////////////////////////////////////////////////
  loadOptions = async (inputValue, callback) => {
    if (inputValue == "" || inputValue == null) {
      toast.dismiss(this.firstErrorToast)
    } else {
      if (!inputValue.match("^[A-Za-z0-9 ]+$")) {
        this.firstErrorToast = toast.error('Sorry, the search parameter can\'t include characters like @ or #. Please use only letters and numbers', {
          position: "top-center",
          autoClose: false,
        });
      } else {
        toast.dismiss(this.firstErrorToast)
        var requestValues = await this.search(inputValue, this.state.start.type.value)
        callback(requestValues)
      }
    }
  }

  loadOptions2 = async (inputValue, callback) => {
    if (inputValue == "" || inputValue == null) {
      toast.dismiss(this.firstErrorToast)
    } else {
      if (!inputValue.match("^[A-Za-z0-9 ]+$")) {
        this.firstErrorToast = toast.error('Sorry, the search parameter can\'t include characters like @ or #. Please use only letters and numbers', {
          position: "top-center",
          autoClose: false,
        });
      } else {
        toast.dismiss(this.firstErrorToast)
        var requestValues = await this.search(inputValue, this.state.end.type.value)
        callback(requestValues)
      }
    }
  }

  loadOptions3 = async (inputValue, callback) => {
    if (inputValue == "" || inputValue == null) {
      toast.dismiss(this.firstErrorToast)
    } else {
      if (!inputValue.match("^[A-Za-z0-9 ]+$")) {
        this.firstErrorToast = toast.error('Sorry, the search parameter can\'t include characters like @ or #. Please use only letters and numbers', {
          position: "top-center",
          autoClose: false,
        });
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

    } else if (type != "Tweet") {
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
            tempData.push({ "value": user.id, "label": user.name + " (@" + user.screen_name + ")" })
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
            tempData.push({ "value": tweet, "label": "#" + tweet })
          })

        }
      }).catch(error => {
        console.log("error: " + error);
        this.setState({
          error: true,
        })
      });
    }

    return tempData
  }

  // Methods //////////////////////////////////////////////////////////
  changeSelectedStartType = (selectedOption) => {
    if (selectedOption != null) {
      this.setState({ start: { type: selectedOption, nodes: [], relation: this.state.start.relation } });
    } else {
      this.setState({ start: { type: { value: "Bot", label: "Bot" }, nodes: [], relation: this.state.start.relation } });
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
      this.setState({ end: { type: selectedOption, nodes: [] } });
    } else {
      this.setState({ end: { type: { value: "Bot", label: "Bot" }, nodes: [] } });
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

      if (selectedOption.length + 3 > this.state.intermediateTypeOptions.length) {
        var newPush = selectedOption[selectedOption.length - 1]
        var newValue = newPush.value
        var newNumber = parseInt(newValue.split("_")[1]) + 1
        newValue = newValue.split("_")[0] + "_" + newNumber

        var newElement = { value: newValue, label: newValue.split("_")[0] }

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

      if (selectedOption.length + 5 > this.state.intermediateRelOptions.length) {
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
      this.setState({ start: { type: this.state.intermediate.type, nodes: [], relation: this.state.intermediate.relation } });
    }
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
                      <Col md="2">
                        <FormGroup>
                          <Select
                            defaultValue={[]}
                            id="startType" onChange={this.changeSelectedStartType}
                            value={this.state.start.type}
                            options={[{ value: "Bot", label: "Bot" }, { value: "User", label: "User" }, { value: "Tweet", label: "Tweet" }]}
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
                            options={[{ value: "FOLLOWS", label: "Follows" }, { value: "QUOTED", label: "Quoted" }, { value: "REPLIED", label: "Replied" }, { value: "RETWEETED", label: "Retweeted" }, { value: "WROTE", label: "Wrote" }]}
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
                      <Col md="2">
                        <FormGroup>
                          <Select
                            defaultValue={[]}
                            id="endType" onChange={this.changeSelectedEndType}
                            value={this.state.end.type}
                            options={[{ value: "Bot", label: "Bot" }, { value: "User", label: "User" }, { value: "Tweet", label: "Tweet" }]}
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

                    <hr />

                    <Row style={{ marginTop: "30px" }}>
                      <Col sm="12" md="12" xs="12">
                        <span id="errorNew" style={{ visibility: "hidden", color: "#f86c6b" }}>You need to, at least, pick a name, choose the filter type, define at least one tag and assign a bot before proceeding!</span>
                      </Col>
                    </Row>


                    <Row style={{ marginTop: "10px" }}>
                      <Col sm="12" md="12" xs="12">
                        <Button block outline color="success" onClick={() => this.confirmNew()} style={{
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

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
  };

  async componentDidMount() {
    this.setState({
      doneLoading: true
    })

  }

  // Methods //////////////////////////////////////////////////////////


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
                            id="firstType" onChange={this.changeSelectedFilter}
                            value={this.state.filter || ''}
                            options={[{ value: "Bot", label: "Bot" }, { value: "User", label: "User" }, { value: "Tweet", label: "Tweet" }]}
                            className="basic-single"
                            classNamePrefix="select"
                            placeholder="Filter"
                          />
                          <i data-tip="Target specifies the twitter name of users you want the bot to attempt to follow, whilst Keywords define tags that a tweet should be classified as for the bot to have interest in" style={{ color: "#1da1f2", float: "right", marginTop: "10px", marginRight: "5px" }} class="fas fa-info-circle"></i>
                        </FormGroup>
                      </Col>
                      <Col md="10">
                        <FormGroup>
                          <Input type="text" id="name" placeholder="Policy name" required />
                        </FormGroup>
                      </Col>
                    </Row>

                    <Row style={{ marginTop: "30px", minHeight: "48px" }}>
                      <Col md="12">
                        <CreatableSelect
                          isMulti
                          onChange={this.addNewTags}
                          options={[]}
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

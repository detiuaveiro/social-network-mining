import React, { Component, lazy, Suspense } from 'react';

import baseURL from '../../variables/baseURL'
import {
    Container, Row, Col, Button,
    Input, Badge,
    FormGroup, Label
} from 'reactstrap';
import Table from "../../components/Table/Table.js";

import Card from "../../components/Card/Card";
import CardHeader from "../../components/Card/CardHeader";
import CardBody from "../../components/Card/CardBody";
import CardAvatar from "../../components/Card/CardAvatar.js";

import Dialog from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogTitle from "@material-ui/core/DialogTitle";
import DialogContentText from "@material-ui/core/DialogContentText";

import Bots from './Bots';
import BotProfile from './BotProfile';


import 'react-toastify/dist/ReactToastify.css';

import ReactLoading from "react-loading";
import Pagination from '@material-ui/lab/Pagination';

import FadeIn from "react-fade-in";
import Lottie from "react-lottie";

import ToggleButton from '@material-ui/lab/ToggleButton';
import ToggleButtonGroup from '@material-ui/lab/ToggleButtonGroup';

import { ToastContainer, toast, Flip } from 'react-toastify';


import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend, Brush } from 'recharts';

import * as loadingAnim from "../../assets/animations/squares_1.json";

import CardFooter from "../../components/Card/CardFooter";

import Select from 'react-select';




class PolicyForm extends Component {
    constructor() {
        super();
    }

    state = {
        error: null,
        goBack: false,
        doneLoading: false,
        redirectionList: [],

        animationOptions: {
            loop: true, autoplay: true, animationData: loadingAnim.default, rendererSettings: {
                preserveAspectRatio: "xMidYMid slice"
            }
        },

        allPolicies: [],
        selectedPolicy: null
    };

    async getAllPolicies() {
        await fetch(baseURL + "policies", {
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

                data.forEach(policy => {

                    tempPolicies.push({ 'value': policy, 'label': <span><span style={{ color: "#999" }}>({policy.filter})</span> {policy.name}</span> });
                })


                this.setState({
                    allPolicies: tempPolicies,
                })
            }
        }).catch(error => {
            console.log("error: " + error);
            this.setState({
                error: error
            })
        });
    }



    async componentDidMount() {
        await this.setState({ redirectionList: this.props.redirection })

        // Get Policy
        if (this.state.error == null) {
            await this.getAllPolicies()
        }

        this.setState({
            doneLoading: true
        })

    }

    // Methods //////////////////////////////////////////////////////////
    handleGoBack() {
        this.setState({
            goBack: true,
        })
    }


    /////////////////////////////////////////////////////////////////////


    // Policy //////////////////////////////////////////////////////////
    changeSelectedPolicy = (selectedOption) => {
        if (selectedOption != null) {
            this.setState({ selectedPolicy: selectedOption });
        } else {
            this.setState({ selectedPolicy: null });
        }
    }
    /////////////////////////////////////////////////////////////////////


    render() {
        if (this.state.goBack) {
            if (this.state.redirectionList[this.state.redirectionList.length - 1]['type'] == "LIST")
                return (<Bots />)
            else {
                var lastBot = this.state.redirectionList.pop()
                return (<BotProfile bot={lastBot['info']} redirection={this.state.redirectionList}></BotProfile>)
            }
        } else {
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
                                <Col xs="12" sm="12" md="12" style={{ marginBottom: "30px" }}>
                                    <Button block outline color="danger" onClick={() => this.handleGoBack()} style={{
                                        width: "150px", marginTop: "15px", borderWidth: "2px"
                                    }}><i class="fas fa-chevron-left"></i> Go Back</Button>
                                </Col>
                            </Row>
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
                                <Col xs="12" sm="12" md="12" style={{ marginBottom: "30px" }}>
                                    <Button block outline color="danger" onClick={() => this.handleGoBack()} style={{
                                        width: "150px", marginTop: "15px", borderWidth: "2px"
                                    }}><i class="fas fa-chevron-left"></i> Go Back</Button>
                                </Col>
                            </Row>
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
                return (
                    <div className="animated fadeIn">
                        <Container fluid>
                            <Row>
                                <Col xs="12" sm="12" md="12">
                                    <Card>
                                        <CardHeader color="primary">
                                            <h3 style={{ color: "white" }}>
                                                <strong>Add new Policy to bot {this.props.bot.name}</strong> (@{this.props.bot.screen_name})
                                            </h3>
                                            <h5 style={{ color: "white" }}>
                                                Create or pick a new policy to train the bot with
                                            </h5>
                                        </CardHeader>
                                        <CardBody>
                                            <Button block outline color="danger" onClick={() => this.handleGoBack()} style={{
                                                width: "150px", marginTop: "15px", borderWidth: "2px"
                                            }}><i class="fas fa-chevron-left"></i> Go Back</Button>
                                        </CardBody>
                                    </Card>
                                </Col>
                            </Row>

                            <Row>
                                <Col xs="12" sm="12" md="6">
                                    <Card>
                                        <CardHeader color="primary">
                                            <h3 style={{ color: "white" }}>
                                                New Policy
                                            </h3>
                                        </CardHeader>
                                        <CardBody>
                                            <Button block outline color="danger" onClick={() => this.handleGoBack()} style={{
                                                width: "150px", marginTop: "15px", borderWidth: "2px"
                                            }}><i class="fas fa-chevron-left"></i> Go Back</Button>
                                        </CardBody>
                                    </Card>
                                </Col>

                                <Col xs="12" sm="12" md="6">
                                    <Card>
                                        <CardHeader color="primary">
                                            <h3 style={{ color: "white" }}>
                                                Existing Policy
                                            </h3>
                                        </CardHeader>
                                        <CardBody>
                                            <Row>
                                                <Col sm="12" md="12" xs="12">
                                                    <Select
                                                        defaultValue={[]}
                                                        id="selectOption" onChange={this.changeSelectedPolicy}
                                                        value={this.state.selectedPolicy || ''}
                                                        options={this.state.allPolicies}
                                                        className="basic-single"
                                                        classNamePrefix="select"
                                                    />
                                                </Col>
                                            </Row>

                                            <div class="row">
                                                <div class="col-md-6" style={{backgroundColor:"black"}}>
                                                    <Button block outline color="danger" onClick={() => this.handleGoBack()} style={{
                                                        width: "150px", marginTop: "15px", borderWidth: "2px"
                                                    }}><i class="fas fa-chevron-left"></i> Go Back</Button>
                                                </div>
                                                <div class="col-md-6">
                                                    <Button block outline color="success" onClick={() => this.handleGoBack()} style={{
                                                        width: "150px", marginTop: "15px", borderWidth: "2px"
                                                    }}>Confirm</Button>
                                                </div>
                                            </div>
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
}

export default PolicyForm;

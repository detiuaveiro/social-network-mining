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

import Bots from './Bots';
import BotProfile from './BotProfile';


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
        selectedPolicy: null,

        filter: null,
        tags: [],

        success: false
    };

    async getAllPolicies() {
        await fetch(baseURL + "policies/", {
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
                    var containsBot = false
                    for (var i = 0; i < policy.bots.length; i++) {
                        if (policy.bots[i].bot_id == this.props.bot.user_id) {
                            containsBot = true
                            break
                        }
                    }

                    if (!containsBot) {
                        tempPolicies.push({ 'value': policy, 'label': "(" + policy.filter + ") " + policy.name });
                    }
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
            document.getElementById("existingTags").style.visibility = ""

            console.log(selectedOption.value.tags)
            var tags = ""
            selectedOption.value.tags.forEach(tag => {
                tags += tag
                tags += ", "
            })

            tags = tags.substr(0, tags.length - 2)

            document.getElementById("existingTags2").textContent = tags
            document.getElementById("existingTags2").style.visibility = ""

        } else {
            this.setState({ selectedPolicy: null });
            document.getElementById("existingTags").style.visibility = "hidden"
            document.getElementById("existingTags2").style.visibility = "hidden"
        }
    }

    changeSelectedFilter = (selectedOption) => {
        if (selectedOption != null) {
            this.setState({ filter: selectedOption });

        } else {
            this.setState({ filter: null });
        }
    }

    addNewTags = (newValue, actionMeta) => {
        var tags = []
        if (newValue != null && newValue.length > 0) {
            newValue.forEach(tag => {
                tags.push(tag['value'])
            })
        }

        this.setState({
            tags: tags
        })
    };
    /////////////////////////////////////////////////////////////////////

    // Confirm //////////////////////////////////////////////////////////
    async confirmNew() {
        if (this.state.tags == null || this.state.tags.length <= 0 || document.getElementById("name") == null || document.getElementById("name").value == null || document.getElementById("name").value == "" || this.state.filter == null || this.state.filter == "") {
            document.getElementById("errorNew").style.visibility = ""
        } else {
            document.getElementById("errorNew").style.visibility = "hidden"

            await this.setState({
                processing: true
            })

            await fetch(baseURL + "policies/add", {
                method: "POST",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    API_type: "Twitter",
                    filter: this.state.filter.value,
                    name: document.getElementById("name").value,
                    tags: this.state.tags,
                    bots: [this.props.bot.user_id]
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
                this.setState({
                    processing: false
                })

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
                    this.setState({
                        success: true,
                        goBack: true
                    })
                }

            }).catch(error => {
                console.log("error: " + error);
                this.setState({
                    processing: false,
                    error: true,
                })
            });
        }
    }

    async confirmExisting() {

        if (this.state.selectedPolicy == null || this.state.selectedPolicy == "") {
            document.getElementById("errorExisting").style.visibility = ""
        } else {
            document.getElementById("errorExisting").style.visibility = "hidden"

            var bots = []
            for (var i = 0; i < this.state.selectedPolicy.value.bots.length; i++) {
                bots.push(this.state.selectedPolicy.value.bots[i].bot_id)
            }
            
            bots.push(this.props.bot.user_id)

            await this.setState({
                processing: true
            })

            await fetch(baseURL + "policies/update/" + this.state.selectedPolicy.value.id + "/", {
                method: "PUT",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    bots: bots
                })
            }).then(response => {
                if (response.ok) return response.json();
                else {
                    throw new Error(response.status);
                }
            }).then(data => {
                this.setState({
                    processing: false
                })


                this.setState({
                    success: true,
                    goBack: true
                })

            }).catch(error => {
                console.log("error: " + error);
                this.setState({
                    processing: false,
                    error: true,
                })
            });
        }
    }
    /////////////////////////////////////////////////////////////////////


    render() {
        if (this.state.goBack) {
            if (this.state.redirectionList[this.state.redirectionList.length - 1]['type'] == "LIST")
                return (<Bots />)
            else {
                var lastBot = this.state.redirectionList.pop()
                return (<BotProfile user={lastBot['info']} redirection={this.state.redirectionList} success={this.state.success}></BotProfile>)
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
                                                <strong>Add new Policy to bot {this.props.bot.name}</strong> (@{this.props.bot.screen_name})
                                            </h3>
                                            <h5 style={{ color: "white" }}>
                                                Create a new policy or pick from a list of existing ones to train the bot with
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
                                            <Row style={{ marginTop: "25px" }}>
                                                <Col md="8">
                                                    <FormGroup>
                                                        <Input type="text" id="name" placeholder="Policy name" required />
                                                    </FormGroup>
                                                </Col>
                                                <Col md="4">
                                                    <FormGroup>
                                                        <Select
                                                            defaultValue={[]}
                                                            id="filter" onChange={this.changeSelectedFilter}
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
                                                        onChange={this.addNewTags}
                                                        options={[]}
                                                        components={makeAnimated()}
                                                        placeholder="Tags"
                                                    />
                                                </Col>
                                            </Row>

                                            <Row style={{ marginTop: "30px" }}>
                                                <Col sm="12" md="12" xs="12">
                                                    <span id="errorNew" style={{ visibility: "hidden", color: "#f86c6b" }}>You need to fill all fields and define at least one tag!</span>
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

                                <Col xs="12" sm="12" md="6">
                                    <Card>
                                        <CardHeader color="primary">
                                            <h3 style={{ color: "white" }}>
                                                Existing Policy
                                            </h3>
                                        </CardHeader>
                                        <CardBody>
                                            <Row style={{ marginTop: "25px" }}>
                                                <Col sm="12" md="12" xs="12">
                                                    <Select
                                                        defaultValue={[]}
                                                        id="findNode"
                                                        onChange={this.changeSelectedPolicy}
                                                        value={this.state.selectedPolicy || ''}
                                                        options={this.state.allPolicies}
                                                        className="basic-single"
                                                        classNamePrefix="select"
                                                        placeholder="Select from a list of existing policies"
                                                    />
                                                </Col>
                                            </Row>

                                            <Row style={{ marginTop: "30px", minHeight: "77px" }}>
                                                <Col sm="12" md="12" xs="12">
                                                    <p style={{ fontSize: "17px", color: "#999", visibility: "hidden" }} id="existingTags">Tags: <br />
                                                        <span style={{ fontSize: "15px", visibility: "hidden", marginLeft: "10px", color: "#657786" }} id="existingTags2"></span>
                                                    </p>
                                                </Col>
                                            </Row>

                                            <Row style={{ marginTop: "30px" }}>
                                                <Col sm="12" md="12" xs="12">
                                                    <span id="errorExisting" style={{ visibility: "hidden", color: "#f86c6b" }}>You need to pick from the list of existing policies!</span>
                                                </Col>
                                            </Row>

                                            <Row style={{ marginTop: "10px" }}>
                                                <Col sm="12" md="12" xs="12">
                                                    <Button block outline color="success" onClick={() => this.confirmExisting()} style={{
                                                        width: "150px", marginTop: "10px", borderWidth: "2px", float: "right"
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
}

export default PolicyForm;

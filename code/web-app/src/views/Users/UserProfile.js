import React, { Component, lazy, Suspense } from 'react';
import { Bar, Line } from 'react-chartjs-2';

import baseURL from '../../variables/baseURL'
import {
    Container, Row, Col, Button,
    Input, Badge,
    FormGroup,
} from 'reactstrap';
import Table from "../../components/Table/Table.js";

import Card from "../../components/Card/Card";
import CardHeader from "../../components/Card/CardHeader";
import CardBody from "../../components/Card/CardBody";
import CardFooter from "../../components/Card/CardFooter";
import CardIcon from "../../components/Card/CardIcon";
import CardAvatar from "../../components/Card/CardAvatar.js";

import Dialog from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogTitle from "@material-ui/core/DialogTitle";

import Users from './Users';

import { CustomTooltips } from '@coreui/coreui-plugin-chartjs-custom-tooltips';

import { ToastContainer, toast, Flip } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import ReactLoading from "react-loading";
import Pagination from '@material-ui/lab/Pagination';


class UserProfile extends Component {
    constructor() {
        super();
    }

    state = {
        error: false,
        goBack: false,

        tweets: {
            data: [],
            noPage: 1,
            curPage: 1,
            latestTweet: null,
            tweet: null
        }

    };

    getTweets(page, first) {
        fetch(baseURL + "twitter/users/" + this.props.user.user_id + "/tweets/5/" + page + "/", {
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

                var tempTweets = []

                data.entries.forEach(tweet => {
                    var tempInfo = []
                    tempInfo.push("#" + tweet.tweet_id);

                    if (tweet.is_quote_status) {
                        tempInfo.push(<Badge pill color="warning" style={{ fontSize: "11px" }}>Quote</Badge>);
                        tempInfo.push(<span style={{ color: "#999" }}><i class="fas fa-minus"></i></span>);

                    } else if (tweet.in_reply_to_screen_name == null) {
                        tempInfo.push(<Badge pill color="info" style={{ fontSize: "11px" }}>Tweet</Badge>);
                        tempInfo.push(<span style={{ color: "#999" }}><i class="fas fa-minus"></i></span>);

                    } else {
                        tempInfo.push(<Badge pill color="success" style={{ fontSize: "11px" }}>Reply</Badge>);
                        tempInfo.push("@" + tweet.in_reply_to_screen_name);
                    }

                    var splitData = tweet.created_at.split(" ")
                    var str = splitData[0] + " " + splitData[1] + " " + splitData[2] + " " + splitData[3] + " " + splitData[5]

                    tempInfo.push(str);

                    tempInfo.push(
                        <Button block outline color="primary"
                            onClick={() => this.handleOpenTweet(tweet)}
                        >
                            <i class="fas fa-plus"></i>
                            <strong style={{ marginLeft: "3px" }}>More</strong>
                        </Button>
                    )

                    tempTweets.push(tempInfo);
                })

                if (first) {
                    this.setState({
                        error: false,
                        tweets: {
                            data: tempTweets,
                            noPage: data.num_pages,
                            curPage: page,
                            latestTweet: data.entries[0],
                            tweet: null
                        }
                    })
                } else {
                    this.setState({
                        error: false,
                        tweets: {
                            data: tempTweets,
                            noPage: data.num_pages,
                            curPage: page,
                            latestTweet: this.state.tweets.latestTweet,
                            tweet: null
                        }
                    })
                }

            }
        }).catch(error => {
            console.log("error: " + error);
            this.setState({
                error: true,
            })
        });
    }

    componentDidMount() {
        this.setState({
            error: this.state.error,
            goBack: this.state.goBack,
        })
        document.getElementById("loadedTweets").style.visibility = "hidden"
        document.getElementById("loadingTweets").style.display = ""

        // Get Tweets

        this.getTweets(1, true)

        document.getElementById("loadedTweets").style.visibility = ""
        document.getElementById("loadingTweets").style.display = "none"


        // Get Policies

        this.setState({
            error: this.state.error,
            goBack: this.state.goBack,
        })

    }


    // Methods //////////////////////////////////////////////////////////

    handleOpenTweet() {
        this.setState({
            modal: true,
            modalType: "TWEET",
        });
    }

    handleClose() {
        this.setState({
            modal: false,
            modalType: null,
        });
    }

    handleGoBack() {
        console.log("back")
        this.setState({
            goBack: true,
        })
    }

    /////////////////////////////////////////////////////////////////////

    // Pagination //////////////////////////////////////////////////////////
    changePageTweets = (event, value) => {
        document.getElementById("loadedTweets").style.visibility = "hidden"
        document.getElementById("loadingTweets").style.display = ""

        this.getTweets(value, false)

        document.getElementById("loadedTweets").style.visibility = ""
        document.getElementById("loadingTweets").style.display = "none"
    };
    /////////////////////////////////////////////////////////////////////


    loading = () => <div className="fadeIn pt-1 text-center"><ReactLoading type={"cubes"} color="#1da1f2" /></div>

    render() {
        if (this.state.goBack) {
            return (<Users />)
        } else {

            var modal
            if (this.state.modal) {
                if (this.state.modalType == "TWEET") {
                    modal = <Dialog class="fade-in"
                        open={this.state.modal}
                        onClose={() => this.handleClose()}
                        aria-labelledby="alert-dialog-title"
                        aria-describedby="alert-dialog-description"
                    >
                        <DialogTitle id="alert-dialog-title">
                            {"🐦 Tweet #"}
                        </DialogTitle>
                        <DialogContent style={{ minWidth: "600px" }}>
                            <Container fluid>
                                <Row>
                                    <Col xs="12" md="12">

                                    </Col>
                                </Row>
                            </Container>

                        </DialogContent>
                        <DialogActions>
                            <Button onClick={() => this.handleClose()} color="info">
                                Cancel
                            </Button>
                        </DialogActions>
                    </Dialog>
                }
            }

            var locale = <h5></h5>
            if (this.props.user.location != "") {
                locale = <h5 style={{ marginTop: "15px" }}>
                    <span style={{ color: "#999", fontSize: "15px" }}><i>from</i> </span>{this.props.user.location}
                </h5>

            }

            var latestTweet = <CardBody></CardBody>

            if (this.state.tweets.latestTweet != null) {
                latestTweet = <CardBody>
                    <h5 style={{ marginTop: "15px" }}>
                        <i>{this.state.tweets.latestTweet.text}</i>
                    </h5>
                    <div class="row" style={{ marginTop: "20px", textAlign: "center" }}>
                        <div class="col-sm-12 offset-md-3 col-md-3">
                            <h6><b>{this.state.tweets.latestTweet.retweet_count}</b> <br /><i style={{color:"#1da1f2"}} class="fas fa-retweet"></i> retweets</h6>
                        </div>

                        <div class="col-sm-12 col-md-3">
                            <h6><b>{this.state.tweets.latestTweet.favorite_count}</b> <br /><i style={{color:"#1da1f2"}} class="far fa-heart"></i> likes</h6>
                        </div>
                    </div>
                </CardBody>
            }

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
                            <Col xs="12" sm="12" md="12" style={{ marginBottom: "30px" }}>
                                <Button block outline color="danger" onClick={() => this.handleGoBack()} style={{
                                    width: "150px", marginTop: "15px"
                                }}><i class="fas fa-chevron-left"></i> Go Back</Button>
                            </Col>
                        </Row>
                        <Row>
                            <Col xs="12" sm="12" md="4">
                                <Card profile>
                                    <CardAvatar profile>
                                        <a onClick={e => e.preventDefault()}>
                                            <img src={this.props.user.profile_image_url_https.replace("normal", "400x400")} alt="Profile Image" style={{ minWidth: "100px" }} />
                                        </a>
                                    </CardAvatar>
                                    <CardBody profile>
                                        <h6 style={{
                                            color: "#999",
                                            margin: "0",
                                            fontSize: "14px",
                                            marginTop: "0",
                                            paddingTop: "10px",
                                            marginBottom: "0"
                                        }}>@{this.props.user.screen_name}</h6>
                                        <h4 style={{
                                            color: "#3C4858",
                                            marginTop: "0px",
                                            minHeight: "auto",
                                            fontWeight: "550",
                                            marginBottom: "3px",
                                            textDecoration: "none",
                                            "& small": {
                                                color: "#999",
                                                fontWeight: "400",
                                                lineHeight: "1"
                                            }
                                        }}>{this.props.user.name}</h4>
                                        <h5 style={{ marginTop: "15px" }}>
                                            <i>{this.props.user.description}</i>
                                        </h5>

                                        {locale}

                                        <div class="row" style={{ marginTop: "20px" }}>
                                            <div class="col-sm-12 offset-md-3 col-md-3">
                                                <h6><b>{this.props.user.followers_count}</b> <br />following</h6>
                                            </div>

                                            <div class="col-sm-12 col-md-3">
                                                <h6><b>{this.props.user.friends_count}</b> <br />followers</h6>
                                            </div>
                                        </div>
                                    </CardBody>
                                </Card>

                            </Col>
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
                                        }} > Stats</h4>
                                    </CardHeader>
                                    <CardBody style={{ paddingTop: "0px" }}>

                                    </CardBody>
                                </Card>
                            </Col>
                        </Row>

                        <Row>
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
                                        }} > Last tweet</h4>
                                    </CardHeader>
                                    {latestTweet}
                                </Card>

                            </Col>
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
                                        }} > Tweets</h4>
                                    </CardHeader>
                                    <CardBody>
                                        <div style={{ position: "relative" }}>
                                            <div
                                                id="loadedTweets"
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
                                                    tableHead={["Id", "Type", "Replying to", "Date", ""]}
                                                    tableData={this.state.tweets.data}
                                                />

                                            </div>
                                            <div
                                                id="loadingTweets"
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
                                                <Pagination count={this.state.tweets.noPage} page={this.state.tweets.curPage} onChange={this.changePageTweets} variant="outlined" color="primary" showFirstButton showLastButton shape="rounded" />
                                            </div>
                                        </div>
                                    </CardBody>
                                </Card>
                            </Col>
                        </Row>

                        <Row>
                            <Col xs="12" sm="12" md="6">
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
                                        }} > Followers</h4>
                                    </CardHeader>
                                    <CardBody>

                                    </CardBody>
                                </Card>
                            </Col>

                            <Col xs="12" sm="12" md="6">
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
                                        }} > Following</h4>
                                    </CardHeader>
                                    <CardBody>

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

export default UserProfile;

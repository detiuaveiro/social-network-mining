import React, { Component, lazy, Suspense } from 'react';

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
import CardAvatar from "../../components/Card/CardAvatar.js";

import Dialog from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogTitle from "@material-ui/core/DialogTitle";

import Users from './Users';

import { ToastContainer, toast, Flip } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import ReactLoading from "react-loading";
import Pagination from '@material-ui/lab/Pagination';

import FadeIn from "react-fade-in";
import Lottie from "react-lottie";

import * as loadingAnim from "../../assets/animations/squares_1.json";


class UserProfileRedirected extends Component {
    constructor() {
        super();
        var userInfo = null
    }

    state = {
        error: false,
        goBack: false,
        doneLoading: false,

        animationOptions: {
            loop: true, autoplay: true, animationData: loadingAnim.default, rendererSettings: {
                preserveAspectRatio: "xMidYMid slice"
            }
        },

        tweets: {
            data: [],
            noPage: 1,
            curPage: 1,
            latestTweet: null,
            tweet: null,
            empty: false
        },

        nextUser: null

    };

    


    getTweets(page, first) {
        fetch(baseURL + "twitter/users/" + this.userInfo.user_id + "/tweets/5/" + page + "/", {
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
                        tempInfo.push(<span style={{ color: "#1b95e0", cursor: "pointer" }}>#{tweet.quoted_status_id}</span>);

                    } else if (tweet.in_reply_to_screen_name == null) {
                        tempInfo.push(<Badge pill color="info" style={{ fontSize: "11px" }}>Tweet</Badge>);
                        tempInfo.push(<span style={{ color: "#999" }}><i class="fas fa-minus"></i></span>);
                    } else {
                        tempInfo.push(<Badge pill color="success" style={{ fontSize: "11px" }}>Reply</Badge>);
                        tempInfo.push(<span style={{ color: "#1b95e0", cursor: "pointer" }} onClick={() => this.handleOpenProfile(tweet.in_reply_to_user_id)}>@{tweet.in_reply_to_screen_name}</span>);
                    }

                    var splitData = tweet.created_at.split(" ")
                    tweet.created_at = splitData[3] + " · " + splitData[1] + " " + splitData[2] + ", " + splitData[5] + " (" + splitData[0] + ")"

                    tempInfo.push(tweet.created_at);

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

                var empty = false
                if (tempTweets.length == 0) {
                    empty = true
                }

                if (first) {
                    this.setState({
                        error: false,
                        tweets: {
                            data: tempTweets,
                            noPage: data.num_pages,
                            curPage: page,
                            latestTweet: data.entries[0],
                            tweet: null,
                            empty: empty
                        }
                    }, () => {
                        this.setState({
                            doneLoading: true
                        })
                    })
                } else {
                    this.setState({
                        error: false,
                        tweets: {
                            data: tempTweets,
                            noPage: data.num_pages,
                            curPage: page,
                            latestTweet: this.state.tweets.latestTweet,
                            tweet: null,
                            empty: empty
                        }
                    }, () => {
                        document.getElementById("loadedTweets").style.visibility = ""
                        document.getElementById("loadingTweets").style.display = "none"
                    })
                }

            }
        }).catch(error => {
            console.log("error: " + error);
            this.setState({
                error: true,
                doneLoading: true
            })
        });
    }

    getUserInfo() {
        fetch(baseURL + "twitter/users/" + this.props.user + "/", {
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

                this.userInfo = data
                console.log(this.userInfo)

            }
        }).catch(error => {
            console.log("error: " + error);
            this.setState({
                error: true,
                doneLoading: true
            })
        });
    }

    async componentDidMount() {
        await this.getUserInfo()

        // Get Tweets

        this.getTweets(1, true)

        // Get Policies

        this.setState({
            goBack: this.state.goBack,
        })

    }

    handleOpenProfile(user) {
        this.setState({
          nextUser: user
        })
      }


    // Methods //////////////////////////////////////////////////////////

    handleOpenTweet(tweet) {
        console.log(tweet)

        this.setState({
            modal: true,
            modalType: "TWEET",
            tweets: {
                data: this.state.tweets.data,
                noPage: this.state.tweets.noPage,
                curPage: this.state.tweets.curPage,
                latestTweet: this.state.tweets.latestTweet,
                tweet: tweet
            }
        });
    }

    handleClose() {
        this.setState({
            modal: false,
            modalType: null,
            tweets: {
                data: this.state.tweets.data,
                noPage: this.state.tweets.noPage,
                curPage: this.state.tweets.curPage,
                latestTweet: this.state.tweets.latestTweet,
                tweet: null
            }
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
    };
    /////////////////////////////////////////////////////////////////////


    render() {
        if (this.state.goBack) {
            return (<Users />)
        } else {
            if (!this.state.doneLoading) {
                return (
                    <div className="animated fadeIn">
                        <div style={{ width: "100%", marginTop: "10%" }}>
                            <FadeIn>
                                <Lottie options={this.state.animationOptions} height={"30%"} width={"30%"} />
                            </FadeIn>
                        </div>
                    </div>
                )
            } else if (this.state.error) {
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
                                <Card>
                                    <CardHeader color="danger">
                                        <h3 style={{ color: "white" }}>
                                            Oh no! An error :(
                                        </h3>
                                    </CardHeader>
                                    <CardBody>
                                        <h4 style={{ marginTop: "10px" }}>
                                            Sorry, there was an error retrieving information on <strong>{this.userInfo.name}</strong> <span style={{ color: "#999" }}>(@{this.userInfo.screen_name})</span>.
                                        </h4>
                                        <h5>
                                            We're very sorry for any inconvenience this may have caused and ask that you refresh the page in a few minutes.
                                        </h5>
                                    </CardBody>
                                </Card>
                            </Col>
                        </Row>
                    </Container>
                )
            } else {
                var modal
                if (this.state.modal) {
                    if (this.state.modalType == "TWEET") {
                        var extraInfo
                        if (this.state.tweets.tweet.is_quote_status) {
                            extraInfo = <h6 style={{ color: "#999" }}>
                                Retweeted <span style={{ color: "#1b95e0", cursor: "pointer" }}>#{this.state.tweets.tweet.quoted_status_id}</span>
                            </h6>
                        } else if (this.state.tweets.tweet.in_reply_to_screen_name != null) {
                            extraInfo = <h6 style={{ color: "#999" }}>
                                Replying to <span style={{ color: "#1b95e0", cursor: "pointer" }}>@{this.state.tweets.tweet.in_reply_to_screen_name}</span>
                            </h6>
                        }

                        modal = <Dialog class="fade-in"
                            open={this.state.modal}
                            onClose={() => this.handleClose()}
                            aria-labelledby="alert-dialog-title"
                            aria-describedby="alert-dialog-description"
                        >
                            <DialogTitle id="alert-dialog-title">
                                {"🐦 Tweet "} <span style={{ color: "#999" }}>{"#" + this.state.tweets.tweet.tweet_id}</span>
                                <hr />
                            </DialogTitle>
                            <DialogContent>
                                <Container fluid>
                                    <Row>
                                        <Col xs="12" md="12">
                                            {extraInfo}
                                            <h4>
                                                <i>{this.state.tweets.tweet.text}</i>
                                            </h4>
                                            <h6 style={{ color: "#999" }}>
                                                {this.state.tweets.tweet.created_at}
                                            </h6>
                                            <div class="row" style={{ marginTop: "40px", textAlign: "center" }}>
                                                <div class="col-sm-12 offset-md-3 col-md-3">
                                                    <h6><b>{this.state.tweets.tweet.retweet_count}</b> <br /><i style={{ color: "#1da1f2" }} class="fas fa-retweet"></i> retweets</h6>
                                                </div>

                                                <div class="col-sm-12 col-md-3">
                                                    <h6><b>{this.state.tweets.tweet.favorite_count}</b> <br /><i style={{ color: "#1da1f2" }} class="far fa-heart"></i> likes</h6>
                                                </div>
                                            </div>
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

                //Latest Tweet

                var locale = <h5></h5>
                if (this.userInfo.location != "") {
                    locale = <h5 style={{ marginTop: "15px" }}>
                        <span style={{ color: "#999", fontSize: "15px" }}><i>from</i> </span>{this.userInfo.location}
                    </h5>

                }

                var latestTweet = <CardBody></CardBody>

                if (this.state.tweets.latestTweet != null) {
                    var extraInfo
                    if (this.state.tweets.latestTweet.is_quote_status) {
                        extraInfo = <h6 style={{ color: "#999" }}>
                            Retweeted <span style={{ color: "#1b95e0", cursor: "pointer" }}>#{this.state.tweets.latestTweet.quoted_status_id}</span>
                        </h6>
                    } else if (this.state.tweets.latestTweet.in_reply_to_screen_name != null) {
                        extraInfo = <h6 style={{ color: "#999" }}>
                            Replying to <span style={{ color: "#1b95e0", cursor: "pointer" }}>@{this.state.tweets.latestTweet.in_reply_to_screen_name}</span>
                        </h6>
                    }

                    latestTweet = <CardBody>
                        <div style={{ marginTop: "25px" }}>
                            {extraInfo}
                            <h4>
                                <i>{this.state.tweets.latestTweet.text}</i>
                            </h4>
                            <h6 style={{ color: "#999" }}>
                                {this.state.tweets.latestTweet.created_at}
                            </h6>
                            <div class="row" style={{ marginTop: "40px", textAlign: "center" }}>
                                <div class="col-sm-12 offset-md-3 col-md-3">
                                    <h6><b>{this.state.tweets.latestTweet.retweet_count}</b> <br /><i style={{ color: "#1da1f2" }} class="fas fa-retweet"></i> retweets</h6>
                                </div>

                                <div class="col-sm-12 col-md-3">
                                    <h6><b>{this.state.tweets.latestTweet.favorite_count}</b> <br /><i style={{ color: "#1da1f2" }} class="far fa-heart"></i> likes</h6>
                                </div>
                            </div>
                        </div>
                    </CardBody>
                } else {
                    latestTweet = <CardBody>
                        <div style={{ marginTop: "25px" }}>
                            <h5 style={{ color: "#999" }}>
                                We weren't able to find any tweets made by this user yet
                            </h5>
                        </div>
                    </CardBody>
                }

                var tweets = <CardBody></CardBody>
                if (this.state.tweets.empty) {
                    tweets =
                        <CardBody>
                            <div style={{ marginTop: "25px" }}>
                                <h5 style={{ color: "#999" }}>
                                    We weren't able to find any tweets made by this user yet
                                </h5>
                            </div>
                        </CardBody>
                } else {
                    tweets =
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
                                    <Pagination count={this.state.tweets.noPage} page={this.state.tweets.curPage} onChange={this.changePageTweets} variant="outlined" color="primary" showFirstButton showLastButton shape="rounded" />
                                </div>
                            </div>
                        </CardBody>
                }

                ///////////////////////

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
                                        width: "150px", marginTop: "15px", borderWidth: "2px"
                                    }}><i class="fas fa-chevron-left"></i> Go Back</Button>
                                </Col>
                            </Row>
                            <Row>
                                <Col xs="12" sm="12" md="4">
                                    <Card profile>
                                        <CardAvatar profile>
                                            <a onClick={e => e.preventDefault()}>
                                                <img src={this.userInfo.profile_image_url_https.replace("normal", "400x400")} alt="Profile Image" style={{ minWidth: "100px" }} />
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
                                            }}>@{this.userInfo.screen_name}</h6>
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
                                            }}>{this.userInfo.name}</h4>
                                            <h5 style={{ marginTop: "15px" }}>
                                                <i>{this.userInfo.description}</i>
                                            </h5>

                                            {locale}

                                            <div class="row" style={{ marginTop: "20px" }}>
                                                <div class="col-sm-12 offset-md-3 col-md-3">
                                                    <h6><b>{this.userInfo.followers_count}</b> <br />following</h6>
                                                </div>

                                                <div class="col-sm-12 col-md-3">
                                                    <h6><b>{this.userInfo.friends_count}</b> <br />followers</h6>
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
                                        {tweets}
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
                            {modal}
                        </Container>
                    </div>
                )
            }
        }

    }
}

export default UserProfileRedirected;

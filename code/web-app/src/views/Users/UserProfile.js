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
import BotProfile from '../Bots/BotProfile';

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


class UserProfile extends Component {
    constructor() {
        super();
    }

    state = {
        error: null,
        goBack: false,
        doneLoading: false,
        redirectionList: [],

        userInfo: null,
        redirectUser: null,

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

        followers: {
            data: [],
            noPage: 1,
            curPage: 1,
            empty: false
        },

        followings: {
            data: [],
            noPage: 1,
            curPage: 1,
            empty: false
        },

        stats: {
            data: [],
            type: 'month'
        }

    };

    async getTweets(page, first) {
        await fetch(baseURL + "twitter/users/" + this.state.userInfo.user_id + "/tweets/7/" + page + "/", {
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
                        if(tweet.quoted_status_id != null){
                            tempInfo.push(<span style={{ color: "#1b95e0", cursor: "pointer" }} onClick={() => this.handleOpenTweet(tweet.quoted_status_id)}>#{tweet.quoted_status_id}</span>);
                        }else{
                            tempInfo.push(<span style={{ color: "#999" }}><i class="fas fa-minus"></i></span>);
                        }

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

                    if (tweet.extended_entities != null) {
                        if (tweet.extended_entities.media[0].type == "video") {
                            tweet.extended_entities.media[0] = { "type": "video", "url": tweet.extended_entities.media[0].video_info.variants[0].url, "placeholder": tweet.extended_entities.media[0].media_url_https }
                        } else if (tweet.extended_entities.media[0].type == "animated_gif") {
                            tweet.extended_entities.media[0] = { "type": "gif", "url": tweet.extended_entities.media[0].video_info.variants[0].url, "placeholder": tweet.extended_entities.media[0].media_url_https }
                        }

                    }


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
                        tweets: {
                            data: tempTweets,
                            noPage: data.num_pages,
                            curPage: page,
                            latestTweet: data.entries[0],
                            tweet: null,
                            empty: empty
                        }
                    })
                } else {
                    this.setState({
                        tweets: {
                            data: tempTweets,
                            noPage: data.num_pages,
                            curPage: page,
                            latestTweet: this.state.tweets.latestTweet,
                            tweet: null,
                            empty: empty
                        }
                    })
                }

            }
        }).catch(error => {
            console.log("error: " + error);
            this.setState({
                error: error
            })
        });
    }

    async getFollowers(page) {
        await fetch(baseURL + "twitter/users/" + this.state.userInfo.user_id + "/followers/5/" + page + "/", {
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

                var tempUsers = []

                console.log(data)

                data.entries.forEach(user => {
                    var tempInfo = []

                    tempInfo.push("@" + user.username)
                    tempInfo.push(user.name)

                    if (user.label == "Bot") {
                        tempInfo.push(<span><i class="fas fa-robot" style={{ color: "#1da1f2" }}></i> Bot</span>)
                    } else {
                        tempInfo.push(<span><i class="fas fa-user" style={{ color: "#1da1f2" }}></i> User</span>)
                    }

                    tempInfo.push(
                        <Button block outline color="primary"
                            onClick={() => this.handleOpenProfile(user.id)}
                        >
                            <i class="far fa-user-circle"></i>
                            <strong style={{ marginLeft: "3px" }}>Profile</strong>
                        </Button>
                    )


                    tempUsers.push(tempInfo);
                })

                var empty = false
                if (tempUsers.length == 0) {
                    empty = true
                }

                this.setState({
                    followers: {
                        data: tempUsers,
                        noPage: data.num_pages,
                        curPage: page,
                        empty: empty
                    }
                })


            }
        }).catch(error => {
            console.log("error: " + error);
            this.setState({
                error: error
            })
        });
    }

    async getFollowings(page) {
        await fetch(baseURL + "twitter/users/" + this.state.userInfo.user_id + "/followers/5/" + page + "/", {
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

                var tempUsers = []

                data.entries.forEach(user => {
                    var tempInfo = []

                    tempInfo.push("@" + user.username)
                    tempInfo.push(user.name)
                    if (user.label == "Bot") {
                        tempInfo.push(<span><i class="fas fa-robot" style={{ color: "#1da1f2" }}></i> Bot</span>)
                    } else {
                        tempInfo.push(<span><i class="fas fa-user" style={{ color: "#1da1f2" }}></i> User</span>)
                    }
                    tempInfo.push(
                        <Button block outline color="primary"
                            onClick={() => this.handleOpenProfile(user.id)}
                        >
                            <i class="far fa-user-circle"></i>
                            <strong style={{ marginLeft: "3px" }}>Profile</strong>
                        </Button>
                    )

                    tempUsers.push(tempInfo);
                })

                var empty = false
                if (tempUsers.length == 0) {
                    empty = true
                }

                this.setState({
                    followings: {
                        data: tempUsers,
                        noPage: data.num_pages,
                        curPage: page,
                        empty: empty
                    }
                })


            }
        }).catch(error => {
            console.log("error: " + error);
            this.setState({
                error: error
            })
        });
    }

    async getUserInfo() {
        await fetch(baseURL + "twitter/users/" + this.props.nextUser + "/", {
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
                this.setState({ userInfo: data })
            }
        }).catch(error => {
            console.log("error: " + error);
            this.setState({
                error: "NOT FOUND"
            })
        });
    }

    async getStats(type) {
        await fetch(baseURL + "twitter/users/" + this.state.userInfo.user_id + "/stats/grouped/" + type + "/", {
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

                var tempData = []

                data.data.forEach(entry => {
                    var tempInfo = {}

                    tempInfo['name'] = entry['full_date'] + ""


                    tempInfo['followers'] = entry['sum_followers']
                    tempInfo['following'] = entry['sum_following']
                    tempInfo['tweets'] = 0 // TODO CHANGE THIS

                    tempData.push(tempInfo)
                })


                this.setState({
                    stats: {
                        data: tempData,
                        type: type
                    }
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
        console.log(this.props.user)
        if (this.props.user == null) {
            await this.getUserInfo()
        } else {
            await this.setState({ userInfo: this.props.user })
        }

        // Get Tweets
        if (this.state.error == null) {
            await this.getTweets(1, true)
        }

        // Get Stats
        if (this.state.error == null) {
            await this.getStats("month")
        }

        // Get Followers
        if (this.state.error == null) {
            await this.getFollowers(1)
        }

        // Get Followings
        if (this.state.error == null) {
            await this.getFollowings(1)
        }

        this.setState({
            doneLoading: true
        })

    }

    handleOpenProfile(user) {
        fetch(baseURL + "twitter/users/" + user + "/type/", {
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
                var list = this.state.redirectionList
                list.push({ type: "PROFILE", info: this.state.userInfo })
                this.setState({
                    redirectUser: { "user": user, "type": data.type },
                    redirectionList: list
                })

            }
        }).catch(error => {
            console.log("error: " + error);
            toast.error('Sorry, we couldn\'t redirect you to that user/bot\'s profile page. It\'s likely that they\'re still not in our databases, please try again later', {
                position: "top-center",
                autoClose: 7500,
                hideProgressBar: false,
                closeOnClick: true,
                pauseOnHover: true,
                draggable: true
            });
        });
    }

    // Methods //////////////////////////////////////////////////////////

    handleOpenTweet(tweet) {
        if(tweet.tweet_id != null){
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
        }else{
            fetch(baseURL + "twitter/tweets/" + tweet + "/", {
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
    
                    this.setState({
                        modal: true,
                        modalType: "TWEET",
                        tweets: {
                            data: this.state.tweets.data,
                            noPage: this.state.tweets.noPage,
                            curPage: this.state.tweets.curPage,
                            latestTweet: this.state.tweets.latestTweet,
                            tweet: data[0]
                        }
                    });
    
                }
            }).catch(error => {
                console.log("error: " + error);
                toast.error('🐦 Sorry, we couldn\'t find that tweet. It\'s likely that it\'s still not in our databases, please try again later', {
                    position: "top-center",
                    autoClose: 7500,
                    hideProgressBar: false,
                    closeOnClick: true,
                    pauseOnHover: true,
                    draggable: true
                });
            });
        } 
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
        this.setState({
            goBack: true,
        })
    }

    /////////////////////////////////////////////////////////////////////

    // Pagination //////////////////////////////////////////////////////////
    changePageTweets = async (event, value) => {
        document.getElementById("loadedTweets").style.visibility = "hidden"
        document.getElementById("loadingTweets").style.display = ""

        await this.getTweets(value, false)

        document.getElementById("loadedTweets").style.visibility = ""
        document.getElementById("loadingTweets").style.display = "none"
    };

    changePageFollowers = async (event, value) => {
        document.getElementById("loadedFollowers").style.visibility = "hidden"
        document.getElementById("loadingFollowers").style.display = ""

        await this.getFollowers(value)

        document.getElementById("loadedFollowers").style.visibility = ""
        document.getElementById("loadingFollowers").style.display = "none"
    };

    changePageFollowing = async (event, value) => {
        document.getElementById("loadedFollowings").style.visibility = "hidden"
        document.getElementById("loadingFollowings").style.display = ""

        await this.getFollowings(value)

        document.getElementById("loadedFollowings").style.visibility = ""
        document.getElementById("loadingFollowings").style.display = "none"
    };
    /////////////////////////////////////////////////////////////////////

    // Pagination //////////////////////////////////////////////////////////
    changeType = async (event, value) => {
        this.setState({
            stats: {
                data: this.state.stats.data,
                type: value
            }
        })

        await this.getStats(value)

    };
    /////////////////////////////////////////////////////////////////////


    render() {
        if (this.state.goBack) {
            if (this.state.redirectionList[this.state.redirectionList.length - 1]['type'] == "USERS")
                return (<Users page={this.state.redirectionList[0].info["page"]} searchQuery={this.state.redirectionList[0].info["query"]} />)
            else {
                var lastUser = this.state.redirectionList.pop()
                if (lastUser.type == "PROFILE") {
                    return (<UserProfile user={lastUser['info']} redirection={this.state.redirectionList}></UserProfile>)
                } else {
                    return (<BotProfile user={lastUser['info']} redirection={this.state.redirectionList}></BotProfile>)
                }
            }
        } else if (this.state.redirectUser != null) {
            if (this.state.redirectUser.type != null) {
                if (this.state.redirectUser.type == "Bot") {
                    return (
                        <BotProfile nextUser={this.state.redirectUser.user} redirection={this.state.redirectionList}></BotProfile>
                    )
                } else {
                    return (
                        <UserProfile nextUser={this.state.redirectUser.user} redirection={this.state.redirectionList}></UserProfile>
                    )
                }
            }
            return (
                <BotProfile nextUser={this.state.redirectUser} redirection={this.state.redirectionList}></BotProfile>
            )

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
                var modal
                if (this.state.modal) {
                    if (this.state.modalType == "TWEET") {
                        var extraInfo
                        if (this.state.tweets.tweet.is_quote_status) {
                            extraInfo = <h6 style={{ color: "#999" }}>
                                Retweeted <span style={{ color: "#1b95e0", cursor: "pointer" }} onClick={() => this.handleOpenTweet(this.state.tweets.tweet.quoted_status_id)}>#{this.state.tweets.tweet.quoted_status_id}</span>
                            </h6>
                        } else if (this.state.tweets.tweet.in_reply_to_screen_name != null) {
                            extraInfo = <h6 style={{ color: "#999" }}>
                                Replying to <span style={{ color: "#1b95e0", cursor: "pointer" }} onClick={() => this.handleOpenProfile(this.state.tweets.tweet.in_reply_to_user_id)}>@{this.state.tweets.tweet.in_reply_to_screen_name}</span>
                            </h6>
                        }

                        var media = <div></div>
                        if (this.state.tweets.tweet.extended_entities != null) {
                            console.log(this.state.tweets.tweet.extended_entities.media[0])
                            if (this.state.tweets.tweet.extended_entities.media[0].type == "photo") {
                                if (this.state.tweets.tweet.extended_entities.media.length == 1) {
                                    media =
                                        <div>
                                            <div class="d-flex flex-row flex-wrap justify-content-center">
                                                <div class="d-flex flex-column col-md-12">
                                                    <img src={this.state.tweets.tweet.extended_entities.media[0].media_url_https} id="tweetPic1" alt="Tweet Pic" onError={() => { document.getElementById("tweetPic1").src = require('../../assets/img/no_pic.png') }} style={{ width: "100%", display: "block", marginLeft: "auto", marginRight: "auto", borderRadius: "5%" }} />
                                                </div>
                                            </div>
                                        </div>
                                } else if (this.state.tweets.tweet.extended_entities.media.length == 2) {
                                    media =
                                        <div>
                                            <div class="d-flex flex-row flex-wrap justify-content-center">
                                                <div class="d-flex flex-column col-md-6">
                                                    <img src={this.state.tweets.tweet.extended_entities.media[0].media_url_https} id="tweetPic1" alt="Tweet Pic" onError={() => { document.getElementById("tweetPic1").src = require('../../assets/img/no_pic.png') }} style={{ width: "100%", display: "block", marginLeft: "auto", marginRight: "auto", borderRadius: "5%" }} />
                                                </div>

                                                <div class="d-flex flex-column col-md-6">
                                                    <img src={this.state.tweets.tweet.extended_entities.media[1].media_url_https} id="tweetPic2" alt="Tweet Pic" onError={() => { document.getElementById("tweetPic2").src = require('../../assets/img/no_pic.png') }} style={{ width: "100%", display: "block", marginLeft: "auto", marginRight: "auto", borderRadius: "5%" }} />
                                                </div>
                                            </div>
                                        </div>
                                } else if (this.state.tweets.tweet.extended_entities.media.length == 3) {
                                    media =
                                        <div>
                                            <div class="d-flex flex-row flex-wrap justify-content-center">
                                                <div class="d-flex flex-column col-md-6">
                                                    <img src={this.state.tweets.tweet.extended_entities.media[0].media_url_https} id="tweetPic1" alt="Tweet Pic" onError={() => { document.getElementById("tweetPic1").src = require('../../assets/img/no_pic.png') }} style={{ width: "100%", display: "block", marginLeft: "auto", marginRight: "auto", borderRadius: "5%" }} />
                                                </div>

                                                <div class="d-flex flex-column col-md-6">
                                                    <img src={this.state.tweets.tweet.extended_entities.media[1].media_url_https} id="tweetPic2" alt="Tweet Pic" onError={() => { document.getElementById("tweetPic2").src = require('../../assets/img/no_pic.png') }} style={{ width: "100%", display: "block", marginLeft: "auto", marginRight: "auto", borderRadius: "5%" }} />
                                                </div>
                                            </div>
                                            <div class="d-flex flex-row flex-wrap justify-content-center" style={{ marginTop: "25px" }}>
                                                <div class="d-flex flex-column col-md-6">
                                                    <img src={this.state.tweets.tweet.extended_entities.media[2].media_url_https} id="tweetPic3" alt="Tweet Pic" onError={() => { document.getElementById("tweetPic3").src = require('../../assets/img/no_pic.png') }} style={{ width: "100%", display: "block", marginLeft: "auto", marginRight: "auto", borderRadius: "5%" }} />
                                                </div>
                                            </div>
                                        </div>
                                } else {
                                    media =
                                        <div>
                                            <div class="d-flex flex-row flex-wrap justify-content-center">
                                                <div class="d-flex flex-column col-md-6">
                                                    <img src={this.state.tweets.tweet.extended_entities.media[0].media_url_https} id="tweetPic1" alt="Tweet Pic" onError={() => { document.getElementById("tweetPic1").src = require('../../assets/img/no_pic.png') }} style={{ width: "100%", display: "block", marginLeft: "auto", marginRight: "auto", borderRadius: "5%" }} />
                                                </div>

                                                <div class="d-flex flex-column col-md-6">
                                                    <img src={this.state.tweets.tweet.extended_entities.media[1].media_url_https} id="tweetPic2" alt="Tweet Pic" onError={() => { document.getElementById("tweetPic2").src = require('../../assets/img/no_pic.png') }} style={{ width: "100%", display: "block", marginLeft: "auto", marginRight: "auto", borderRadius: "5%" }} />
                                                </div>
                                            </div>
                                            <div class="d-flex flex-row flex-wrap justify-content-center" style={{ marginTop: "25px" }}>
                                                <div class="d-flex flex-column col-md-6">
                                                    <img src={this.state.tweets.tweet.extended_entities.media[2].media_url_https} id="tweetPic3" alt="Tweet Pic" onError={() => { document.getElementById("tweetPic3").src = require('../../assets/img/no_pic.png') }} style={{ width: "100%", display: "block", marginLeft: "auto", marginRight: "auto", borderRadius: "5%" }} />
                                                </div>

                                                <div class="d-flex flex-column col-md-6">
                                                    <img src={this.state.tweets.tweet.extended_entities.media[3].media_url_https} id="tweetPic4" alt="Tweet Pic" onError={() => { document.getElementById("tweetPic4").src = require('../../assets/img/no_pic.png') }} style={{ width: "100%", display: "block", marginLeft: "auto", marginRight: "auto", borderRadius: "5%" }} />
                                                </div>
                                            </div>
                                        </div>
                                }
                            } else if (this.state.tweets.tweet.extended_entities.media[0].type == "video") {
                                media =
                                    <div>
                                        <div class="d-flex flex-row flex-wrap justify-content-center">
                                            <div class="d-flex flex-column col-md-12">
                                                <video controls src={this.state.tweets.tweet.extended_entities.media[0].url} style={{ width: "90%", display: "block", marginLeft: "auto", marginRight: "auto", borderRadius: "5%" }} />
                                            </div>
                                        </div>
                                    </div>
                            } else {
                                media =
                                    <div>
                                        <div class="d-flex flex-row flex-wrap justify-content-center">
                                            <div class="d-flex flex-column col-md-12">
                                                <video muted autoplay loop controls src={this.state.tweets.tweet.extended_entities.media[0].url} style={{ width: "90%", display: "block", marginLeft: "auto", marginRight: "auto", borderRadius: "5%" }} />
                                            </div>
                                        </div>
                                    </div>
                            }
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
                                            <h5>
                                                <i>{this.state.tweets.tweet.text}</i>
                                            </h5>

                                            {media}

                                            <h6 style={{ color: "#999", marginTop: "20px" }}>
                                                {this.state.tweets.tweet.created_at}
                                            </h6>
                                            <div class="row" style={{ marginTop: "20px", textAlign: "center" }}>
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
                if (this.state.userInfo.location != "" && this.state.userInfo.location.trim().length != 0) {
                    locale = <h5 style={{ marginTop: "15px" }}>
                        <span style={{ color: "#999", fontSize: "15px" }}><i>from</i> </span>{this.state.userInfo.location}
                    </h5>

                }

                var latestTweet = <CardBody></CardBody>

                if (this.state.tweets.latestTweet != null) {
                    var extraInfo
                    if (this.state.tweets.latestTweet.is_quote_status) {
                        extraInfo = <h6 style={{ color: "#999" }}>
                            Retweeted <span style={{ color: "#1b95e0", cursor: "pointer" }} onClick={() => this.handleOpenTweet(this.state.tweets.latestTweet.quoted_status_id)}>#{this.state.tweets.latestTweet.quoted_status_id}</span>
                        </h6>
                    } else if (this.state.tweets.latestTweet.in_reply_to_screen_name != null) {
                        extraInfo = <h6 style={{ color: "#999" }}>
                            Replying to <span style={{ color: "#1b95e0", cursor: "pointer" }} onClick={() => this.handleOpenProfile(this.state.tweets.latestTweet.in_reply_to_user_id)}>@{this.state.tweets.latestTweet.in_reply_to_screen_name}</span>
                        </h6>
                    }

                    var media = <div></div>
                    if (this.state.tweets.latestTweet.extended_entities != null) {
                        console.log(this.state.tweets.latestTweet.extended_entities.media[0])
                        if (this.state.tweets.latestTweet.extended_entities.media[0].type == "photo") {
                            if (this.state.tweets.latestTweet.extended_entities.media.length == 1) {
                                media =
                                    <div>
                                        <div class="d-flex flex-row flex-wrap justify-content-center">
                                            <div class="d-flex flex-column col-md-12">
                                                <img src={this.state.tweets.latestTweet.extended_entities.media[0].media_url_https} id="tweetPic1" alt="Tweet Pic" onError={() => { document.getElementById("tweetPic1").src = require('../../assets/img/no_pic.png') }} style={{ width: "100%", display: "block", marginLeft: "auto", marginRight: "auto", borderRadius: "5%" }} />
                                            </div>
                                        </div>
                                    </div>
                            } else if (this.state.tweets.latestTweet.extended_entities.media.length == 2) {
                                media =
                                    <div>
                                        <div class="d-flex flex-row flex-wrap justify-content-center">
                                            <div class="d-flex flex-column col-md-6">
                                                <img src={this.state.tweets.latestTweet.extended_entities.media[0].media_url_https} id="tweetPic1" alt="Tweet Pic" onError={() => { document.getElementById("tweetPic1").src = require('../../assets/img/no_pic.png') }} style={{ width: "100%", display: "block", marginLeft: "auto", marginRight: "auto", borderRadius: "5%" }} />
                                            </div>

                                            <div class="d-flex flex-column col-md-6">
                                                <img src={this.state.tweets.latestTweet.extended_entities.media[1].media_url_https} id="tweetPic2" alt="Tweet Pic" onError={() => { document.getElementById("tweetPic2").src = require('../../assets/img/no_pic.png') }} style={{ width: "100%", display: "block", marginLeft: "auto", marginRight: "auto", borderRadius: "5%" }} />
                                            </div>
                                        </div>
                                    </div>
                            } else if (this.state.tweets.latestTweet.extended_entities.media.length == 3) {
                                media =
                                    <div>
                                        <div class="d-flex flex-row flex-wrap justify-content-center">
                                            <div class="d-flex flex-column col-md-6">
                                                <img src={this.state.tweets.latestTweet.extended_entities.media[0].media_url_https} id="tweetPic1" alt="Tweet Pic" onError={() => { document.getElementById("tweetPic1").src = require('../../assets/img/no_pic.png') }} style={{ width: "100%", display: "block", marginLeft: "auto", marginRight: "auto", borderRadius: "5%" }} />
                                            </div>

                                            <div class="d-flex flex-column col-md-6">
                                                <img src={this.state.tweets.latestTweet.extended_entities.media[1].media_url_https} id="tweetPic2" alt="Tweet Pic" onError={() => { document.getElementById("tweetPic2").src = require('../../assets/img/no_pic.png') }} style={{ width: "100%", display: "block", marginLeft: "auto", marginRight: "auto", borderRadius: "5%" }} />
                                            </div>
                                        </div>
                                        <div class="d-flex flex-row flex-wrap justify-content-center" style={{ marginTop: "25px" }}>
                                            <div class="d-flex flex-column col-md-6">
                                                <img src={this.state.tweets.latestTweet.extended_entities.media[2].media_url_https} id="tweetPic3" alt="Tweet Pic" onError={() => { document.getElementById("tweetPic3").src = require('../../assets/img/no_pic.png') }} style={{ width: "100%", display: "block", marginLeft: "auto", marginRight: "auto", borderRadius: "5%" }} />
                                            </div>
                                        </div>
                                    </div>
                            } else {
                                media =
                                    <div>
                                        <div class="d-flex flex-row flex-wrap justify-content-center">
                                            <div class="d-flex flex-column col-md-6">
                                                <img src={this.state.tweets.latestTweet.extended_entities.media[0].media_url_https} id="tweetPic1" alt="Tweet Pic" onError={() => { document.getElementById("tweetPic1").src = require('../../assets/img/no_pic.png') }} style={{ width: "100%", display: "block", marginLeft: "auto", marginRight: "auto", borderRadius: "5%" }} />
                                            </div>

                                            <div class="d-flex flex-column col-md-6">
                                                <img src={this.state.tweets.latestTweet.extended_entities.media[1].media_url_https} id="tweetPic2" alt="Tweet Pic" onError={() => { document.getElementById("tweetPic2").src = require('../../assets/img/no_pic.png') }} style={{ width: "100%", display: "block", marginLeft: "auto", marginRight: "auto", borderRadius: "5%" }} />
                                            </div>
                                        </div>
                                        <div class="d-flex flex-row flex-wrap justify-content-center" style={{ marginTop: "25px" }}>
                                            <div class="d-flex flex-column col-md-6">
                                                <img src={this.state.tweets.latestTweet.extended_entities.media[2].media_url_https} id="tweetPic3" alt="Tweet Pic" onError={() => { document.getElementById("tweetPic3").src = require('../../assets/img/no_pic.png') }} style={{ width: "100%", display: "block", marginLeft: "auto", marginRight: "auto", borderRadius: "5%" }} />
                                            </div>

                                            <div class="d-flex flex-column col-md-6">
                                                <img src={this.state.tweets.latestTweet.extended_entities.media[3].media_url_https} id="tweetPic4" alt="Tweet Pic" onError={() => { document.getElementById("tweetPic4").src = require('../../assets/img/no_pic.png') }} style={{ width: "100%", display: "block", marginLeft: "auto", marginRight: "auto", borderRadius: "5%" }} />
                                            </div>
                                        </div>
                                    </div>
                            }
                        } else if (this.state.tweets.latestTweet.extended_entities.media[0].type == "video") {
                            media =
                                <div>
                                    <div class="d-flex flex-row flex-wrap justify-content-center">
                                        <div class="d-flex flex-column col-md-12">
                                            <video controls src={this.state.tweets.latestTweet.extended_entities.media[0].url} style={{ width: "90%", display: "block", marginLeft: "auto", marginRight: "auto", borderRadius: "5%" }} />
                                        </div>
                                    </div>
                                </div>
                        } else {
                            media =
                                <div>
                                    <div class="d-flex flex-row flex-wrap justify-content-center">
                                        <div class="d-flex flex-column col-md-12">
                                            <video muted autoplay loop controls src={this.state.tweets.latestTweet.extended_entities.media[0].url} style={{ width: "90%", display: "block", marginLeft: "auto", marginRight: "auto", borderRadius: "5%" }} />
                                        </div>
                                    </div>
                                </div>
                        }
                    }

                    latestTweet = <CardBody>
                        <div style={{ marginTop: "25px" }}>
                            {extraInfo}
                            <h5>
                                <i>{this.state.tweets.latestTweet.text}</i>
                            </h5>

                            {media}

                            <h6 style={{ color: "#999", marginTop: "20px" }}>
                                {this.state.tweets.latestTweet.created_at}
                            </h6>
                            <div class="row" style={{ marginTop: "20px", textAlign: "center" }}>
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

                //All Tweets

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
                                        top: "30%",
                                        left: "40%",
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

                //All Followers
                var followers = <CardBody></CardBody>
                if (this.state.followers.empty) {
                    followers =
                        <div style={{ marginTop: "25px" }}>
                            <h5 style={{ color: "#999" }}>
                                We weren't able to find any of this user's followers
                        </h5>
                        </div>
                } else {
                    followers =
                        <div style={{ position: "relative" }}>
                            <div
                                id="loadedFollowers"
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
                                    tableHead={["Username", "Name", "Type", ""]}
                                    tableData={this.state.followers.data}
                                />

                            </div>
                            <div
                                id="loadingFollowers"
                                style={{
                                    zIndex: 10,
                                    position: "absolute",
                                    top: "30%",
                                    left: "40%",
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
                                    <Pagination count={this.state.followers.noPage} page={this.state.followers.curPage} onChange={this.changePageFollowers} variant="outlined" color="primary" showFirstButton showLastButton shape="rounded" />
                                </div>
                            </div>
                        </div>
                }

                //All Followings
                var followings = <CardBody></CardBody>
                if (this.state.followings.empty) {
                    followings =
                        <div style={{ marginTop: "25px" }}>
                            <h5 style={{ color: "#999" }}>
                                We weren't able to find any of this user's followers
                        </h5>
                        </div>
                } else {
                    followings =
                        <div style={{ position: "relative" }}>
                            <div
                                id="loadedFollowings"
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
                                    tableHead={["Username", "Name", "Type", ""]}
                                    tableData={this.state.followings.data}
                                />

                            </div>
                            <div
                                id="loadingFollowings"
                                style={{
                                    zIndex: 10,
                                    position: "absolute",
                                    top: "30%",
                                    left: "40%",
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
                                    <Pagination count={this.state.followings.noPage} page={this.state.followings.curPage} onChange={this.changePageFollowing} variant="outlined" color="primary" showFirstButton showLastButton shape="rounded" />
                                </div>
                            </div>
                        </div>
                }

                ///////////////////////
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
                                                <img src={this.state.userInfo.profile_image_url_https.replace("normal", "400x400")} id="profilePic" alt="Profile Image" onError={() => { document.getElementById("profilePic").src = require('../../assets/img/no_pic_smaller.png') }} style={{ minWidth: "100px" }} />
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
                                            }}>@{this.state.userInfo.screen_name}</h6>
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
                                            }}>{this.state.userInfo.name}</h4>
                                            <h5 style={{ marginTop: "15px" }}>
                                                <i>{this.state.userInfo.description}</i>
                                            </h5>

                                            {locale}

                                            <div class="row" style={{ marginTop: "20px" }}>
                                                <div class="col-sm-12 offset-md-3 col-md-3">
                                                    <h6><b>{this.state.userInfo.followers_count}</b> <br />following</h6>
                                                </div>

                                                <div class="col-sm-12 col-md-3">
                                                    <h6><b>{this.state.userInfo.friends_count}</b> <br />followers</h6>
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
                                            <div class="row" style={{ marginTop: "10px" }}>
                                                <ToggleButtonGroup
                                                    value={this.state.stats.type}
                                                    exclusive
                                                    aria-label="text alignment"
                                                    onChange={this.changeType}
                                                    style={{ display: "block", marginLeft: "auto", marginRight: "auto" }}
                                                >
                                                    <ToggleButton value="day" aria-label="Daily">
                                                        Daily
                                                    </ToggleButton>
                                                    <ToggleButton value="month" aria-label="Monthly">
                                                        Monthly
                                                    </ToggleButton>
                                                    <ToggleButton value="year" aria-label="Yearly">
                                                        Yearly
                                                    </ToggleButton>
                                                </ToggleButtonGroup>
                                            </div>
                                            <div class="row" style={{ marginTop: "15px" }}>
                                                <ResponsiveContainer width="100%" height={250}>
                                                    <LineChart data={this.state.stats.data} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
                                                        <Legend verticalAlign="bottom" height={36} />
                                                        <Line name="Followers" type="monotone" dataKey="followers" stroke="#63c2de" strokeWidth={3} />
                                                        <Line name="Following" type="monotone" dataKey="following" stroke="#833ab4" strokeWidth={3} />
                                                        <Line name="Tweets" type="monotone" dataKey="tweets" stroke="#f77737" strokeWidth={3} strokeDasharray="5 5" />

                                                        <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
                                                        <XAxis dataKey="name" />
                                                        <YAxis width={82} angle={-25} />
                                                        <Tooltip />

                                                        <Brush dataKey="name" height={30} stroke="#1da1f2" />

                                                    </LineChart>
                                                </ResponsiveContainer>
                                            </div>

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
                                            {followers}
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
                                            {followings}
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

export default UserProfile;

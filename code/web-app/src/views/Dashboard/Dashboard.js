import React, { Component } from 'react';
import baseURL from '../../variables/baseURL'
import {
  FormGroup, Label, Input,
  Container, Row, Col, Button, Badge, Form,
} from 'reactstrap';

import Table from "../../components/Table/Table.js";

import Card from "../../components/Card/Card";
import CardHeader from "../../components/Card/CardHeader";
import CardBody from "../../components/Card/CardBody";
import CardIcon from "../../components/Card/CardIcon";
import CardFooter from '../../components/Card/CardFooter';

import { ToastContainer, toast, Flip } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import ReactLoading from "react-loading";
import Pagination from '@material-ui/lab/Pagination';

import { PieChart } from 'react-minimal-pie-chart';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend, Brush, Bar, BarChart } from 'recharts';

import ToggleButton from '@material-ui/lab/ToggleButton';
import ToggleButtonGroup from '@material-ui/lab/ToggleButtonGroup';

import FadeIn from "react-fade-in";
import Lottie from "react-lottie";

import Dialog from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogTitle from "@material-ui/core/DialogTitle";

import * as loadingAnim from "../../assets/animations/squares_1.json";

import UserProfile from '../Users/UserProfile';
import BotProfile from '../Bots/BotProfile';


class Dashboard extends Component {
  constructor() {
    super();
  }

  state = {
    error: false,
    doneLoading: false,

    modal: false,
    modalType: null,

    animationOptions: {
      loop: true, autoplay: true, animationData: loadingAnim.default, rendererSettings: {
        preserveAspectRatio: "xMidYMid slice"
      }
    },

    redirect: {
      user: null,
      type: null
    },

    counter: {
      noUsers: 0,
      noBots: 0,
      noTweets: 0
    },

    tweets: {
      data: [],
      noPage: 1,
      curPage: 1,
      tweet: null,
      empty: true,
      noTweets: 100
    },

    activities: {
      data: [],
      noPage: 1,
      curPage: 1,
      empty: true,
      noActivities: 100
    },

    generalStats: {
      data: [],
      type: "month"
    },

    entityStats: {
      data: [],
      type: "month"
    },

    relationStats: {
      data: [],
      type: "month"
    },

    todayStats: {
      general: [],
      entities: {},
      relations: {}
    }

  };

  async getTodayStats() {
    await fetch(baseURL + "graphs/general/today/", {
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

        var tempInfo = {}
        tempInfo['name'] = ""
        tempInfo['general'] = data["data"]

        this.setState({
          todayStats: {
            general: [tempInfo],
            entities: this.state.todayStats.entities,
            relations: this.state.todayStats.relations
          }
        })
      }
    }).catch(error => {
      console.log("error: " + error);
      this.setState({
        error: true,
      })
    });


    await fetch(baseURL + "graphs/user_tweets/today/", {
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

        var tempInfo = {}


        tempInfo['name'] = ""
        tempInfo['users'] = data['user']
        tempInfo['tweets'] = data['tweets']

        this.setState({
          todayStats: {
            general: this.state.todayStats.general,
            entities: [tempInfo],
            relations: this.state.todayStats.relations
          }
        })
      }
    }).catch(error => {
      console.log("error: " + error);
      this.setState({
        error: true,
      })
    });

    await fetch(baseURL + "graphs/relations/today/", {
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


        var tempInfo = {}

        tempInfo['name'] = ""

        tempInfo['follows'] = data['follow']
        tempInfo['likes'] = data['likes']
        tempInfo['replies'] = data['replies']
        tempInfo['retweets'] = data['retweet']
        tempInfo['quotes'] = data['quotes']


        this.setState({
          todayStats: {
            general: this.state.todayStats.general,
            entities: this.state.todayStats.entities,
            relations: [tempInfo]
          }
        })
      }
    }).catch(error => {
      console.log("error: " + error);
      this.setState({
        error: true,
      })
    });
  }

  async getTweets(page) {
    await fetch(baseURL + "graphs/latest_tweets/daily/5/" + page + "/", {
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
          tempInfo.push(<span style={{ color: "#1b95e0", cursor: "pointer" }} onClick={() => this.handleOpenProfile(tweet.in_reply_to_user_id)}>@jonas</span>);

          if (tweet.is_quote_status) {
            tempInfo.push(<Badge pill color="warning" style={{ fontSize: "11px" }}>Quote</Badge>);
            if (tweet.quoted_status_id != null) {
              tempInfo.push(<span style={{ color: "#1b95e0", cursor: "pointer" }} onClick={() => this.handleOpenTweet(tweet.quoted_status_id)}>#{tweet.quoted_status_id}</span>);
            } else {
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

        this.setState({
          tweets: {
            data: tempTweets,
            noPage: data.num_pages,
            curPage: page,
            tweet: null,
            empty: empty,
            noTweets: this.state.tweets.noTweets
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

  async getActivities(page) {
    await fetch(baseURL + "graphs/latest_activities/daily/6/" + page + "/", {
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

        var tempActivities = []

        console.log(data)

        data.entries.forEach(activity => {
          var tempInfo = []
          tempInfo.push(activity.action)
          tempInfo.push(<span style={{ color: "#1b95e0", cursor: "pointer" }} onClick={() => this.handleOpenProfile("foof")}>@jonas</span>);

          if (activity.target_screen_name == null || activity.target_screen_name == "") {
            tempInfo.push(<span style={{ color: "#1b95e0", cursor: "pointer" }} onClick={() => this.handleOpenTweet(activity.target_id)}>#{activity.target_id}</span>);
          } else {
            tempInfo.push(<span style={{ color: "#1b95e0", cursor: "pointer" }} onClick={() => this.handleOpenProfile(activity.target_id)}>@{activity.target_screen_name}</span>);
          }

          var date = new Date(activity.timestamp)

          date = date.toString()
          date = date.split(" ")
          date = date[4] + " · " + date[1] + " " + date[2] + ", " + date[3] + " (" + date[0] + ")"

          tempInfo.push(date)

          tempActivities.push(tempInfo);
        })

        var empty = false
        if (tempActivities.length == 0) {
          empty = true
        }

        this.setState({
          activities: {
            data: tempActivities,
            noPage: data.num_pages,
            curPage: page,
            tweet: null,
            empty: empty,
            noActivities: this.state.activities.noActivities
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

  async getActivityStats(type) {
    await fetch(baseURL + "graphs/gen_stats_grouped/new/" + type + "/", {
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

        data.forEach(entry => {
          var tempInfo = {}

          tempInfo['name'] = entry['date'] + ""


          tempInfo['activities'] = entry['general']

          tempData.push(tempInfo)
        })


        this.setState({
          generalStats: {
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

  async getEntityStats(type) {
    await fetch(baseURL + "graphs/user_tweets_stats_grouped/new/" + type + "/", {
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

        data.forEach(entry => {
          var tempInfo = {}

          tempInfo['name'] = entry['date'] + ""

          tempInfo['tweets'] = entry['tweets']
          tempInfo['users'] = entry['users']

          tempData.push(tempInfo)
        })


        this.setState({
          entityStats: {
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

  async getRelationStats(type) {
    await fetch(baseURL + "graphs/relations_stats_grouped/new/" + type + "/", {
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

        data.forEach(entry => {
          var tempInfo = {}

          tempInfo['name'] = entry['date'] + ""

          tempInfo['follows'] = entry['follows']
          tempInfo['likes'] = entry['likes']
          tempInfo['replies'] = entry['replies']
          tempInfo['retweets'] = entry['retweets']
          tempInfo['quote'] = entry['quote']

          tempData.push(tempInfo)
        })


        this.setState({
          relationStats: {
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
    await this.getActivityStats("month")
    await this.getRelationStats("month")
    await this.getEntityStats("month")

    await this.getActivities(1)
    await this.getTweets(1)

    await this.getTodayStats()

    console.log(this.state.todayStats)

    this.setState({
      doneLoading: true
    })
  }


  // Methods //////////////////////////////////////////////////////////
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

        this.setState({
          redirect: {
            user: user,
            type: data.type
          },
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

  handleOpenTweet(tweet) {
    if (tweet.tweet_id != null) {
      this.setState({
        modal: true,
        modalType: "TWEET",
        tweets: {
          data: this.state.tweets.data,
          noPage: this.state.tweets.noPage,
          curPage: this.state.tweets.curPage,
          empty: this.state.tweets.empty,
          noTweets: this.state.tweets.noTweets,
          tweet: tweet
        }
      });
    } else {
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
          console.log(data)

          this.setState({
            modal: true,
            modalType: "TWEET",
            tweets: {
              data: this.state.tweets.data,
              noPage: this.state.tweets.noPage,
              curPage: this.state.tweets.curPage,
              empty: this.state.tweets.empty,
              noTweets: this.state.tweets.noTweets,
              tweet: data
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
        empty: this.state.tweets.empty,
        noTweets: this.state.tweets.noTweets,
        tweet: null
      }
    });
  }

  keydown(e) {
    if (e.keyCode == 13) {
      document.getElementById("searchButton").click()
    }
  }

  async search() {
    if (document.getElementById("searchUser").value != null && document.getElementById("searchUser").value != "" && !document.getElementById("searchUser").value.match("^[0-9]+$")) {
      toast.error('The number of tweets must be a number...', {
        position: "top-center",
        autoClose: 7500,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true
      });
    } else {
      document.getElementById("loadedTweets").style.visibility = "hidden"
      document.getElementById("loadingTweets").style.display = ""

      var value = 100
      if (!document.getElementById("searchUser").value == "") {
        value = parseInt(document.getElementById("searchUser").value)
      }

      await this.setState({
        tweets: {
          data: this.state.tweets.data,
          noPage: this.state.tweets.noPage,
          curPage: this.state.tweets.curPage,
          tweet: this.state.tweets.tweet,
          empty: this.state.tweets.empty,
          noTweets: value
        }
      })

      await this.getTweets(1)

      if (!this.state.error) {
        document.getElementById("loadedTweets").style.visibility = ""
        document.getElementById("loadingTweets").style.display = "none"
      }
    }
  }

  keydown2(e) {
    if (e.keyCode == 13) {
      document.getElementById("searchButton2").click()
    }
  }

  async search2() {
    if (document.getElementById("searchUser2").value != null && document.getElementById("searchUser2").value != "" && !document.getElementById("searchUser2").value.match("^[0-9]+$")) {
      toast.error('The number of activities must be a number...', {
        position: "top-center",
        autoClose: 7500,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true
      });
    } else {
      document.getElementById("loadedActivities").style.visibility = "hidden"
      document.getElementById("loadingActivities").style.display = ""

      var value = 100
      if (!document.getElementById("searchUser2").value == "") {
        value = parseInt(document.getElementById("searchUser2").value)
      }

      await this.setState({
        activities: {
          data: this.state.activities.data,
          noPage: this.state.activities.noPage,
          curPage: this.state.activities.curPage,
          empty: this.state.activities.empty,
          noActivities: value
        },
      })

      await this.getActivities(1)

      if (!this.state.error) {
        document.getElementById("loadedActivities").style.visibility = ""
        document.getElementById("loadingActivities").style.display = "none"
      }
    }
  }
  /////////////////////////////////////////////////////////////////////


  changeGeneralType = async (event, value) => {
    if (value != null) {
      this.setState({
        generalStats: {
          data: this.state.generalStats.data,
          type: value
        }
      })

      await this.getActivityStats(value)
    }
  };

  changeEntityType = async (event, value) => {
    if (value != null) {
      this.setState({
        entityStats: {
          data: this.state.entityStats.data,
          type: value
        }
      })

      await this.getEntityStats(value)
    }
  };

  changeRelationType = async (event, value) => {
    if (value != null) {
      this.setState({
        relationStats: {
          data: this.state.relationStats.data,
          type: value
        }
      })

      await this.getRelationStats(value)
    }
  };

  // Pagination //////////////////////////////////////////////////////////
  changePageTweets = async (event, value) => {
    document.getElementById("loadedTweets").style.visibility = "hidden"
    document.getElementById("loadingTweets").style.display = ""

    await this.getTweets(value)

    if (!this.state.error) {
      document.getElementById("loadedTweets").style.visibility = ""
      document.getElementById("loadingTweets").style.display = "none"
    }
  };

  changePageActivity = async (event, value) => {
    document.getElementById("loadedActivities").style.visibility = "hidden"
    document.getElementById("loadingActivities").style.display = ""

    await this.getActivities(value)

    if (!this.state.error) {
      document.getElementById("loadedActivities").style.visibility = ""
      document.getElementById("loadingActivities").style.display = "none"
    }
  };

  /////////////////////////////////////////////////////////////////////


  loading = () => <div className="fadeIn pt-1 text-center"><ReactLoading type={"cubes"} color="#1da1f2" /></div>

  render() {
    if (this.state.redirect.user != null) {
      if (this.state.redirect.type == "Bot") {
        return (
          <BotProfile user={this.state.redirect.user} redirection={[{ "type": "STATS", "info": "" }]}></BotProfile>
        )
      } else {
        return (
          <UserProfile user={this.state.redirect.user} redirection={[{ "type": "STATS", "info": "" }]}></UserProfile>
        )
      }

    } else if (!this.state.doneLoading) {
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
      // MODALS ///////////////
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
              {"🐦 Tweet by "} <span style={{ color: "#1b95e0", cursor: "pointer" }} onClick={() => this.handleOpenProfile('foof')}>@jonas</span> <span style={{ color: "#999", fontSize: "15px" }}>({"#" + this.state.tweets.tweet.tweet_id})</span>
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


      // TWEETS ///////////////
      var tweets = <CardBody></CardBody>

      if (this.state.tweets.empty) {
        tweets =
          <CardBody>
            <div style={{ marginTop: "25px" }}>
              <h5 style={{ color: "#999" }}>
                There don't seem to be any new tweets today...
                </h5>
            </div>
          </CardBody>
      } else {
        tweets =
          <CardBody>
            <div class="row" style={{ marginTop: "15px" }}>
              <div class="col-md-4 col-sm-12 form-group">
                <input type="text" placeholder="Number of tweets (default 100)" class="form-control" id="searchUser" onKeyDown={this.keydown} />
              </div>
              <div class="col-md-2 col-sm-12">
                <Button outline color="primary" id="searchButton"
                  onClick={() => this.search()}
                >

                  <i class="fas fa-filter"></i>
                  <strong style={{ marginLeft: "3px" }}>Filter</strong>
                </Button>
              </div>
            </div>
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
                  tableHead={["Id", "User", "Type", "Replying to", "Date", ""]}
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


      // ACTIVITIES ///////////////
      var activity = <CardBody></CardBody>
      if (this.state.activities.empty) {
        activity =
          <CardBody>
            <div style={{ marginTop: "25px" }}>
              <h5 style={{ color: "#999" }}>
                There don't seem to be any new activities today...
            </h5>
            </div>
          </CardBody>
      } else {
        activity = <CardBody>
          <div class="row" style={{ marginTop: "15px" }}>
            <div class="col-md-5 col-sm-12 form-group">
              <input type="text" placeholder="Number of activities (default 100)" class="form-control" id="searchUser2" onKeyDown={this.keydown2} />
            </div>
            <div class="col-md-2 col-sm-12">
              <Button outline color="primary" id="searchButton2"
                onClick={() => this.search2()}
              >

                <i class="fas fa-filter"></i>
                <strong style={{ marginLeft: "3px" }}>Filter</strong>
              </Button>
            </div>
          </div>
          <div style={{ position: "relative" }}>
            <div
              id="loadedActivities"
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
                tableHead={["Type", "User", "Target", "Date"]}
                tableData={this.state.activities.data}
              />

            </div>
            <div
              id="loadingActivities"
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
              marginTop: "38px",
              width: "100%",
              textAlign: "center"
            }}>
              <div style={{ display: "inline-block" }}>
                <Pagination count={this.state.activities.noPage} page={this.state.activities.curPage} onChange={this.changePageActivity} variant="outlined" color="primary" showFirstButton showLastButton shape="rounded" />
              </div>
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
                      <strong>Home</strong>
                    </h3>
                    <h5 style={{ color: "white" }}>
                      Today's numbers and statistics
                      </h5>
                  </CardHeader>
                  <CardBody>
                  </CardBody>
                </Card>
              </Col>
            </Row>

            <Row>
              <Col xs="12" sm="12" md="5">
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
                    }} ><strong>Today's Entity Count</strong></h4>
                    <h6>
                      Number of new users and tweets registered today
                    </h6>
                  </CardHeader>
                  <CardBody>
                    <div class="row" style={{ marginTop: "55px", marginBottom: "20px" }}>
                      <ResponsiveContainer width="100%" height={350}>
                        <BarChart data={this.state.todayStats.entities} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
                          <Legend verticalAlign="bottom" height={36} />
                          <Tooltip cursor={false} />

                          <Bar name="Users" dataKey="users" fill="#f77737" />
                          <Bar name="Tweets" dataKey="tweets" fill="#63c2de" />

                          <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
                          <XAxis dataKey="name" />
                          <YAxis width={82} angle={-25} />

                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </CardBody>

                </Card>
              </Col>


              <Col xs="12" sm="12" md="7">
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
                    }} ><strong>Entities</strong></h4>
                    <h6>
                      Number of entities recorded over time
                    </h6>
                  </CardHeader>
                  <CardBody>
                    <div class="row" style={{ marginTop: "10px" }}>
                      <ToggleButtonGroup
                        value={this.state.entityStats.type}
                        exclusive
                        aria-label="text alignment"
                        onChange={this.changeEntityType}
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
                      <ResponsiveContainer width="100%" height={350}>
                        <LineChart data={this.state.entityStats.data} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
                          <Legend verticalAlign="bottom" height={36} />
                          <Line name="Users" type="monotone" dataKey="users" stroke="#f77737" strokeWidth={3} />
                          <Line name="Tweets" type="monotone" dataKey="tweets" stroke="#63c2de" strokeWidth={3} />

                          <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
                          <XAxis dataKey="name" />
                          <YAxis width={82} angle={-25} />
                          <Tooltip />

                          <Brush dataKey="name" height={50} stroke="#1da1f2" >
                            <LineChart data={this.state.entityStats.data}>
                              <Line name="Users" type="monotone" dataKey="users" stroke="#f77737" strokeWidth={3} />
                              <Line name="Tweets" type="monotone" dataKey="tweets" stroke="#63c2de" strokeWidth={3} />
                            </LineChart>
                          </Brush>

                        </LineChart>
                      </ResponsiveContainer>
                    </div>
                  </CardBody>

                </Card>
              </Col>
            </Row>

            <Row>
              <Col xs="12" sm="12" md="5">
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
                    }} ><strong>Today's Relation Count</strong></h4>
                    <h6>
                      Number of new relations registered today
                    </h6>
                  </CardHeader>
                  <CardBody>
                    <div class="row" style={{ marginTop: "55px", marginBottom: "20px" }}>
                      <ResponsiveContainer width="100%" height={350}>
                        <BarChart data={this.state.todayStats.relations} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
                          <Legend verticalAlign="bottom" height={36} />
                          <Tooltip cursor={false} />

                          <Bar name="Follows" dataKey="users" fill="#f8cb00" />
                          <Bar name="Likes" dataKey="tweets" fill="#c13584" />
                          <Bar name="Replies" dataKey="users" fill="#833ab4" />
                          <Bar name="Retweets" dataKey="retweets" fill="#fd1d1d" />
                          <Bar name="Quotes" dataKey="quotes" fill="#17a2b8" />

                          <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
                          <XAxis dataKey="name" />
                          <YAxis width={82} angle={-25} />

                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </CardBody>

                </Card>
              </Col>


              <Col xs="12" sm="12" md="7">
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
                    }} ><strong>Relations</strong></h4>
                    <h6>
                      Number of relations recorded over time
                    </h6>
                  </CardHeader>
                  <CardBody>
                    <div class="row" style={{ marginTop: "10px" }}>
                      <ToggleButtonGroup
                        value={this.state.relationStats.type}
                        exclusive
                        aria-label="text alignment"
                        onChange={this.changeRelationType}
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
                      <ResponsiveContainer width="100%" height={350}>
                        <LineChart data={this.state.relationStats.data} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
                          <Legend verticalAlign="bottom" height={36} />
                          <Line name="Follows" type="monotone" dataKey="follows" stroke="#f8cb00" strokeWidth={2} />
                          <Line name="Likes" type="monotone" dataKey="likes" stroke="#c13584" strokeWidth={2} />
                          <Line name="Replies" type="monotone" dataKey="replies" stroke="#833ab4" strokeWidth={2} />
                          <Line name="Retweets" type="monotone" dataKey="retweets" stroke="#fd1d1d" strokeWidth={2} />
                          <Line name="Quotes" type="monotone" dataKey="quote" stroke="#17a2b8" strokeWidth={2} />

                          <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
                          <XAxis dataKey="name" />
                          <YAxis width={82} angle={-25} />
                          <Tooltip />

                          <Brush dataKey="name" height={50} stroke="#1da1f2">
                            <LineChart data={this.state.relationStats.data}>
                              <Line name="Follows" type="monotone" dataKey="follows" stroke="#f8cb00" strokeWidth={2} />
                              <Line name="Likes" type="monotone" dataKey="likes" stroke="#c13584" strokeWidth={2} />
                              <Line name="Replies" type="monotone" dataKey="replies" stroke="#833ab4" strokeWidth={2} />
                              <Line name="Retweets" type="monotone" dataKey="retweets" stroke="#fd1d1d" strokeWidth={2} />
                              <Line name="Quotes" type="monotone" dataKey="quote" stroke="#17a2b8" strokeWidth={2} />
                            </LineChart>
                          </Brush>

                        </LineChart>
                      </ResponsiveContainer>
                    </div>
                  </CardBody>
                </Card>
              </Col>
            </Row>

            <Row>
              <Col xs="12" sm="12" md="5">
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
                    }} ><strong>Today's Activity Count</strong></h4>
                    <h6>
                      Number of new activities registered today
                    </h6>
                  </CardHeader>
                  <CardBody>
                    <div class="row" style={{ marginTop: "55px", marginBottom: "20px" }}>
                      <ResponsiveContainer width="100%" height={350}>
                        <BarChart data={this.state.todayStats.general} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
                          <Legend verticalAlign="bottom" height={36} />
                          <Tooltip cursor={false} />

                          <Bar name="Activities" dataKey="general" fill="#f86c6b" />

                          <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
                          <XAxis dataKey="name" />
                          <YAxis width={82} angle={-25} />

                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </CardBody>

                </Card>
              </Col>


              <Col xs="12" sm="12" md="7">
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
                    }} ><strong>Activities</strong></h4>
                    <h6>
                      Number of activities recorded over time
                    </h6>
                  </CardHeader>
                  <CardBody>
                    <div class="row" style={{ marginTop: "10px" }}>
                      <ToggleButtonGroup
                        value={this.state.generalStats.type}
                        exclusive
                        aria-label="text alignment"
                        onChange={this.changeGeneralType}
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
                      <ResponsiveContainer width="100%" height={350}>
                        <LineChart data={this.state.generalStats.data} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
                          <Legend verticalAlign="bottom" height={36} />
                          <Line name="Activities" type="monotone" dataKey="activities" stroke="#f86c6b" strokeWidth={3} />

                          <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
                          <XAxis dataKey="name" />
                          <YAxis width={82} angle={-25} />
                          <Tooltip />

                          <Brush dataKey="name" height={50} stroke="#1da1f2" >
                            <LineChart data={this.state.generalStats.data}>
                              <Line name="Activities" type="monotone" dataKey="activities" stroke="#f86c6b" strokeWidth={3} />
                            </LineChart>
                          </Brush>

                        </LineChart>
                      </ResponsiveContainer>
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
                    }} ><strong>Today's Activities</strong></h4>
                    <h6>
                      Today's recorded activities
                    </h6>
                  </CardHeader>
                  {activity}

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
                    }} ><strong>Today's Tweets</strong></h4>
                    <h6>
                      Today's recorded tweets
                    </h6>
                  </CardHeader>
                  {tweets}
                </Card>
              </Col>
            </Row>
            {modal}
          </Container>
        </div >
      );
    }
  }
}


export default Dashboard;

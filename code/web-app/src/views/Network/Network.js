import React, { Component } from 'react';
import ReactDOM from "react-dom";
import Graph from "react-graph-vis";

import baseURL from '../../variables/baseURL'

import {
  Container, Row, Col, Button, Form,
  FormGroup,
  FormText,
  FormFeedback,
  Input,
  InputGroup,
  InputGroupAddon,
  InputGroupButtonDropdown,
  InputGroupText,
  Pagination, PaginationItem, PaginationLink,
  Label,
} from 'reactstrap';
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

import Select from 'react-select';

import Table from "../../components/Table/Table.js";

import { ToastContainer, toast, Flip } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import ReactLoading from "react-loading";
import ReactPaginate from 'react-paginate';

import FadeIn from "react-fade-in";
import Lottie from "react-lottie";

import * as loadingAnim from "../../assets/animations/squares_1.json";
import NetworkReport from './NetworkReport';
import UserProfile from '../Users/UserProfile';
import BotProfile from '../Bots/BotProfile';

class Network extends Component {
  constructor(props) {
    super(props);
  }

  state = {
    loading: true,
    graph: {
      nodes: [],
      edges: []
    },

    nodesForSelect: [],

    options: {
      autoResize: true,
      layout: {
        hierarchical: false,
      },
      edges: {
        color: "#000000",
        font: {
          size: 13,
          color: '#999'
        },
        smooth: {
          type: "discrete"
        }
      },
      nodes: {
        size: 30,
        shape: 'dot',

        font: {
          color: '#000',
          strokeWidth: 5,
          size: 20,
        },
      },
      physics: {
        enabled: true,
        barnesHut: {
          gravitationalConstant: -10000,
          centralGravity: 0.1,
        }
      },

      interaction: {
        navigationButtons: true,
        keyboard: true
      },

      height: "850px",
    },

    animationOptions: {
      loop: true, autoplay: true, animationData: loadingAnim.default, rendererSettings: {
        preserveAspectRatio: "xMidYMid slice"
      }
    },

    graphRef: null,
    hideBots: false,
    hideTweets: false,
    hideUsers: false,
    hideLinks: false,

    allNodes: [],
    allLinks: [],


    modal: false,
    modalType: null,
    modalInfo: null,

    foundNode: null,

    redirectNetwork: false,
    redirect: {
      user: null,
      type: null
    },
  }

  async getBaseNetwork() {
    await fetch(baseURL + "twitter/network", {
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


        var tempNodes = []
        var tempLinks = []
        var tempNodesForSelect = []

        data[0].nodes.forEach(item => {
          var tempItem = {}
          tempItem['id'] = item.id
          tempItem['name'] = item.properties.name
          tempItem['real_id'] = item.properties.id
          tempItem['username'] = "@" + item.properties.username
          tempItem['type'] = item.labels[0]

          if (tempItem['type'] == "Tweet") {
            tempItem['label'] = "#" + tempItem['real_id']
          } else {
            tempItem['label'] = item.properties.name
          }

          if (tempItem['type'] == "User") {
            tempItem['color'] = {
              border: '#405de6',
              background: "#1da1f2",
              highlight: {
                border: '#4dbd74',
                background: '#20c997'
              }
            }

          } else if (tempItem['type'] == "Bot") {
            tempItem['color'] = {
              border: '#63218f',
              background: "#833ab4",
              highlight: {
                border: '#4dbd74',
                background: '#20c997'
              }
            }

          } else if (tempItem['type'] == "Tweet") {
            tempItem['color'] = {
              border: '#ce2c2c',
              background: "#f86c6b",
              highlight: {
                border: '#4dbd74',
                background: '#20c997'
              }
            }

          }
          tempNodes.push(tempItem)
          if (tempItem['type'] == "Tweet") {
            tempNodesForSelect.push({ value: tempItem['id'], label: "(" + tempItem['type'] + ") #" + tempItem['real_id'] })
          } else {
            tempNodesForSelect.push({ value: tempItem['id'], label: "(" + tempItem['type'] + ") " + tempItem['name'] + " - " + tempItem['username'] })
          }

        })

        data[0].rels.forEach(item => {
          if (item != [] && item != null && item != undefined) {
            item = item[0]

            if (item != [] && item != null && item != undefined) {
              var tempItem = {}
              tempItem['id'] = item.id
              tempItem['from'] = item.start.id
              tempItem['to'] = item.end.id
              tempItem['label'] = item.label

              tempLinks.push(tempItem)
            }
          }
        })


        this.setState({
          graph: {
            nodes: tempNodes,
            edges: tempLinks,
          },

          nodesForSelect: tempNodesForSelect,

          allNodes: tempNodes,
          allLinks: tempLinks
        })

      }
    }).catch(error => {
      console.log("error: " + error);
      this.setState({
        error: true,
        loading: false
      })
    });
  }

  async processGraph() {
    var tempNodes = []
    var tempLinks = []
    var tempNodesForSelect = []


    console.log(this.props.returnValues)

    this.props.returnValues.nodes.forEach(item => {
      var tempItem = {}
      tempItem['id'] = item.id
      tempItem['name'] = item.properties.name
      tempItem['real_id'] = item.properties.id
      tempItem['username'] = "@" + item.properties.username
      tempItem['type'] = item.labels[0]

      if (tempItem['type'] == "Tweet") {
        tempItem['label'] = "#" + tempItem['real_id']
      } else {
        tempItem['label'] = item.properties.name
      }

      if (tempItem['type'] == "User") {
        tempItem['color'] = {
          border: '#405de6',
          background: "#1da1f2",
          highlight: {
            border: '#4dbd74',
            background: '#20c997'
          }
        }

      } else if (tempItem['type'] == "Bot") {
        tempItem['color'] = {
          border: '#63218f',
          background: "#833ab4",
          highlight: {
            border: '#4dbd74',
            background: '#20c997'
          }
        }

      } else if (tempItem['type'] == "Tweet") {
        tempItem['color'] = {
          border: '#ce2c2c',
          background: "#f86c6b",
          highlight: {
            border: '#4dbd74',
            background: '#20c997'
          }
        }

      }
      tempNodes.push(tempItem)
      if (tempItem['type'] == "Tweet") {
        tempNodesForSelect.push({ value: tempItem['id'], label: "(" + tempItem['type'] + ") #" + tempItem['real_id'] })
      } else {
        tempNodesForSelect.push({ value: tempItem['id'], label: "(" + tempItem['type'] + ") " + tempItem['name'] + " - " + tempItem['username'] })
      }
    })

    this.props.returnValues.rels.forEach(item => {
      if (item != [] && item != null && item != undefined) {
        item = item[0]

        if (item != [] && item != null && item != undefined) {
          var tempItem = {}
          tempItem['id'] = item.id
          tempItem['from'] = item.start.id
          tempItem['to'] = item.end.id
          tempItem['label'] = item.label

          tempLinks.push(tempItem)
        }
      }
    })


    this.setState({
      graph: {
        nodes: tempNodes,
        edges: tempLinks,
      },

      nodesForSelect: tempNodesForSelect,

      allNodes: tempNodes,
      allLinks: tempLinks
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


  async componentDidMount() {
    await this.setState({
      loading: true
    })

    console.log(this.props.returnValues)

    if (this.props.returnValues == null) {
      // Get Network
      await this.getBaseNetwork()

      await this.setState({
        loading: false
      })
    } else {
      await this.processGraph()

      await this.setState({
        loading: false
      })
      toast.success('Successfully processed query!', {
        position: "top-center",
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true
      });
    }

    document.getElementById("loadedGraph").style.visibility = "visible"
    document.getElementById("loadingGraph").style.display = "none"
  }


  loading = () => <div className="fadeIn pt-1 text-center"><ReactLoading type={"cubes"} color="#1da1f2" /></div>


  // Graph methods //////////////////////////////////////////////////////////
  async resetNetwork() {
    document.getElementById("loadedGraph").style.visibility = "hidden"
    document.getElementById("loadingGraph").style.display = ""

    await this.setState({ hideBots: false, hideLinks: false, hideUsers: false, botRoot: [], userRoot: [] })
    document.getElementById("hideBots").checked = false
    document.getElementById("hideTweets").checked = false
    document.getElementById("hideUsers").checked = false
    document.getElementById("hideLinks").checked = false

    if (this.state.graphRef != null) {
      this.state.graphRef.selectNodes([])
      this.state.graphRef.moveTo({
        position: { x: 0, y: 0 },
        scale: 0.9,
        animation: {
          duration: 100,
          easingFunction: 'linear'
        }
      });
    }

    await this.setState({
      loading: true
    })

    // Get Network
    await this.getBaseNetwork()

    await this.setState({
      loading: false
    })

    document.getElementById("loadedGraph").style.visibility = "visible"
    document.getElementById("loadingGraph").style.display = "none"
  }
  /////////////////////////////////////////////////////////////////////


  // Select Methods //////////////////////////////////////////////////////////
  changeFindNode = (event) => {
    this.setState({ foundNode: event });
    var node = event.value
    if (this.state.graphRef != null) {
      try {
        this.state.graphRef.selectNodes([node])
        this.state.graphRef.focus(node, {
          scale: 1.3,
          animation: {
            duration: 100,
            easingFunction: 'linear'
          }
        })

        this.state.graphRef.moveTo({ position: this.state.graphRef.getPositions([node])[node] })
      } catch (e) {

      }
    }
  };

  removeFocus = () => {
    this.setState({ foundNode: '' });

    if (this.state.graphRef != null) {
      this.state.graphRef.selectNodes([])
      this.state.graphRef.moveTo({
        scale: 0.9,
        animation: {
          duration: 100,
          easingFunction: 'linear'
        }
      });
    }
  };
  /////////////////////////////////////////////////////////////////////

  // Hide Methods //////////////////////////////////////////////////////////

  hideBots = () => {
    this.setState({ hideBots: !this.state.hideBots }, () => {
      if (this.state.hideBots) {
        var tempArray = []

        this.state.graph.nodes.forEach(node => {
          if (node.type != "Bot") {
            tempArray.push(node)
          }
        })

        this.setState({
          graph: {
            nodes: tempArray,
            edges: this.state.allLinks
          }
        })
      } else {
        var tempArray = this.state.graph.nodes

        this.state.allNodes.forEach(node => {
          if (node.type == "Bot") {
            tempArray.push(node)
          }
        })

        this.setState({
          graph: {
            nodes: tempArray,
            edges: this.state.allLinks
          }
        })
      }

      this.state.graphRef.body.emitter.emit('_dataChanged')
      this.state.graphRef.redraw()
    })
  }

  hideUsers = () => {
    this.setState({ hideUsers: !this.state.hideUsers }, () => {
      if (this.state.hideUsers) {
        var tempArray = []

        this.state.graph.nodes.forEach(node => {
          if (node.type != "User") {
            tempArray.push(node)
          }
        })

        this.setState({
          graph: {
            nodes: tempArray,
            edges: this.state.allLinks
          }
        })
      } else {
        var tempArray = this.state.graph.nodes

        this.state.allNodes.forEach(node => {
          if (node.type == "User") {
            tempArray.push(node)
          }
        })

        this.setState({
          graph: {
            nodes: tempArray,
            edges: this.state.allLinks
          }
        })
      }

      this.state.graphRef.body.emitter.emit('_dataChanged')
      this.state.graphRef.redraw()
    })
  }

  hideTweets = () => {
    this.setState({ hideTweets: !this.state.hideTweets }, () => {
      if (this.state.hideTweets) {
        var tempArray = []

        this.state.graph.nodes.forEach(node => {
          if (node.type != "Tweet") {
            tempArray.push(node)
          }
        })

        this.setState({
          graph: {
            nodes: tempArray,
            edges: this.state.allLinks
          }
        })
      } else {
        var tempArray = this.state.graph.nodes

        this.state.allNodes.forEach(node => {
          if (node.type == "Tweet") {
            tempArray.push(node)
          }
        })

        this.setState({
          graph: {
            nodes: tempArray,
            edges: this.state.allLinks
          }
        })
      }

      this.state.graphRef.body.emitter.emit('_dataChanged')
      this.state.graphRef.redraw()
    })
  }

  hideLinks = () => {
    this.setState({ hideLinks: !this.state.hideLinks }, () => {
      if (this.state.hideLinks) {
        this.setState({
          graph: {
            nodes: this.state.graph.nodes,
            edges: []
          }
        })
      } else {
        this.setState({
          graph: {
            nodes: this.state.graph.nodes,
            edges: this.state.allLinks
          }
        })
      }

      this.state.graphRef.body.emitter.emit('_dataChanged')
      this.state.graphRef.redraw()
    })
  }
  /////////////////////////////////////////////////////////////////////

  // Modal Methods //////////////////////////////////////////////////////////
  handleClose() {
    this.setState({
      modal: false,
      modalType: null,
      modalInfo: null,
    });
  }

  openUserModal(element) {
    fetch(baseURL + "twitter/users/" + element.real_id + "/", {
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

        this.setState({
          modal: true,
          modalType: "USER",
          modalInfo: { 'base': element, 'info': data.data, 'error': null },
        })
      }
    }).catch(error => {
      console.log("error: " + error);
      this.setState({
        modal: true,
        modalType: "USER",
        modalInfo: { 'base': element, 'info': null, 'error': error },
      })
    });
  }

  handleOpenQuery() {
    this.setState({
      redirectNetwork: true
    })
  }
  /////////////////////////////////////////////////////////////////////


  render() {
    if (this.state.redirectNetwork) {
      return (<NetworkReport></NetworkReport>)
    }

    if (this.state.redirect.user != null) {
      if (this.state.redirect.type == "Bot") {
        return (
          <BotProfile nextUser={this.state.redirect.user} redirection={[{ "type": "NET", "info": { "redirectionList": this.props.returnValues } }]}></BotProfile>
        )
      } else {
        return (
          <UserProfile nextUser={this.state.redirect.user} redirection={[{ "type": "NET", "info": "" }]}></UserProfile>
        )
      }
    }

    if (this.state.loading) {
      return (
        <div className="animated fadeOut animated" style={{ width: "100%", marginTop: "10%" }}>
          <FadeIn>
            <Lottie options={this.state.animationOptions} height={"30%"} width={"30%"} />
          </FadeIn>
        </div>
      )
    }

    const events = {
      doubleClick: function (event) {
        var { nodes, edges } = event;

        try {
          this.state.graphRef.selectNodes([nodes[0]])


          var element = this.state.graph.nodes.find((element) => {
            return element.id == nodes[0];
          })

          this.handleOpenProfile(element.real_id)
        } catch (e) {

        }

      }.bind(this),

      click: function (event) {
        var { nodes } = event;

        this.state.graphRef.focus(nodes[0], {
          scale: 1.3,
          animation: {
            duration: 100,
            easingFunction: 'linear'
          }
        })

        var element = this.state.nodesForSelect.find((element) => {
          return element.value == nodes[0];
        })

        this.setState({ foundNode: element })

        this.state.graphRef.moveTo({ position: this.state.graphRef.getPositions([nodes[0]])[nodes[0]] })
      }.bind(this)
    }

    var graph
    graph = <Graph graph={this.state.graph} options={this.state.options} events={events} getNetwork={network => {
      this.setState({ graphRef: network })
    }} />

    var modal
    if (this.state.modal) {
      if (this.state.modalType == "TWEET") {
        modal =
          <Dialog class="fade-in"
            open={this.state.modal}
            onClose={() => this.handleClose()}
            aria-labelledby="alert-dialog-title"
            aria-describedby="alert-dialog-description"
          >
            <DialogTitle id="alert-dialog-title">
              <span>{"🐦 Tweet #" + this.state.modalInfo.real_id}</span>
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


    return (
      <div className="animated fadeIn">
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
        <Container fluid>
          <Row>
            <Col xs="12" sm="12" md="12">
              <Card>
                <CardHeader color="primary">
                  <h3 style={{ color: "white" }}>
                    <strong>Network</strong>
                  </h3>
                  <h5 style={{ color: "white" }}>
                    Graph with all users, bots and tweets on our database
                  </h5>
                </CardHeader>
                <CardBody>
                </CardBody>
              </Card>
            </Col>
          </Row>

          <Row>
            <Col xs="12" sm="12" md="9">
              <Card>
                <CardBody>
                  <div style={{ position: "relative" }}>
                    <div
                      id="loadedGraph"
                      style={{
                        width: "100%",
                        height: "100%",
                        position: "relative",
                        top: 0,
                        left: 0,
                        visibility: "hidden"
                      }}>
                      {graph}

                    </div>
                    <div
                      id="loadingGraph"
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
                </CardBody>
              </Card>
            </Col>
            <Col xs="12" sm="12" md="3">
              <Card>
                <CardHeader color="primary">
                  <h3 style={{ color: "white" }}>
                    <strong>Filters and Queries</strong>
                  </h3>
                </CardHeader>
                <CardBody>

                  <Row style={{ marginBottom: "35px" }}>
                    <Col md="12">
                      <h5 style={{ color: "#1fa8dd" }}><strong>Find node</strong></h5>
                      <Row>
                        <Col md="9" sm="12" xm="12">
                          <Select
                            defaultValue={[]}
                            id="findNode" onChange={this.changeFindNode}
                            value={this.state.foundNode || ''}
                            options={this.state.nodesForSelect}
                            className="basic-single"
                            classNamePrefix="select"
                          />
                        </Col>
                        <Col md="3" sm="12" xm="12">
                          <Button block outline color="danger"
                            onClick={this.removeFocus}
                          ><i class="fas fa-times"></i></Button>
                        </Col>

                      </Row>
                    </Col>
                  </Row>

                  <hr />

                  <Row style={{ marginTop: "20px" }}>
                    <Col md="6">
                      <FormGroup check>
                        <Input className="form-check-input" type="checkbox" id="hideBots" name="inline-checkbox1" onChange={this.hideBots} />
                        <Label className="form-check-label" check htmlFor="inline-checkbox1">Hide bots</Label>
                      </FormGroup>
                    </Col>
                    <Col md="6">
                      <FormGroup check>
                        <Input className="form-check-input" type="checkbox" id="hideUsers" name="inline-checkbox2" onChange={this.hideUsers} value="option2" />
                        <Label className="form-check-label" check htmlFor="inline-checkbox2">Hide users</Label>
                      </FormGroup>
                    </Col>
                  </Row>
                  <Row style={{ marginTop: "10px" }}>
                    <Col md="6">
                      <FormGroup check>
                        <Input className="form-check-input" type="checkbox" id="hideTweets" name="inline-checkbox2" onChange={this.hideTweets} value="option2" />
                        <Label className="form-check-label" check htmlFor="inline-checkbox2">Hide tweets</Label>
                      </FormGroup>
                    </Col>
                    <Col md="6">
                      <FormGroup check>
                        <Input className="form-check-input" type="checkbox" id="hideLinks" name="inline-checkbox2" onChange={this.hideLinks} value="option2" />
                        <Label className="form-check-label" check htmlFor="inline-checkbox2">Hide links</Label>
                      </FormGroup>
                    </Col>
                  </Row>

                  <hr></hr>
                  <h5 style={{ color: "#1fa8dd" }}><strong>Advanced Filters</strong></h5>
                  <Row style={{ marginTop: "25px" }}>
                    <Col md="6">
                      <Button block outline color="success"
                        onClick={() => this.handleOpenQuery()}
                      > Query <i class="fas fa-search" style={{ marginLeft: "8px" }}></i></Button>
                    </Col>
                    <Col md="6" style={{ alignItems: "center" }}>
                      <Button block outline color="danger"
                        onClick={() => this.resetNetwork()}
                      > Reset <i class="fas fa-times" style={{ marginLeft: "8px" }}></i></Button>
                    </Col>
                  </Row>

                </CardBody>
              </Card>

            </Col>
          </Row>
          {modal}
        </Container>
      </div>
    );
  }
}

export default Network;

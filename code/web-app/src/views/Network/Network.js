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
    botsForSelect: [],
    usersForSelect: [],


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
          centralGravity: 0.4,
        }
      },

      interaction: {
        navigationButtons: true,
        keyboard: true
      },

      height: "850px",
    },

    graphRef: null,
    hideBots: false,
    hideUsers: false,
    hideLinks: false,

    allNodes: null,
    allLinks: null,
    bots: null,
    users: null,

    bots: null,
    users: null,

    modal: false,
    modalType: null,
    modalInfo: null,

    botRoot: [],
    userRoot: [],
    foundNode: null
  }

  getBaseNetwork() {
    fetch(baseURL + "twitter/network", {
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


        var tempNodes = []
        var tempLinks = []
        var tempBots = []
        var tempUsers = []

        var tempNodesForSelect = []
        var tempNodesForSelectBots = []
        var tempNodesForSelectUsers = []


        data.forEach(item => {
          if (item.type == "node") {
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
              tempUsers.push(tempItem)

              tempNodesForSelectUsers.push({ value: tempItem['id'], label: "(" + tempItem['type'] + " #" + tempItem['real_id'] + ") " + tempItem['name'] + " - " + tempItem['username'] })
            } else if (tempItem['type'] == "Bot") {
              tempItem['color'] = {
                border: '#63218f',
                background: "#833ab4",
                highlight: {
                  border: '#4dbd74',
                  background: '#20c997'
                }
              }
              tempBots.push(tempItem)

              tempNodesForSelectBots.push({ value: tempItem['id'], label: "(" + tempItem['type'] + " #" + tempItem['real_id'] + ") " + tempItem['name'] + " - " + tempItem['username'] })
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
          } else {
            var tempItem = {}
            tempItem['id'] = item.id
            tempItem['from'] = item.start.id
            tempItem['to'] = item.end.id
            tempItem['label'] = item.label

            tempLinks.push(tempItem)
          }
        })

        this.setState({
          graph: {
            nodes: tempNodes,
            edges: tempLinks,
          },
          nodesForSelect: tempNodesForSelect,
          botsForSelect: tempNodesForSelectBots,
          usersForSelect: tempNodesForSelectUsers,

          allNodes: tempNodes,
          allLinks: tempLinks,
          bots: tempBots,
          users: tempUsers
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

  getSubNetwork(url) {
    fetch(url, {
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

        var tempNodes = []
        var tempLinks = []

        var tempNodesForSelect = []

        data.forEach(item => {
          item.nodes.forEach(node => {
            var element = tempNodes.find((element) => {
              return element.id == node.id;
            })
            if (element == null) {
              var tempItem = {}
              tempItem['id'] = node.id
              tempItem['name'] = node.properties.name
              tempItem['real_id'] = node.properties.id
              tempItem['username'] = "@" + node.properties.username
              tempItem['label'] = node.properties.name
              tempItem['type'] = node.labels[0]

              if (tempItem['type'] == "User") {
                tempItem['color'] = {
                  border: '#405de6',
                  background: "#1da1f2",
                  highlight: {
                    border: '#4dbd74',
                    background: '#20c997'
                  }
                }

              } else {
                tempItem['color'] = {
                  border: '#63218f',
                  background: "#833ab4",
                  highlight: {
                    border: '#4dbd74',
                    background: '#20c997'
                  }
                }

              }
              tempNodes.push(tempItem)
              tempNodesForSelect.push({ value: tempItem['id'], label: "(" + tempItem['type'] + " #" + tempItem['real_id'] + ") " + tempItem['name'] + " - " + tempItem['username'] })
            }
          })

          item.rels.forEach(item => {
            var element = tempLinks.find((element) => {
              return element.id == item.id;
            })
            if (element == null) {
              var tempItem = {}
              tempItem['id'] = item.id
              tempItem['from'] = item.start.id
              tempItem['to'] = item.end.id
              tempItem['label'] = item.label

              tempLinks.push(tempItem)
            }
          })

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

  componentDidMount() {
    this.setState({
      loading: true
    })

    // Get Network
    this.getBaseNetwork()

    this.setState({
      loading: false
    })
  }


  loading = () => <div className="fadeIn pt-1 text-center"><ReactLoading type={"cubes"} color="#1da1f2" /></div>


  // Graph methods //////////////////////////////////////////////////////////
  resetNetwork() {
    this.setState({ hideBots: false, hideLinks: false, hideUsers: false, botRoot: [], userRoot: [] })
    document.getElementById("hideBots").checked = false
    document.getElementById("hideUsers").checked = false
    document.getElementById("hideLinks").checked = false
    document.getElementById("botDepth").value = ""
    document.getElementById("userDepth").value = ""

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

    this.setState({
      loading: true
    })

    // Get Network
    this.getBaseNetwork()

    this.setState({
      loading: false
    })
  }

  searchNetwork() {
    if (this.state.botRoot.length == 0 && this.state.userRoot.length == 0 && document.getElementById("botDepth").value == "" && document.getElementById("userDepth").value == "") {
      this.resetNetwork()
    } else {
      this.setState({ hideBots: false, hideLinks: false, hideUsers: false, nodesForSelect: [], foundNode: '' })
      document.getElementById("hideBots").checked = false
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

      this.setState({
        loading: true
      })

      // Get Network
      var url = baseURL + "twitter/sub_network?"

      for (const [index, value] of this.state.botRoot.entries()) {

        var element = this.state.bots.find((element) => {
          return element.id == value.value;
        })
        url += "bots_id=" + element.real_id + "&"

      }

      if (document.getElementById("botDepth").value != "") {
        url += "bots_depth=" + document.getElementById("botDepth").value + "&"
      }


      for (const [index, value] of this.state.userRoot.entries()) {

        var element = this.state.users.find((element) => {
          return element.id == value.value;
        })

        url += "users_id=" + element.real_id + "&"

      }

      if (document.getElementById("userDepth").value != "") {
        url += "users_depth=" + document.getElementById("userDepth").value + "&"
      }

      url = url.replace(/.$/, "")
      this.getSubNetwork(url)

      this.setState({
        loading: false
      })
    }
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

  changeRootBot = (selectedOption) => {
    if (selectedOption != null) {
      this.setState({ botRoot: selectedOption });
    } else {
      this.setState({ botRoot: [] });
    }
  }
  changeRootUser = (selectedOption) => {
    if (selectedOption != null) {
      this.setState({ userRoot: selectedOption });
    } else {
      this.setState({ userRoot: [] });
    }
  }

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
        if (this.state.hideUsers) {
          this.setState({
            graph: {
              nodes: [],
              edges: this.state.allLinks
            }
          })
        } else {

          var tempArray = []
          this.state.allNodes.forEach(item => {
            if (item.type == "User") {
              tempArray.push(item)
            }
          })

          this.setState({
            graph: {
              nodes: tempArray,
              edges: this.state.allLinks
            }
          })
        }
      } else {
        if (this.state.hideUsers) {
          var tempArray = []
          this.state.allNodes.forEach(item => {
            if (item.type == "Bot") {
              tempArray.push(item)
            }
          })

          this.setState({
            graph: {
              nodes: tempArray,
              edges: this.state.allLinks
            }
          })
        } else {
          this.setState({
            graph: {
              nodes: this.state.allNodes,
              edges: this.state.allLinks
            }
          })
        }
      }

      this.state.graphRef.body.emitter.emit('_dataChanged')
      this.state.graphRef.redraw()
    })
  }

  hideUsers = () => {
    this.setState({ hideUsers: !this.state.hideUsers }, () => {
      if (this.state.hideUsers) {
        if (this.state.hideBots) {
          this.setState({
            graph: {
              nodes: [],
              edges: this.state.allLinks
            }
          })
        } else {
          var tempArray = []
          this.state.allNodes.forEach(item => {
            if (item.type == "Bot") {
              tempArray.push(item)
            }
          })

          this.setState({
            graph: {
              nodes: tempArray,
              edges: this.state.allLinks
            }
          })
        }
      } else {
        if (this.state.hideBots) {
          var tempArray = []
          this.state.allNodes.forEach(item => {
            if (item.type == "User") {
              tempArray.push(item)
            }
          })

          this.setState({
            graph: {
              nodes: tempArray,
              edges: this.state.allLinks
            }
          })
        } else {
          this.setState({
            graph: {
              nodes: this.state.allNodes,
              edges: this.state.allLinks
            }
          })
        }
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
  /////////////////////////////////////////////////////////////////////


  render() {
    const events = {
      doubleClick: function (event) {
        var { nodes, edges } = event;

        try {
          this.state.graphRef.selectNodes([nodes[0]])


          var element = this.state.graph.nodes.find((element) => {
            return element.id == nodes[0];
          })

          var type
          var info = null

          if (element.type == "Bot") {
            type = "BOT"
          } else if (element.type == "User") {
            this.openUserModal(element)

          } else {
            type = "TWEET"
          }

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

    var infoCard
    if (this.state.info) {
      infoCard =
        <Card>
          <CardHeader color="primary">
            <h3 style={{ color: "white" }}>
              <strong>Info</strong>
            </h3>
          </CardHeader>
          <CardBody>
            <p>No info has been selected</p>
          </CardBody>
        </Card>
    }


    var graph
    if (!this.state.loading) {
      graph = <Graph graph={this.state.graph} options={this.state.options} events={events} getNetwork={network => {
        this.setState({ graphRef: network })
      }} />
    } else {
      graph = <ReactLoading type={"cubes"} color="#1da1f2" />
    }

    var modal
    if (this.state.modal) {
      if (this.state.modalType == "USER") {
        modal =
          <Dialog class="fade-in"
            open={this.state.modal}
            onClose={() => this.handleClose()}
            aria-labelledby="alert-dialog-title"
            aria-describedby="alert-dialog-description"
          >
            <DialogTitle id="alert-dialog-title">
              <span>{"👤 Info on user "}</span><strong style={{ color: "#1da1f2" }}>{this.state.modalInfo.base.name}</strong><span style={{ color: "#999", fontSize: "15px" }}>{" (" + this.state.modalInfo.base.username + ")"}</span>
            </DialogTitle>
            <DialogContent style={{ minWidth: "600px" }}>
              <Container fluid>
                <CardAvatar profile>
                  <a onClick={e => e.preventDefault()}>
                    <img src={this.state.modalInfo.info.profile_image_url_https.replace("normal", "400x400")} alt="Profile Image" style={{ minWidth: "100px" }} />
                  </a>
                </CardAvatar>
                <Row>
                  <Col xs="12" md="12">
                    <Card profile>

                      <CardBody profile>
                        <h6 style={{
                          color: "#999",
                          margin: "0",
                          fontSize: "14px",
                          marginTop: "0",
                          paddingTop: "10px",
                          marginBottom: "0"
                        }}>@{this.state.modalInfo.info.screen_name}</h6>
                        <h4 style={{
                          color: "#3C4858",
                          marginTop: "0px",
                          minHeight: "auto",
                          fontWeight: "300",
                          marginBottom: "3px",
                          textDecoration: "none",
                          "& small": {
                            color: "#999",
                            fontWeight: "400",
                            lineHeight: "1"
                          }
                        }}>{this.state.modalInfo.info.name}</h4>
                        <h5 style={{ marginTop: "15px" }}>
                          <i>{this.state.modalInfo.info.description}</i>
                        </h5>

                        <div class="row" style={{ marginTop: "20px" }}>
                          <div class="col-sm-12 offset-md-3 col-md-3">
                            <h6><b>{this.state.modalInfo.info.followers_count}</b> following</h6>
                          </div>

                          <div class="col-sm-12 col-md-3">
                            <h6><b>{this.state.modalInfo.info.friends_count}</b> followers</h6>
                          </div>
                        </div>
                      </CardBody>
                      <CardFooter>
                        <h5><b style={{ color: "#4dbd74" }}>Active</b></h5>
                      </CardFooter>
                    </Card>
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
      } else if (this.state.modalType == "BOT") {
        modal =
          <Dialog class="fade-in"
            open={this.state.modal}
            onClose={() => this.handleClose()}
            aria-labelledby="alert-dialog-title"
            aria-describedby="alert-dialog-description"
          >
            <DialogTitle id="alert-dialog-title">
              <span>{"🤖 Info on bot "}</span><strong style={{ color: "#1da1f2" }}>{this.state.modalInfo.name}</strong><span style={{ color: "#999", fontSize: "15px" }}>{" (" + this.state.modalInfo.username + ")"}</span>
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
      } else if (this.state.modalType == "TWEET") {
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
                  {graph}
                </CardBody>
              </Card>
            </Col>
            <Col xs="12" sm="12" md="3">
              <Card>
                <CardHeader color="primary">
                  <h3 style={{ color: "white" }}>
                    <strong>Filters</strong>
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

                  <Row>
                    <Col md="12">
                      <h5 style={{ color: "#1fa8dd" }}><strong>Number of nodes per page</strong></h5>
                      <Row>
                        <Col md="9" sm="12" xm="12">
                          <FormGroup>
                            <Input type="text" id="name" placeholder="0" required />
                          </FormGroup>
                        </Col>
                        <Col md="3" sm="12" xm="12">
                          <Button block outline color="primary"

                          ><i class="fas fa-check"></i></Button>
                        </Col>

                      </Row>
                    </Col>
                  </Row>
                  <Row >
                    <Col md="12" style={{ zIndex: "0" }}>
                      <ReactPaginate
                        previousLabel={'<'}
                        nextLabel={'>'}
                        breakLabel={'...'}

                        pageCount={10}
                        marginPagesDisplayed={2}
                        pageRangeDisplayed={1}

                        breakClassName={'page-item'}
                        breakLinkClassName={'page-link'}
                        containerClassName={'pagination'}
                        pageClassName={'page-item'}
                        pageLinkClassName={'page-link'}
                        previousClassName={'page-item'}
                        previousLinkClassName={'page-link'}
                        nextClassName={'page-item'}
                        nextLinkClassName={'page-link'}
                        activeClassName={'active'}
                      />

                    </Col>
                  </Row>

                  <hr />

                  <Row style={{ marginTop: "20px" }}>
                    <Col md="4">
                      <FormGroup check>
                        <Input className="form-check-input" type="checkbox" id="hideBots" name="inline-checkbox1" onChange={this.hideBots} />
                        <Label className="form-check-label" check htmlFor="inline-checkbox1">Hide bots</Label>
                      </FormGroup>
                    </Col>
                    <Col md="4">
                      <FormGroup check>
                        <Input className="form-check-input" type="checkbox" id="hideUsers" name="inline-checkbox2" onChange={this.hideUsers} value="option2" />
                        <Label className="form-check-label" check htmlFor="inline-checkbox2">Hide users</Label>
                      </FormGroup>
                    </Col>
                    <Col md="4">
                      <FormGroup check>
                        <Input className="form-check-input" type="checkbox" id="hideLinks" name="inline-checkbox2" onChange={this.hideLinks} value="option2" />
                        <Label className="form-check-label" check htmlFor="inline-checkbox2">Hide links</Label>
                      </FormGroup>
                    </Col>
                  </Row>

                </CardBody>
              </Card>

              <Card>
                <CardHeader color="primary">
                  <h3 style={{ color: "white" }}>
                    <strong>Options</strong>
                  </h3>
                </CardHeader>
                <CardBody>
                  <Row style={{ marginBottom: "20px" }}>
                    <Col md="12">
                      <h5 style={{ color: "#1fa8dd" }}><strong>Bot root nodes</strong></h5>
                      <Select
                        defaultValue={[]}
                        isMulti
                        name="colors"
                        id="botRoot"
                        value={this.state.botRoot || ''}
                        options={this.state.botsForSelect}
                        className="basic-multi-select"
                        classNamePrefix="select"
                        onChange={this.changeRootBot}
                      />
                    </Col>
                  </Row>
                  <Row>
                    <Col md="12">
                      <FormGroup>
                        <Label htmlFor="name">Bot node depth</Label>
                        <Input type="text" id="botDepth" placeholder="0" />
                      </FormGroup>
                    </Col>
                  </Row>

                  <hr />

                  <Row style={{ marginBottom: "20px" }}>
                    <Col md="12">
                      <h5 style={{ color: "#1fa8dd" }}><strong>User root nodes</strong></h5>
                      <Select
                        defaultValue={[]}
                        isMulti
                        name="colors"
                        id="userRoot"
                        value={this.state.userRoot || ''}
                        options={this.state.usersForSelect}
                        className="basic-multi-select"
                        classNamePrefix="select"
                        onChange={this.changeRootUser}
                      />
                    </Col>
                  </Row>
                  <Row>
                    <Col md="12">
                      <FormGroup>
                        <Label htmlFor="name">User node depth</Label>
                        <Input type="text" id="userDepth" placeholder="0" />
                      </FormGroup>
                    </Col>
                  </Row>

                  <hr />

                  <Row style={{ marginTop: "25px" }}>
                    <Col md="6" style={{ alignItems: "center" }}>
                      <Button block outline color="danger"
                        onClick={() => this.resetNetwork()}
                      > Reset <i class="fas fa-times" style={{ marginLeft: "8px" }}></i></Button>
                    </Col>
                    <Col md="6">
                      <Button block outline color="success"
                        onClick={() => this.searchNetwork()}
                      > Search <i class="fas fa-search" style={{ marginLeft: "8px" }}></i></Button>
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

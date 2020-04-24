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
    loading: false,
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
        hierarchical: false
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
          gravitationalConstant: -12000,
          centralGravity: 0.6,
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
    bots: null,
    users: null,
    allLinks: null,

    modal: false,
    focusedUser: null,
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
            tempItem['label'] = item.properties.name
            tempItem['type'] = item.labels[0]

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
            } else {
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
            }

            tempNodes.push(tempItem)
            tempNodesForSelect.push({ value: tempItem['id'], label: "(" + tempItem['type'] + " #" + tempItem['real_id'] + ") " + tempItem['name'] + " - " + tempItem['username'] })
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
          bots: tempBots,
          users: tempUsers,
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
    this.setState({ hideBots: false, hideLinks: false, hideUsers: false })
    document.getElementById("hideBots").checked = false
    document.getElementById("hideUsers").checked = false
    document.getElementById("hideLinks").checked = false

    if (this.state.graphRef != null) {
      this.state.graphRef.selectNodes([])
      this.state.graphRef.moveTo({
        position: {x: 0, y: 0},
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

  /////////////////////////////////////////////////////////////////////


  // Select Methods //////////////////////////////////////////////////////////
  changeFindNode = (event) => {
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
          this.setState({
            graph: {
              nodes: this.state.users,
              edges: this.state.allLinks
            }
          })
        }
      } else {
        if (this.state.hideUsers) {
          this.setState({
            graph: {
              nodes: this.state.bots,
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
          this.setState({
            graph: {
              nodes: this.state.bots,
              edges: this.state.allLinks
            }
          })
        }
      } else {
        if (this.state.hideBots) {
          this.setState({
            graph: {
              nodes: this.state.users,
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
      focusedUser: null,
    });
  }

  /////////////////////////////////////////////////////////////////////


  render() {
    const events = {
      doubleClick: function (event) {
        var { nodes, edges } = event;
        this.state.graphRef.selectNodes([nodes[0]])

        console.log(nodes[0])

        this.setState({
          modal: true,
          focusedUser: this.state.graph.nodes.find((element) => {
            return element.id == nodes[0];
          })
        })
      }.bind(this),
      click: function (event) {
        var { nodes } = event;

        this.focus(nodes[0], {
          scale: 1.3,
          animation: {
            duration: 100,
            easingFunction: 'linear'
          }
        })

        this.moveTo({ position: this.getPositions([nodes[0]])[nodes[0]] })
      }
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
      modal = <Dialog class="fade-in"
        open={this.state.modal}
        onClose={() => this.handleClose()}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">
          <span>{"👤 Info on " + this.state.focusedUser.name}</span><span style={{ color: "#999" }}>{" (" + this.state.focusedUser.username + ")"}</span>
        </DialogTitle>
        <DialogContent style={{ minWidth: "600px" }}>
          <Container fluid>
            <Row>
              <Col xs="12" md="12">

              </Col>
            </Row>

            <DialogContentText>
              <span id="error" style={{ display: "None", color: "#f86c6b" }}>Sorry, the tweet can't be empty!</span>
            </DialogContentText>
          </Container>

        </DialogContent>
        <DialogActions>
          <Button onClick={() => this.handleClose()} color="info">
            Cancel
          </Button>
        </DialogActions>
      </Dialog>
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
                        options={this.state.botsForSelect}
                        className="basic-multi-select"
                        classNamePrefix="select"
                      />
                    </Col>
                  </Row>
                  <Row>
                    <Col md="12">
                      <FormGroup>
                        <Label htmlFor="name">Bot node depth</Label>
                        <Input type="text" id="name" placeholder="0" required />
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
                        options={this.state.usersForSelect}
                        className="basic-multi-select"
                        classNamePrefix="select"
                      />
                    </Col>
                  </Row>
                  <Row>
                    <Col md="12">
                      <FormGroup>
                        <Label htmlFor="name">User node depth</Label>
                        <Input type="text" id="name" placeholder="0" required />
                      </FormGroup>
                    </Col>
                  </Row>

                  <hr />

                  <Row style={{ marginTop: "25px" }}>
                    <Col md="6" style={{ alignItems: "center" }}>
                      <Button block outline color="danger"
                        onClick={() => this.resetNetwork()}
                      > Reset</Button>
                    </Col>
                    <Col md="6">
                      <Button block outline color="success"

                      > Search</Button>
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

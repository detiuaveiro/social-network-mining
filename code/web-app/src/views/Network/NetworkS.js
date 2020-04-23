import React, { Component } from 'react';

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

import { Graph } from "react-d3-graph";

class Network extends Component {
  constructor(props) {
    super(props);
  }

  state = {
    error: false,
    loading: false,
    info: false,
    infoNode: null,

    search: {
      specifiedBots: [],
      specifiedUsers: [],
      hideBots: false,
      hideUsers: false,
      hideRels: false
    },

    bots: [],
    users: [],

    modalType: null,
    modal: false,

    data: {
      nodes: [{ id: "oof" }],
      links: [],
      focusedNodeId: null
    },

    config: {
      "automaticRearrangeAfterDropNode": false,
      "collapsible": false,
      "directed": true,
      "focusAnimationDuration": 1,
      "focusZoom": 6,
      "height": 400,
      "highlightDegree": 1,
      "highlightOpacity": 0.3,
      "linkHighlightBehavior": false,
      "maxZoom": 8,
      "minZoom": 0.1,
      "nodeHighlightBehavior": true,
      "panAndZoom": false,
      "staticGraph": false,
      "staticGraphWithDragAndDrop": false,
      "d3": {
        "alphaTarget": 0.05,
        "gravity": -25,
        "linkLength": 100,
        "linkStrength": 1,
        "disableLinkForce": false
      },
      "node": {
        "color": "#1da1f2",
        "fontColor": "black",
        "fontSize": 8,
        "fontWeight": "bold",
        "highlightColor": "SAME",
        "highlightFontSize": 8,
        "highlightFontWeight": "normal",
        "highlightStrokeColor": "SAME",
        "highlightStrokeWidth": "SAME",
        "labelProperty": "name",
        "mouseCursor": "pointer",
        "opacity": 1,
        "renderLabel": true,
        "size": 200,
        "strokeColor": "none",
        "strokeWidth": 1.5,
        "svg": "",
        "symbolType": "circle"
      },
      "link": {
        "color": "#d3d3d3",
        "fontColor": "grey",
        "fontSize": 8,
        "fontWeight": "bold",
        "highlightColor": "#1da1f2",
        "highlightFontSize": 8,
        "highlightFontWeight": "normal",
        "labelProperty": "label",
        "mouseCursor": "pointer",
        "opacity": 1,
        "renderLabel": true,
        "semanticStrokeWidth": false,
        "strokeWidth": 1.5,
        "markerHeight": 6,
        "markerWidth": 6
      },

      "height": 700,
    }
  };

  decorateGraphNodesWithInitialPositioning = nodes => {
    return nodes.map(n =>
      Object.assign({}, n, {
        x: n.x || Math.floor(Math.random() * 500),
        y: n.y || Math.floor(Math.random() * 500),
      })
    );
  };

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
        console.log("oof")

        var tempNodes = []
        var tempLinks = []
        data.forEach(item => {
          if (item.type == "node") {
            var tempItem = {}
            tempItem['id'] = item.id
            tempItem['name'] = item.properties.name
            tempItem['real_id'] = item.properties.id
            tempItem['username'] = "@" + item.properties.username
            tempItem['type'] = item.labels[0]

            if (tempItem['type'] == "User") {
              tempItem['color'] = "#1da1f2"
            } else {
              tempItem['color'] = "#833ab4"
            }
            tempNodes.push(tempItem)
          } else {
            var tempItem = {}
            tempItem['id'] = item.id
            tempItem['source'] = item.start.id
            tempItem['target'] = item.end.id
            tempItem['label'] = item.label

            tempLinks.push(tempItem)
          }
        })

        this.setState({
          data: {
            nodes: tempNodes,
            links: tempLinks,
            focusedNodeId: this.state.data.focusedNodeId
          }
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
  onDoubleClickNode = id => {
    this.setState({
      data: {
        nodes: this.state.data.nodes,
        links: this.state.data.links,
        focusedNodeId: id
      }
    });
  };

  onClickNode = id => {
    this.setState({
      info: true,
      infoNode: id
    });
  };
  /////////////////////////////////////////////////////////////////////


  // Methods //////////////////////////////////////////////////////////
  handleOpenUsers() {
    this.setState({
      modalType: "USERS",
      modal: true
    });
  }

  handleClose() {
    this.setState({
      modalType: null,
      modal: false
    });
  }
  /////////////////////////////////////////////////////////////////////

  render() {
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

    var modal

    if (this.state.modalType == "USERS") {
      modal = <Dialog class="fade-in"
        open={this.state.modal}
        onClose={() => this.handleClose()}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">
          {"👤 Specify user root nodes"}
        </DialogTitle>
        <DialogContent style={{ minWidth: "600px" }}>
          <Container fluid>
            <Row>
              <Col xs="12" md="12">
                <Table style={{ paddingTop: "0px" }}
                  tableHeaderColor="primary"
                  tableHead={["User name", "Twitter tag", "Specified depth", ""]}
                  tableData={[["Posted Tweet", "Published a new tweet - #id", "24/24/24"], ["Posted Tweet", "Published a new tweet - #id", "24/24/24"], ["Posted Tweet", "Published a new tweet - #id", "24/24/24"], ["Posted Tweet", "Published a new tweet - #id", "24/24/24"], ["Posted Tweet", "Published a new tweet - #id", "24/24/24"], ["Posted Tweet", "Published a new tweet - #id", "24/24/24"]]}
                />
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
          <Button
            onClick={() => this.handleTweet()}
            color="success"
            autoFocus
          >
            Confirm
              </Button>
        </DialogActions>
      </Dialog>
    }
    var graph
    if (this.loading) {
      graph =
        <Graph
          id="graph-id"
          data={this.state.data}
          config={this.state.config}
          onClickNode={this.onClickNode}
          onDoubleClickNode={this.onDoubleClickNode}
        />
    } else {
      graph = <ReactLoading type={"cubes"} color="#1da1f2" />
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
                    <strong>Search filters</strong>
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
                        options={[{ value: 'chocolate', label: 'Chocolate' },
                        { value: 'strawberry', label: 'Strawberry' },
                        { value: 'vanilla', label: 'Vanilla' }]}
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
                        options={[{ value: 'chocolate', label: 'Chocolate' },
                        { value: 'strawberry', label: 'Strawberry' },
                        { value: 'vanilla', label: 'Vanilla' }]}
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

                  <Row style={{ marginTop: "20px" }}>
                    <Col md="4">
                      <FormGroup check>
                        <Input className="form-check-input" type="checkbox" id="inline-checkbox1" name="inline-checkbox1" value="option1" />
                        <Label className="form-check-label" check htmlFor="inline-checkbox1">Hide bots</Label>
                      </FormGroup>
                    </Col>
                    <Col md="4">
                      <FormGroup check>
                        <Input className="form-check-input" type="checkbox" id="inline-checkbox2" name="inline-checkbox2" value="option2" />
                        <Label className="form-check-label" check htmlFor="inline-checkbox2">Hide users</Label>
                      </FormGroup>
                    </Col>
                    <Col md="4">
                      <FormGroup check>
                        <Input className="form-check-input" type="checkbox" id="inline-checkbox2" name="inline-checkbox2" value="option2" />
                        <Label className="form-check-label" check htmlFor="inline-checkbox2">Hide links</Label>
                      </FormGroup>
                    </Col>
                  </Row>

                  <hr />

                  <Row style={{ marginTop: "25px" }}>
                    <Col md="6" style={{ alignItems: "center" }}>
                      <Button block outline color="danger"

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
        </Container>
        {modal}
      </div>
    );
  }
}

export default Network;

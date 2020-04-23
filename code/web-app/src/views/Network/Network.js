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
    graph: {
      nodes: [],
      edges: []
    },
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

      height: "895px",
    },
    events: {
      doubleClick: function (event) {
        var { nodes, edges } = event;
        console.log("Selected nodes:");
        console.log(nodes);
        console.log("Selected edges:");
        console.log(edges);
      },
      click: function (event) {
        var { nodes, edges } = event;

        this.focus(nodes[0], {
          scale: 1.3,
          animation: {
            duration: 100,
            easingFunction: 'linear'
          }
        })
      }
    }
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
            tempItem['label'] = item.properties.name
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
  handlePageClick = data => {
    let selected = data.selected;
    console.log(selected)
  };
  /////////////////////////////////////////////////////////////////////


  // Methods //////////////////////////////////////////////////////////

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


    var graph
    if (this.loading) {
      graph = <Graph graph={this.state.graph} options={this.state.options} events={this.state.events} id="graph" />
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
                    <strong>Filters</strong>
                  </h3>
                </CardHeader>
                <CardBody>
                  <Row style={{ marginBottom: "20px" }}>
                    <Col md="12">
                      <h5 style={{ color: "#1fa8dd" }}><strong>Find node</strong></h5>
                      <Select
                        defaultValue={[]}
                        name="colors"
                        options={[{ value: 'chocolate', label: 'Chocolate' },
                        { value: 'strawberry', label: 'Strawberry' },
                        { value: 'vanilla', label: 'Vanilla' }]}
                        className="basic-single"
                        classNamePrefix="select"
                      />
                    </Col>
                  </Row>

                  <hr />

                  <Row>
                    <Col md="12">
                      <h5 style={{ color: "#1fa8dd" }}><strong>Number of nodes per page</strong></h5>
                      <Row>
                        <Col md="8" sm="12" xm="12">
                          <FormGroup>
                            <Input type="text" id="name" placeholder="0" required />
                          </FormGroup>
                        </Col>
                        <Col md="4" sm="12" xm="12">
                          <Button block outline color="primary"

                          > Confirm</Button>
                        </Col>

                      </Row>



                    </Col>
                  </Row>
                  <Row>
                    <Col md="12">
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
      </div>
    );
  }
}

export default Network;

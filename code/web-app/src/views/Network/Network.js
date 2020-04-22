import React, { Component } from 'react';

import { Graph } from "react-d3-graph";

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

import Table from "../../components/Table/Table.js";

import { ToastContainer, toast, Flip } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import ReactLoading from "react-loading";

class Network extends Component {
  constructor(props) {
    super(props);
  }

  state = {
    error: false,
    loading: false,
    info: false,
    infoNode: null,

    data: {
      nodes: [{ id: "Harry", type: "bot" }, { id: "Sally", type: "bot" }, { id: "Alice", type: "user" }],
      links: [{ source: "Harry", target: "Sally", label: "oof" }, { source: "Harry", target: "Alice", label: "oof" }],
      focusedNodeId: "Harry"
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
        "gravity": -175,
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
        "labelProperty": "id",
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
                  <Graph
                    id="graph-id"
                    data={this.state.data}
                    config={this.state.config}
                    onClickNode={this.onClickNode}
                    onDoubleClickNode={this.onDoubleClickNode}
                  />
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
                  <Row>
                    <Table style={{ paddingTop: "0px" }}
                      tableHeaderColor="primary"
                      tableHead={["Log", "Description"]}
                      tableData={[["Posted Tweet", "Published a new tweet - #id", "24/24/24"], ["Posted Tweet", "Published a new tweet - #id", "24/24/24"], ["Posted Tweet", "Published a new tweet - #id", "24/24/24"], ["Posted Tweet", "Published a new tweet - #id", "24/24/24"], ["Posted Tweet", "Published a new tweet - #id", "24/24/24"], ["Posted Tweet", "Published a new tweet - #id", "24/24/24"]]}
                    />
                    <Pagination>
                      <PaginationItem>
                        <PaginationLink previous tag="button"></PaginationLink>
                      </PaginationItem>
                      <PaginationItem active>
                        <PaginationLink tag="button">1</PaginationLink>
                      </PaginationItem>
                      <PaginationItem>
                        <PaginationLink tag="button">2</PaginationLink>
                      </PaginationItem>
                      <PaginationItem>
                        <PaginationLink next tag="button"></PaginationLink>
                      </PaginationItem>
                    </Pagination>
                  </Row>
                  <Row>
                    <Col md="6">
                      <FormGroup check>
                        <Input className="form-check-input" type="checkbox" id="inline-checkbox1" name="inline-checkbox1" value="option1" />
                        <Label className="form-check-label" check htmlFor="inline-checkbox1">Hide bots</Label>
                      </FormGroup>
                    </Col>
                    <Col md="6">
                      <FormGroup check>
                        <Input className="form-check-input" type="checkbox" id="inline-checkbox2" name="inline-checkbox2" value="option2" />
                        <Label className="form-check-label" check htmlFor="inline-checkbox2">Hide users</Label>
                      </FormGroup>
                    </Col>
                  </Row>

                  <Row style={{ marginTop: "25px" }}>
                    <Col md="6" style={{ alignItems: "center" }}>
                      <Button
                        style={{ minWidth: "100%" }}
                        color="success"
                      >
                        Search
                    </Button>
                    </Col>
                    <Col md="6">
                      <Button style={{ minWidth: "100%" }}
                        color="info">
                        Reset
                  </Button>
                    </Col>
                  </Row>


                </CardBody>
              </Card>
              {infoCard}
            </Col>
          </Row>
        </Container>
      </div>
    );
  }
}

export default Network;

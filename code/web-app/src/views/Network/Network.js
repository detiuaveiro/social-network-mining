import React, { Component } from 'react';

import { Graph } from "react-d3-graph";

import { Container, Row, Col, Button } from 'reactstrap';
import Card from "../../components/Card/Card";
import CardHeader from "../../components/Card/CardHeader";
import CardBody from "../../components/Card/CardBody";

import Dialog from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogTitle from "@material-ui/core/DialogTitle";

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
    modal: false,
    modalType: null,
    modalNode: null,

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
      modal: true,
      modalType: "INFO",
      modalNode: id
    });
  };
  /////////////////////////////////////////////////////////////////////


  // Methods //////////////////////////////////////////////////////////
  handleClose() {
    this.setState({
      modal: false,
      modalType: null,
      modalNode: null
    });
  }
  /////////////////////////////////////////////////////////////////////

  render() {
    var modal
    if (this.state.modal) {
      if (this.state.modalType == "INFO") {
        modal = <Dialog class="fade-in"
          open={this.state.modal}
          onClose={() => this.handleClose()}
          aria-labelledby="alert-dialog-title"
          aria-describedby="alert-dialog-description"
        >
          <DialogTitle id="alert-dialog-title">
            {"👤 Info about " + this.state.modalNode}
          </DialogTitle>
          <DialogContent style={{ minWidth: "600px" }}>
            <Container fluid>
              <Row>
                <Col xs="12" md="12">
                  <DialogContentText>
                    <span id="error">Sorry, the tweet can't be empty!</span>
                  </DialogContentText>
                </Col>
              </Row>
            </Container>

          </DialogContent>
          <DialogActions>
            <Button onClick={() => this.handleClose()} color="info">
              Close
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
          </Row>
        </Container>
        {modal}
      </div>
    );
  }
}

export default Network;

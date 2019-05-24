import React from "react";
import {
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  CardTitle,
  Row,
  Col,
  Form,
  FormGroup,
  Label,
  Input,
  Modal, ModalHeader, ModalBody, ModalFooter,
  FormText
} from "reactstrap";

import { PanelHeader, DataTables, AddModal, Button } from "components";
import axios from "axios";

class Policies extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        modalTooltips: false,
    };
    this.toggleModalTooltips = this.toggleModalTooltips.bind(this);
  }
  toggleModalTooltips() {
    this.setState({
        modalTooltips: !this.state.modalTooltips
    });
  }

  clickAddPolicy(e) {
    this.modalRef.current.toggle();
  }

  savePolicy = (data) => {
    console.log(data);
    axios.post('/policies/add', data)
      .then(function (response) {
        console.log(response);
      })
  }

  render() {
    return (
      <div>
        <PanelHeader
          size="md"
          content={
            <div className="header text-center">
              <h2 className="title">Policies</h2>
            </div>
          }
        />
        <div className="content">
          <Row>
            <Col xs={12} md={12}>
              <Card className="card-tasks">
                <CardBody>
                  <DataTables ref={this.dataTablesRef} />
                </CardBody>
              </Card>
            </Col>
            <Col xs={12} md={12} className="text-right">
              <Button icon round color="primary" onClick={this.toggleModalTooltips} size="md" size="lg">
                <i class="fas fa-2x fa-plus"></i>
              </Button>
            </Col>
          </Row>
          <AddModal status={this.state.modalTooltips} handleClose={this.toggleModalTooltips} handleSave={this.savePolicy}></AddModal>
        </div>
      </div>
    );
  }
}

export default Policies;

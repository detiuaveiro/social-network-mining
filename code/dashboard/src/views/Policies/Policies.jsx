import React from "react";
import {
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  CardTitle,
  Row,
  Col,
  Button,
  Form,
  FormGroup,
  Label,
  Input,
  Modal, ModalHeader, ModalBody, ModalFooter,
  FormText
} from "reactstrap";

import { PanelHeader, DataTables } from "components";
import axios from "axios";

class Policies extends React.Component {

  constructor(props) {
    super(props);

    this.dataTablesRef = React.createRef();
    this.modalRef = React.createRef();

    this.clickAddPolicy = this.clickAddPolicy.bind(this);
    this.submitAddPolicy = this.submitAddPolicy.bind(this);
  }

  clickAddPolicy(e) {
    this.modalRef.current.toggle();
  }

  submitAddPolicy(policy) {
    console.log(policy);
    axios.post("/policies/add", { policy })
      .then(res => {
        console.log(res);
        this.modalRef.toggle();
        this.dataTablesRef.current.loadPolicies();
      });
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
                <CardHeader>
                  <CardTitle tag="h4">Policies</CardTitle>
                </CardHeader>
                <CardBody>
                  <DataTables ref={this.dataTablesRef} />
                </CardBody>
                <CardFooter>
                  <Row>
                    <Col sm={{ size: 1, offset: 11 }}>
                      <Button color="success" onClick={this.clickAddPolicy}>
                        <i className="now-ui-icons ui-1_simple-add"></i>
                      </Button>
                    </Col>
                  </Row>
                </CardFooter>
              </Card>
            </Col>
          </Row>
        </div>

        {/*The modals stay down here */}
        <AddPoliciesModal ref={this.modalRef} submitCallBack={this.submitAddPolicy}></AddPoliciesModal>
      </div>
    );
  }
}

class AddPoliciesModal extends React.Component {

  state = {
    modal: false,
    submitCallBack: this.props.submitCallBack !== undefined ? this.props.submitCallBack : function () { }
  };

  constructor(props) {
    super(props);

    this.toggle = this.toggle.bind(this);
    this.submitPolicy = this.submitPolicy.bind(this);
  }

  toggle() {
    this.setState(prevState => ({
      modal: !prevState.modal
    }));
  }

  submitPolicy(e) {
    let API_type = document.getElementById("api_type").value;
    let name = document.getElementById("name").value;
    let filter = document.getElementById("filter").value;
    let params = document.getElementById("params").value.split(",");

    let newPolicy = {
      API_type: API_type,
      name: name,
      filter: filter,
      params: params
    };

    this.toggle();
    this.props.submitCallBack(newPolicy);
  }

  render() {
    return (
      <Modal isOpen={this.state.modal} toggle={this.toggle}>
        <ModalHeader>Add Policy</ModalHeader>
        <ModalBody>
          <Form>
            <FormGroup row>
              <Label for="api_type" sm={2}>Social Network</Label>
              <Col sm={10}>
                <Input type="text" name="API_type" id="api_type" placeholder="Social Network to apply this filter" />
              </Col>
            </FormGroup>
            <FormGroup row>
              <Label for="name" sm={2}>Name</Label>
              <Col sm={10}>
                <Input type="text" name="name" id="name" placeholder="Name of the policy" />
              </Col>
            </FormGroup>
            <FormGroup row>
              <Label for="filter" sm={2}>Filter Type</Label>
              <Col sm={10}>
                <Input type="text" name="filter" id="filter" placeholder="Filter type" />
              </Col>
            </FormGroup>
            <FormGroup row>
              <Label for="params" sm={2}>Parameters</Label>
              <Col sm={10}>
                <Input type="text" name="params" id="params" placeholder="Parameters" />
              </Col>
            </FormGroup>
          </Form>
        </ModalBody>
        <ModalFooter>
          <Button color="primary" onClick={this.submitPolicy}>Add</Button>{' '}
          <Button color="secondary" onClick={this.toggle}>Cancel</Button>
        </ModalFooter>
      </Modal>
    );
  }
}

export default Policies;

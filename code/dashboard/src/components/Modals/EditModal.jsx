import React from "react";
import { Button, FormInputs, Radio } from 'components';
import TagsInput from 'react-tagsinput';
import{ Modal, ModalHeader, ModalBody, ModalFooter, Form, FormGroup, Label, Input, FormText, Col, Row } from 'reactstrap';
import PropTypes from "prop-types";

class EditModal extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        modalTooltips: props.status,
        name: "",
        social: "Twitter",
        filter: "Keywords",
        params: [],
    }
    this.handleTags = this.handleTags.bind(this);
    this.handleSave = this.handleSave.bind(this);
  }
  componentDidMount() {
    this.setState({
      modalTooltips: this.props.status
    })
  }

  componentDidUpdate(prevProps) {
    if (this.props.status !== prevProps.status) {
      this.setState({modalTooltips: this.props.status});
    }
  }

  handleTags(params) {
    this.setState({params});
    console.log("social: "+this.state.params)
  }

  handleName = event => {
    this.setState({ name : event.target.value });
    console.log("name: "+this.state.name)
  }

  handleSocial = event => {
    this.setState({social: event.target.value});
    console.log("name: "+this.state.social)
  }

  handleFilter = event => {
    this.setState({ filter : event.target.value });
    console.log("filter: "+this.state.filter)
  }
  
  handleUpdate() {
    const data = {API_type: this.state.social, name: this.state.name, filter: this.state.filter, params: this.state.params}
    this.props.handleUpdate(data)
  }

  render() {
    return (
      <Modal isOpen={this.state.modalTooltips} toggle={this.props.handleClose} size="lg">
        <ModalHeader className="justify-content-center" toggle={this.toggleModalTooltips}>
            Create Policy
        </ModalHeader>
        <ModalBody>
          <Form>
            <FormGroup required>
              <Label for="socialNetwork">Social Network:</Label>
              <Row>
                <FormGroup check className="form-check-radio"> 
                  <Label check>
                    <Input type="radio" name="social" value="Twitter" checked={this.state.social === 'Twitter'} onChange={this.handleSocial} />{' '}
                    <span className="form-check-sign" />
                    Twitter
                  </Label>
                </FormGroup>
                <FormGroup check className="form-check-radio"> 
                  <Label check>
                    <Input type="radio" name="social" value="Instagram" checked={this.state.social === 'Instagram'} onChange={this.handleSocial} />{' '}
                    <span className="form-check-sign" />
                    Instagram
                  </Label>
                </FormGroup>
              </Row>
            </FormGroup>
            <FormGroup required>
              <Label for="name">Name:</Label>
              <Input type="text" name="name" id="name" placeholder="e.g: Sports" value={this.state.name} onChange={this.handleName}/>
            </FormGroup>
            <FormGroup required>
              <Label for="filter">Filter:</Label>
              <Row>
                <FormGroup check className="form-check-radio"> 
                  <Label check>
                    <Input type="radio" name="filter" value="Keywords" checked={this.state.filter === 'Keywords'} onChange={this.handleFilter} />{' '}
                    <span className="form-check-sign" />
                    Keywords
                  </Label>
                </FormGroup>
                <FormGroup check className="form-check-radio"> 
                  <Label check>
                    <Input type="radio" name="filter" value="Targets" checked={this.state.filter === 'Targets'} onChange={this.handleFilter} />{' '}
                    <span className="form-check-sign" />
                    Targets
                  </Label>
                </FormGroup>
              </Row>
            </FormGroup>
            <FormGroup required>
              <Label for="filter">Parameters:</Label>
              <TagsInput
                value={this.state.params}
                onChange={this.handleTags}
                tagProps={{className: 'react-tagsinput-tag primary' }}
              />
            </FormGroup>
          </Form>
        </ModalBody>
        <ModalFooter>
            <Button color="secondary" onClick={this.props.handleClose}>
                Close
            </Button>
            <Button color="primary" onClick={this.handleUpdate}>
                Add
            </Button>
        </ModalFooter>
      </Modal>
    );
  }
}

EditModal.propTypes = {
  label: PropTypes.node
};

export default EditModal;

import React from "react";
import { Button} from 'components';
import Select from 'react-select';
import TagsInput from 'react-tagsinput';
import{ Modal, ModalHeader, ModalBody, ModalFooter, Form, FormText, FormGroup, Label, Input, Row } from 'reactstrap';
import PropTypes from "prop-types";

class EditModal extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        modalTooltips: props.status,
        id_policy: "",
        name: "",
        social: "Twitter",
        filter: "Keywords",
        params: [],
        bots: [],
        options: [],
        emptyName: false,
        emptyTags: false,
        emptyBots: false,
    }
    this.handleTags = this.handleTags.bind(this);
    this.handleUpdate = this.handleUpdate.bind(this);
    this.handleData = this.handleData.bind(this);
  }
  componentDidMount() {
    this.setState({
      modalTooltips: this.props.status,
      options: this.props.bots
    });
  }

  componentDidUpdate(prevProps) {
    if (this.props.status !== prevProps.status) {
      this.setState({modalTooltips: this.props.status});
    }
    if (this.props.bots !== prevProps.bots) {
      this.setState({options: this.props.bots});
    }
    if(this.props.info !== prevProps.info) {
      this.handleData()
    }
  }

  handleData() {
    const info = this.props.info[0];
    const bots = [];
    const avBots = this.state.options;
    info.bots.forEach(function (bot){
      avBots.forEach(function (opt) {
        if (opt.value === bot){
          bots.push({value: bot, label: opt.label})
        }
      })
    })
    this.setState({
      id_policy: info.id_policy,
      name: info.name,
      social: info.API_type,
      filter : info.filter,
      params : info.params,
      bots: bots,
    });
  }

  handleTags(params) {
    this.setState({params, emptyTags: false});
  }

  handleName = event => {
    this.setState({ name : event.target.value, emptyName: false });
  }

  handleSocial = event => {
    this.setState({social: event.target.value});
  }

  handleFilter = event => {
    this.setState({ filter : event.target.value, params: [] });
  }

  handleBots = (bots) => {
    this.setState({ bots, emptyBots: false});
  }
  
  handleUpdate() {
    if (this.state.name===""){
      this.setState({emptyName: true})
    }
    else if (this.state.params.length===0){
      this.setState({emptyTags: true})
    }
    else if (this.state.bots.length===0){
      this.setState({emptyBots: true})
    }
    else {
      const b = []
      this.state.bots.forEach(function (bot){
        b.push(bot['value'])
      })
      const data = {id_policy: this.state.id_policy, API_type: this.state.social, name: this.state.name, filter: this.state.filter, params: this.state.params, bots: b};
      this.props.handleUpdate(data)
    }
  }

  render() {
    return (
      <Modal isOpen={this.state.modalTooltips} toggle={this.props.handleClose} size="lg">
        <ModalHeader className="justify-content-center" toggle={this.toggleModalTooltips}>
            Edit Policy
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
              <div hidden={!this.state.emptyName} className="alert-danger mt-2 p-2" style={{borderRadius: 30}}>
                  Field can't be empty!
              </div>
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
                    <Input type="radio" name="filter" value="Target" checked={this.state.filter === 'Target'} onChange={this.handleFilter} />{' '}
                    <span className="form-check-sign" />
                    Username
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
                maxTags={this.state.filter==="Target" ? "1" : "-1" }
              />
              <div hidden={!this.state.emptyTags} className="alert-danger mt-2 p-2" style={{borderRadius: 30}}>
                  Field can't be empty!
              </div>
              <FormText>If you choose filter "Username" add one Username only.</FormText>
            </FormGroup>
            <FormGroup required>
              <Label>Bots:</Label>
              <Select
                  value={this.state.bots}
                  onChange={this.handleBots}
                  options={this.state.options}
                  isMulti
                  isSearchable
                  placeholder="Add Bots"
                  styles={{
                    control: (provided,state) => ({
                      ...provided,
                      borderRadius: 30,
                      borderColor: state.isFocused ? "#f96332" : "#E3E3E3",
                      boxShadow: state.isFocused ? "#f96332" : "#E3E3E3",
                      '&:hover': {
                        borderColor: state.isFocused ? "#f96332" : "#E3E3E3",
                        boxShadow: state.isFocused ? "#f96332" : "#E3E3E3",
                      },
                    }),
                    multiValue: (provided, state) => ({
                      ...provided,
                      backgroundColor: "#f96332",
                      color: "white",
                      borderRadius: 30,
                    }),
                  }}
                  className="primary"

                />
              <div hidden={!this.state.emptyBots} className="alert-danger mt-2 p-2" style={{borderRadius: 30}}>
                 Field can't be empty!
              </div>
            </FormGroup>
          </Form>
        </ModalBody>
        <ModalFooter>
            <Button color="secondary" onClick={this.props.handleClose}>
                Close
            </Button>
            <Button color="primary" onClick={this.handleUpdate}>
                Update
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

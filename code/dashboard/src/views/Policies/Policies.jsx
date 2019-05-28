import React from "react";
import {
  Row,
  Col,
} from "reactstrap";
import NotificationAlert from "react-notification-alert";
import { PanelHeader, AddModal, EditModal, Button, PoliciesTable } from "components";
import axios from "axios";

class Policies extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        modalAdd: false,
        modalEdit: false,
        policies: [],
        editTools:[]
    };
    this.toggleModalAdd = this.toggleModalAdd.bind(this);
    this.toggleModalEdit = this.toggleModalEdit.bind(this);
    this.savePolicy = this.savePolicy.bind(this);
    this.editPolicy = this.editPolicy.bind(this);
    this.updatePolicy = this.updatePolicy.bind(this);
    this.activatePolicy = this.activatePolicy.bind(this);
    this.removePolicy = this.removePolicy.bind(this);
    this.notify = this.notify.bind(this);
    this.refresh = this.refresh.bind(this);
  }

  componentDidMount(){
    axios.get('http://192.168.85.182:5000/policies')
    .then(res => {
        const policies = res.data;
        this.setState({ policies });
   });
  }

  toggleModalAdd() {
    this.setState({
        modalAdd: !this.state.modalAdd
    });
  }

  toggleModalEdit() {
    this.setState({
        modalEdit: !this.state.modalEdit
    });
  }

  notify = (msg) => {
    var type = "primary";
    var options = {};
    options = {
      place: "tc",
      message: (
        <div>
          <div>
            {msg}
          </div>
        </div>
      ),
      type: type,
      icon: "now-ui-icons ui-1_bell-53",
      autoDismiss: 7
    };
    this.refs.notificationAlert.notificationAlert(options);
  }

  refresh(tipo,msg){
    console.log(tipo)
    switch(tipo){
      case "ADD":
        this.toggleModalAdd()
        this.notify("Policy Added with "+msg)
        this.componentDidMount()
        break
      case "REMOVE":
        this.notify("Policy Removed with "+msg)
        this.componentDidMount()
        break
      case "EDIT":
        this.toggleModalEdit()
        this.notify("Policy Edited with "+msg)
        this.componentDidMount()
        break
      case "ERROR":
        this.notify("ERROR: "+msg)
        this.componentDidMount()
        break
    }
  }

  savePolicy(data) {
    axios.post('http://192.168.85.182:5000/policies/add', data)
      .then((response) => {
        this.refresh(response.status==200 ? "ADD" : "ERROR",response.data['Message'])
      })
  }

  removePolicy(id) {
    axios.delete('http://192.168.85.182:5000/policies/remove/'+id)
        .then(response => {
          this.refresh(response.status==200 ? "REMOVE" : "ERROR",response.data['Message'])
        });
  }

  editPolicy(id) {
    console.log(this.state.modalEdit)
    this.setState({
      modalEdit: !this.state.modalEdit
    });
    axios.get('http://192.168.85.182:5000/policies/'+id)
    .then(res => {
        const editTools = res.data;
        this.setState({ editTools });
   });
  }


  updatePolicy(data) {
    console.log(data);
    axios.post('http://192.168.85.182:5000/policies/update', data)
        .then(response => {
          this.refresh(response.status==200 ? "EDIT" : "ERROR",response.data['Message'])
        });
  }

  activatePolicy(id,state) {
    console.log(id)
    console.log(state.state.value);
    const data = {id_policy: id, active: ""+state.state.value}
    axios.post('http://localhost:5000/policies/update', data)
        .then(response => {
          this.refresh(response.status==200 ? "REMOVE" : "ERROR",response.data['Message'])
        });
  }

  render() {
    return (
      <div>
        <NotificationAlert ref="notificationAlert" />
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
              <PoliciesTable dados={this.state.policies} remove={this.removePolicy} edit={this.editPolicy} activate={this.activatePolicy}/>
            </Col>
            <Col xs={12} md={12} className="text-right">
              <Button icon round color="primary" onClick={this.toggleModalAdd} size="md" size="lg">
                <i class="fas fa-2x fa-plus"></i>
              </Button>
            </Col>
          </Row>
          <AddModal status={this.state.modalAdd} handleClose={this.toggleModalAdd} handleSave={this.savePolicy}></AddModal>
          <EditModal status={this.state.modalEdit} handleClose={this.toggleModalEdit} handleUpdate={this.updatePolicy} info={this.state.editTools}></EditModal>
        </div>
      </div>
    );
  }
}

export default Policies;

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
        modalTooltips: false,
        policies: []
    };
    this.toggleModalTooltips = this.toggleModalTooltips.bind(this);
    this.savePolicy = this.savePolicy.bind(this);
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

  toggleModalTooltips() {
    this.setState({
        modalTooltips: !this.state.modalTooltips
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
        this.toggleModalTooltips()
        this.notify("Policy Added with "+msg)
        this.componentDidMount()
        break
      case "REMOVE":
        this.notify("Policy Removed with "+msg)
        this.componentDidMount()
        break
      case "EDIT":
        this.toggleModalTooltips()
        this.notify("Policy Edited with "+msg)
        this.componentDidMount()
        break
      case "ERROR":
        this.toggleModalTooltips()
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

  updatePolicy(id) {
    //EXEMPLO
    axios.delete('http://192.168.85.182:5000/policies/remove/'+id)
        .then(response => {
          this.refresh(response.status==200 ? "REMOVE" : "ERROR",response.data['Message'])
        });
  }

  activatePolicy(id) {
    //EXEMPLO
    axios.delete('http://192.168.85.182:5000/policies/remove/'+id)
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
              <Button icon round color="primary" onClick={this.toggleModalTooltips} size="md" size="lg">
                <i class="fas fa-2x fa-plus"></i>
              </Button>
            </Col>
          </Row>
          <AddModal status={this.state.modalTooltips} handleClose={this.toggleModalTooltips} handleSave={this.savePolicy}></AddModal>
          <EditModal status={this.state.modalTooltips} handleClose={this.toggleModalTooltips} handleUpdate={this.updatePolicy}></EditModal>
        </div>
      </div>
    );
  }
}

export default Policies;

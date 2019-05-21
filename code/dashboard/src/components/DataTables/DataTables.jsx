import React from "react";
// react component for creating dynamic tables

// core components
import { Button, Checkbox } from "components";
import {
    Row,
    Col,
    Table,
    Form,
    FormGroup,
    Label,
    Input,
    Modal, ModalHeader, ModalBody, ModalFooter,
} from "reactstrap";

import axios from 'axios';

class ReactTables extends React.Component {
    /*
     */
    state = {
        policies: []
    };
    /**
     * [
     *   {
     *     name : "Example name",
     *     API_type : "Twitter",
     *     filter : "keywords",
     *     params : ["keyword1","keyword2","keyword3"],
     *     id_policy : "something"
     *     target : "..."
     *   }
     * ]
     */
    constructor(props) {
        super(props);

        this.modalRef = React.createRef();

        this.clickRemovePolicy = this.clickRemovePolicy.bind(this);
        this.clickEditPolicy = this.clickEditPolicy.bind(this);
        this.loadPolicies = this.loadPolicies.bind(this);
    }

    componentDidMount() {
        this.loadPolicies();
    }

    loadPolicies() {
        axios.get('/policies')
             .then(res => {
                const policies = res.data;
                this.setState({ policies });
                console.log(policies);
            });
    }

    updatePolicy(policy) {
        axios.post("/policies/update", { policy })
            .then(
                res => {
                    console.log(res);
                    this.loadPolicies();
                }
            );
    }

    clickRemovePolicy(e) {
        let id = e.currentTarget.parentElement.parentElement.id;
        console.log(id);
        axios.delete('/policies/remove/' + id)
            .then(res => {
                console.log(res);
                this.loadPolicies();
            });
    }

    clickEditPolicy(e) {
        let index = parseInt(e.currentTarget.parentElement.parentElement.dataset.index);
        let policy = this.state.policies[index];
        console.log(policy);

        this.modalRef.current.setPolicy(policy);
        this.modalRef.current.toggle();
    }

    render() {
        return (
            <div>
                <Table responsive striped>
                    <thead className="text-primary">
                        <tr>
                            <th className="text-center">#</th>
                            <th className="text-center"></th>
                            <th>Policy Name</th>
                            <th>Social Network</th>
                            <th className="text-center">Filter</th>
                            <th className="text-right">Params</th>
                            <th className="text-right">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {this.state.policies.map(function (policy, index) {
                            return (<tr id={policy.id_policy} key={index.toString()} data-index={index}>
                                <td className="text-center">{index + 1}</td>
                                <td className="text-center">
                                    <Checkbox />
                                </td>
                                <td>{policy.name}</td>
                                <td>{policy.API_type}</td>
                                <td className="text-center">{policy.filter}</td>
                                <td className="text-right">{policy.params.join()}</td>
                                <td className="text-right">
                                    <Button icon neutral color="success" size="sm" onClick={this.clickEditPolicy}>
                                        <i className="now-ui-icons ui-2_settings-90"></i>
                                    </Button>{` `}
                                    <Button icon neutral color="danger" size="sm" onClick={this.clickRemovePolicy}>
                                        <i className="now-ui-icons ui-1_simple-remove"></i>
                                    </Button>{` `}
                                </td>
                            </tr>);
                        }.bind(this))}
                    </tbody>
                </Table>
                <EditPoliciesModal ref={this.modalRef} modal={this.state.edit_mode} submitCallBack={this.updatePolicy} ></EditPoliciesModal>
            </div>
        );
    }
}

class EditPoliciesModal extends React.Component {

    state = {
        modal: this.props.modal !== undefined ? this.props.modal : false,
        policy: this.props.policy !== undefined ? this.props.policy : {
            params: []
        }
    }

    constructor(props) {
        super(props);

        this.toggle = this.toggle.bind(this);
        this.submitUpdatePolicy = this.submitUpdatePolicy.bind(this);
    }

    toggle() {
        this.setState(prevState => ({
            modal: !prevState.modal
        }));
    }

    setPolicy(policy) {
        this.setState({
            policy: policy
        });
    }

    submitUpdatePolicy() {
        let API_type = document.getElementById("api_type").value;
        let name = document.getElementById("name").value;
        let filter = document.getElementById("filter").value;
        let params = document.getElementById("params").value.split(",");

        let updateMessage = {
            id_policy: this.state.policy.id_policy,
            API_type: API_type,
            name: name,
            filter: filter,
            params: params
        };

        this.toggle();
        if (this.props.submitCallBack) { this.props.submitCallBack(updateMessage); }
    }

    render() {
        return (
            <div>
                <Modal isOpen={this.state.modal} toggle={this.toggle} className={this.props.className}>
                    <ModalHeader>Edit Policy</ModalHeader>
                    <ModalBody>
                        <Form>
                            <FormGroup row>
                                <Label for="api_type" sm={2}>Social Network</Label>
                                <Col sm={10}>
                                    <Input type="text" name="API_type" id="api_type" placeholder="Social Network to apply this filter" defaultValue={this.state.policy.API_type} />
                                </Col>
                            </FormGroup>
                            <FormGroup row>
                                <Label for="name" sm={2}>Name</Label>
                                <Col sm={10}>
                                    <Input type="text" name="name" id="name" placeholder="Name of the policy" defaultValue={this.state.policy.name} />
                                </Col>
                            </FormGroup>
                            <FormGroup row>
                                <Label for="filter" sm={2}>Filter Type</Label>
                                <Col sm={10}>
                                    <Input type="text" name="filter" id="filter" placeholder="Filter type" defaultValue={this.state.policy.filter} />
                                </Col>
                            </FormGroup>
                            <FormGroup row>
                                <Label for="params" sm={2}>Parameters</Label>
                                <Col sm={10}>
                                    <Input type="text" name="params" id="params" placeholder="Parameters" defaultValue={this.state.policy.params.join()} />
                                </Col>
                            </FormGroup>
                        </Form>
                    </ModalBody>
                    <ModalFooter>
                        <Button color="primary" onClick={this.submitUpdatePolicy}>Update</Button>{' '}
                        <Button color="secondary" onClick={this.toggle}>Cancel</Button>
                    </ModalFooter>
                </Modal>
            </div>
        );
    }
}

export default ReactTables;
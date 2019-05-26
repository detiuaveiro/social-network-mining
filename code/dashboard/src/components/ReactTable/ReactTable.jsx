import React from "react";
// react component for creating dynamic tables
import ReactTable from 'react-table'

// core components
import { Button, Checkbox } from "components";
import {
    Card,
    CardBody,
    Col,
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
        logger: [],
        colums: [ {
            Header: 'Time',
            accessor: 'timestamp',
            style: {
                height: "50px"
            }
          }, {
            Header: 'Action',
            accessor: 'action',
            style: {
                height: "50px"
            }
          }],
        user_id: this.props.userid
    };

    constructor(props) {
        super(props);

    }

    componentDidMount() {
        const url = '/twitter/bots/'+this.state.user_id+'/logs'
        console.log(url)
        axios.get('/twitter/bots/'+this.state.user_id+'/logs')
        .then(res => {
           console.log(res.data)
           const logs = res.data;
           const logger = []
           for(var log in logs) {
                logger.push(logs[log])
           }
           this.setState({ logger });
       });
    }

    render() {
        return (
            <Card>
                <CardBody>
                    <ReactTable
                        data={this.state.logger}
                        columns={this.state.colums}
                        defaultPageSize={10}
                        showPaginationTop
                        showPaginationBottom={false}
                        resizable={false}
                        className="-striped -highlight"
                    />
                </CardBody>
            </Card>
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

        /**
         * API_type: API_type,
            name: name,
            filter: filter,
            params: params
         */
        let updateMessage = {
            id_policy: this.state.policy.id_policy
        };

        //Add the fields that need to be updated
        if(this.state.policy.API_type !== API_type) updateMessage["API_type"] = API_type;
        if(this.state.policy.name !== name) updateMessage["name"] = name;
        if(this.state.policy.filter !== filter) updateMessage["filter"] = filter;
        if(!params.length === this.state.policy.params.length || !params.every(function(ele) {
            return this.state.policy.params.contains(ele);
        })) updateMessage["API_type"] = API_type; 

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
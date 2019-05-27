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

class PoliciesTable extends React.Component {
    /*
     */
    state = {
        policies: [],
        colums: [
            {
                Header: 'ID',
                accessor: 'id_policy',
                width: 60,
                style: {
                    height: "50px",
                }
            }, {
                Header: 'Name',
                accessor: 'name',
                width: 140,
                style: {
                    height: "50px"
                }
            }, {
                Header: 'API',
                accessor: 'API_type',
                width: 140,
                style: {
                    height: "50px"
                }
            }, {
                Header: 'Filter',
                accessor: 'filter',
                width: 140,
                style: {
                    height: "50px"
                }
            }, {
                Header: 'Paramaters',
                accessor: 'params',
                sortable: false,
                filterable: false,
                style: {
                    height: "50px"
                }
            }],
    };

    componentDidMount() {
        console.log('/policies/bots/'+this.props.userid)
        axios.get('/policies/bots/'+this.props.userid)
        .then(res => {
           console.log(res.data)
           const policies = res.data;
           this.setState({ policies });
       });
    }

    render() {
        return (
            <Card>
                <CardBody>
                    <ReactTable
                        data={this.state.policies}
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

export default PoliciesTable;
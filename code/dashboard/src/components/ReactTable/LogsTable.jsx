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

class LogsTable extends React.Component {
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

export default LogsTable;
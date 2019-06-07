import React from "react";
// react component for creating dynamic tables
import ReactTable from 'react-table'

// core components
import {
    Card,
    CardBody,
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
    
    componentDidMount() {
        const url = 'http://192.168.85.182:5000/twitter/bots/'+this.state.user_id+'/logs'
        axios.get('http://192.168.85.182:5000/twitter/bots/'+this.state.user_id+'/logs')
        .then(res => {
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
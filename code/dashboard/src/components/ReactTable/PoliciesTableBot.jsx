import React from "react";
// react component for creating dynamic tables
import ReactTable from 'react-table'

import {
    Card,
    CardBody,
} from "reactstrap";

import axios from 'axios';

class PoliciesTableBot extends React.Component {
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
                filterable: true,
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
        axios.get('http://192.168.85.182:5000/policies/bots/'+this.props.userid)
        .then(res => {
           const policies = res.data;
           this.setState({ policies });
       });
    }

    render() {
        return (
            <Card>
                <CardBody>
                    <ReactTable
                        data={this.state.policies.map(policie => {
                            return({
                            id_policy: policie['id_policy'],
                            name: policie['name'],
                            API_type: policie['API_type'],
                            filter: policie['filter'],
                            params: policie['params'].join(", "),
                            })
                        })}
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

export default PoliciesTableBot;
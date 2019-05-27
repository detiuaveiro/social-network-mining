import React from "react";
// react component for creating dynamic tables
import ReactTable from 'react-table'
import Button from "components/CustomButton/CustomButton.jsx";
// core components
import {
    Card,
    CardBody,
} from "reactstrap";

class PoliciesTable extends React.Component {

    componentDidMount() {
        console.log(this.props.dados)
        this.setState({policies: this.props.dados})
    }

    componentDidUpdate(prevProps) {
        if (this.props.dados !== prevProps.dados) {
            this.setState({policies: this.props.dados});
        }
    }

    state = {
        policies: this.props.dados,
        colums: [
            {
                Header: 'ID',
                accessor: 'id_policy',
                width: 60,
                style: {
                    "text-align": "center",
                    height: "50px",
                }
            }, {
                Header: 'Name',
                accessor: 'name',
                style: {
                    "text-align": "center",
                    height: "50px"
                }
            }, {
                Header: 'API',
                accessor: 'API_type',
                style: {
                    "text-align": "center",
                    height: "50px"
                }
            }, {
                Header: 'Filter',
                accessor: 'filter',
                style: {
                    "text-align": "center",
                    height: "50px"
                }
            }, {
                Header: 'Paramaters',
                accessor: 'params',
                sortable: false,
                filterable: false,
                style: {
                    height: "50px"
                },
            }, {
                Header: 'Actions',
                accessor: 'actions',
                sortable: false,
                filterable: false,
                style: {
                    height: "50px"
                },
            }],
    };

    handleRemove = (id) => {
        this.props.remove(id)
    }

    handleEdit = (id) => {
        this.props.edit(id)
    }

    handleActivate = (id) => {
        this.props.activate(id)
    }

    render() {
        return (
            <Card>
                <CardBody>
                    <ReactTable
                        data={
                            this.state.policies.map(policie => {
                                return({
                                    id_policy: policie['id_policy'],
                                    name: policie['name'],
                                    API_type: policie['API_type'],
                                    filter: policie['filter'],
                                    params: policie['params'],
                                    actions: (
                                        <div className="actions-center">
                                          <Button
                                            onClick={() => this.handleActivate(policie['id_policy'])}
                                            color="info"
                                            size="sm"
                                            round
                                            icon
                                          >
                                            {
                                                policie['active'] ? <i class="fas fa-check-circle"></i> : <i class="fas fa-circle"></i>
                                            }
                                          </Button>{" "}
                                          <Button
                                            onClick={() => this.handleEdit(policie['id_policy'])}
                                            color="warning"
                                            size="sm"
                                            round
                                            icon
                                          >
                                            <i className="fa fa-edit" />
                                          </Button>{" "}
                                          <Button
                                            onClick={() => this.handleRemove(policie['id_policy'])}
                                            color="danger"
                                            size="sm"
                                            round
                                            icon
                                          >
                                            <i class="fas fa-trash-alt"></i>
                                          </Button>{" "}
                                        </div>
                                      ),
                                })
                            })
                        }
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
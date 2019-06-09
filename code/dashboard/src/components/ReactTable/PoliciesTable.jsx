import React from "react";
// react component for creating dynamic tables
import ReactTable from 'react-table'
import Switch from 'react-bootstrap-switch';
import Button from "components/CustomButton/CustomButton.jsx";
// core components
import {
    Card,
    CardBody,
} from "reactstrap";

class PoliciesTable extends React.Component {

    componentDidMount() {
        this.setState({
            policies: this.props.dados,
            bots: this.props.bots
        })
    }

    componentDidUpdate(prevProps) {
        if (this.props.dados !== prevProps.dados) {
            this.setState({policies: this.props.dados});
        }
        if (this.props.bots !== prevProps.bots) {
            this.setState({bots: this.props.bots});
        }
    }

    state = {
        bots: this.props.bots,
        policies: this.props.dados,
        colums: [
            {
                Header: 'ID',
                accessor: 'id_policy',
                width: 60,
                style: {
                    textAlign: "center",
                    height: "50px",
                }
            }, {
                Header: 'Status',
                accessor: 'status',
                sortable: false,
                filterable: false,
                width: 90,
                style: {
                    textAlign: "center",
                    height: "50px"
                }
            }, {
                Header: 'Name',
                accessor: 'name',
                width: 150,
                style: {
                    textAlign: "center",
                    height: "50px"
                }
            }, {
                Header: 'API',
                accessor: 'API_type',
                width: 100,
                style: {
                    textAlign: "center",
                    height: "50px"
                }
            }, {
                Header: 'Filter',
                accessor: 'filter',
                width: 100,
                style: {
                    textAlign: "center",
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
                Header: 'Bots',
                accessor: 'bots',
                sortable: false,
                filterable: false,
                style: {
                    height: "50px"
                },
            }, {
                Header: 'Actions',
                accessor: 'actions',
                width: 150,
                sortable: false,
                filterable: false,
            }],
    };

    handleRemove = (id) => {
        this.props.remove(id)
    }

    handleEdit = (id) => {
        this.props.edit(id)
    }

    handleActivate = (id,state) => {
        this.props.activate(id,state)
    }

    render() {
        return (
            <Card>
                <CardBody>
                    <ReactTable
                        data={
                            this.state.policies.map(policie => {
                                const new_bots = []
                                policie['bots'].forEach(botid => {
                                    this.state.bots.forEach(bot => {
                                        if (bot.value === botid){
                                          new_bots.push(bot.label)
                                        }
                                      })
                                });
                                return({
                                    id_policy: policie['id_policy'],
                                    status: (
                                        <div className="actions-center">
                                            <Switch
                                                onChange={(state) => this.handleActivate(policie['id_policy'],state)}
                                                defaultValue={policie['active']}
                                                onColor="brown"
                                            />{" "}
                                        </div>
                                      ),
                                    name: policie['name'],
                                    API_type: policie['API_type'],
                                    filter: policie['filter'],
                                    params: policie['params'].join(", "),
                                    bots: new_bots.join(", "),
                                    actions: (
                                        <div className="actions-center">
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
import React from "react";
// react component for creating dynamic tables

// core components
import { Button, Checkbox } from "components";
import {
    Table
} from "reactstrap";

import axios from 'axios';

class ReactTables extends React.Component {
    state = {
        policies: this.props.policies
    };
    /**
     * [
     *   {
     *     policy_name : "Example name",
     *     social_network : "Twitter",
     *     filter : "keywords",
     *     params : ["keyword1","keyword2","keyword3"],
     *     target : "target1"
     *   }
     * ]
     */
    constructor(props) {
        super(props);
        this.clickRemovePolicy = this.clickRemovePolicy.bind(this);
        this.clickEditPolicy = this.clickEditPolicy.bind(this);
    }

    componentDidMount() {
        this.updatePolicies();
    }

    /**
     * @typedef {Object} Policy
     * @property {string} name
     * @property {string} social_network
     * @property {string} filter
     * @property {string[]} params
     * @property {string} target
     * @param {Policy} policy 
     */
    addPolicy(policy) {
        this.state.policies.push(policy);
        this.forceUpdate();
    }

    updatePolicies() {
        axios.get('/policies')
             .then(res => {
                const policies = res.policies;
                this.setState({policies});
                console.log(policies);
        });
    }

    clickRemovePolicy(e) {
        
    }

    clickEditPolicy(e) {
        
    }

    render() {
        return (
            <div>
                <Table responsive striped size>
                    <thead className="text-primary">
                        <tr>
                            <th className="text-center">#</th>
                            <th className="text-center"></th>
                            <th>Policy Name</th>
                            <th>Social Network</th>
                            <th className="text-center">Filter</th>
                            <th className="text-right">Params</th>
                            <th className="text-right">Target</th>
                            <th className="text-right">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {this.state.policies.map(function (policy,index) {
                            return (<tr>
                                <td className="text-center">{index}</td>
                                <td className="text-center">
                                    <Checkbox />
                                </td>
                                <td>{policy.name}</td>
                                <td>{policy.social_network}</td>
                                <td className="text-center">{policy.filter}</td>
                                <td className="text-right">{policy.params.join()}</td>
                                <td className="text-right">{policy.target}</td>
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
            </div>
        );
    }
}
export default ReactTables;
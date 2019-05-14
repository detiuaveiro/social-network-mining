import React from "react";
// react component for creating dynamic tables

// core components
import { Button, Checkbox } from "components";
import {
    Table
} from "reactstrap";

class ReactTables extends React.Component {

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

        this.state = { policies: props.policies };
    }

    componentDidMount() {
        setTimeout(function() {
            var restData = [{
                name: "Futebol",
                social_network: "Twitter",
                filter: "keywords",
                params: ["keyword1","keyword2","keyword3"],
                target : "target1"
              }];
            for(let policy of restData) {
                this.addPolicy(policy);
            }
        }.bind(this));
    }

    clickShowAddModal() {

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

    clickRemovePolicy() {

    }

    clickEditPolicy() {

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
                                    <Button icon neutral color="success" size="sm">
                                        <i className="now-ui-icons ui-2_settings-90"></i>
                                    </Button>{` `}
                                    <Button icon neutral color="danger" size="sm">
                                        <i className="now-ui-icons ui-1_simple-remove"></i>
                                    </Button>{` `}
                                </td>
                            </tr>);
                        })}
                    </tbody>
                </Table>
            </div>
        );
    }
}
export default ReactTables;
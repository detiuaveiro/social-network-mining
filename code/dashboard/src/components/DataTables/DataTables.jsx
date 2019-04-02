import React from "react";
// react component for creating dynamic tables

// core components
import { Button, Checkbox } from "components";
import {
    Table
  } from "reactstrap";

function ReactTables({...props}){
  return(
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
                <tr>
                    <td className="text-center">1</td>
                    <td className="text-center">
                        <Checkbox />
                    </td>
                    <td>Futebol</td>
                    <td>Twitter</td>
                    <td className="text-center">keywords</td>
                    <td className="text-right">FCPORTO, PORTUGAL, ...</td>
                    <td className="text-right">...</td>
                    <td className="text-right">
                        <Button icon neutral color="success" size="sm">
                            <i className="now-ui-icons ui-2_settings-90"></i>
                        </Button>{` `}
                        <Button icon neutral color="danger" size="sm">
                            <i className="now-ui-icons ui-1_simple-remove"></i>
                        </Button>{` `}
                    </td>
                </tr>
                <tr>
                    <td className="text-center">2</td>
                    <td className="text-center">
                        <Checkbox />
                    </td>
                    <td>Politica</td>
                    <td>Twitter</td>
                    <td className="text-center">keywords</td>
                    <td className="text-right">Brexit, DonaldTrump, ...</td>
                    <td className="text-right">...</td>
                    <td className="text-right">
                        <Button icon neutral color="success" size="sm">
                            <i className="now-ui-icons ui-2_settings-90"></i>
                        </Button>{` `}
                        <Button icon neutral color="danger" size="sm">
                            <i className="now-ui-icons ui-1_simple-remove"></i>
                        </Button>{` `}
                    </td>
                </tr>
            </tbody>
        </Table>
    </div>
  );
}
export default ReactTables;
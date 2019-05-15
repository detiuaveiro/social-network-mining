import React from "react";
import {
  Card,
  CardHeader,
  CardBody,
  CardTitle,
  Row,
  Col
} from "reactstrap";

import { PanelHeader, DataTables } from "components";

class Policies extends React.Component {

  constructor(props) {
    super(props);

    this.editPolicy = this.editPolicy.bind(this);
  }

  editPolicy(policy) {
    
  }

  render() {
    return (
      <div>
        <PanelHeader
          size="md"
          content={
            <div className="header text-center">
              <h2 className="title">Policies</h2>
            </div>
          }
        />
        <div className="content">
          <Row>
            <Col xs={12} md={12}>
              <Card className="card-tasks">
                <CardHeader>
                  <CardTitle tag="h4">Policies</CardTitle>
                </CardHeader>
                <CardBody>
                  <DataTables policies={[{
                    name : "Example name",
                    api_type : "Twitter",
                    filter : "keywords",
                    params : ["keyword1","keyword2","keyword3"],
                    id_policy : "something",
                    target : "..."
                  }]}
                   editPolicy={this.editPolicy} />

                </CardBody>
              </Card>
            </Col>
          </Row>
        </div>
      </div>
    );
  }
}

export default Policies;

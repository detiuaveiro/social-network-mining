import React from "react";
import {
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  CardTitle,
  Row,
  Col
} from "reactstrap";

import { PanelHeader, Stats, CardCategory, Tasks, DataTables } from "components";

class Policies extends React.Component {
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
                  <DataTables />
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

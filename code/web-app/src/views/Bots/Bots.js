import React, { Component } from 'react';
import baseURL from '../../variables/baseURL'
import { Container, Row, Col, Button } from 'reactstrap';

import Table from "../../components/Table/Table.js";

import Card from "../../components/Card/Card";
import CardHeader from "../../components/Card/CardHeader";
import CardBody from "../../components/Card/CardBody";
import CardFooter from "../../components/Card/CardFooter";
import CardIcon from "../../components/Card/CardIcon";

class Bots extends Component {
  constructor(props) {
    super(props);
  }


  loading = () => <div className="animated fadeIn pt-1 text-center">Loading...</div>

  render() {

    return (
      <div className="animated fadeIn">
        <Container fluid>
          <Row>
            <Col xs="12" sm="12" md="9">
              <Card>
                <CardHeader color="primary">
                  <h3 style={{ color: "white" }}>
                    <strong>Bots</strong>
                  </h3>
                  <h5 style={{ color: "white" }}>
                    List with all registered bot accounts and their status
                  </h5>
                </CardHeader>
                <CardBody>
                </CardBody>
              </Card>
            </Col>

            <Col xs="12" sm="12" md="3">
              <Card>
                <CardHeader color="primary" stats icon>
                  <CardIcon color="primary">
                    <i class="fab fa-twitter"></i>
                  </CardIcon>
                  <p style={{
                    color: '#999',
                    margin: "0",
                    fontSize: "14px",
                    marginTop: "0",
                    paddingTop: "10px",
                    marginBottom: "0"
                  }}>Active accounts</p>
                  <h3 style={{
                    color: "#23282c",
                    minHeight: "auto",
                    marginBottom: "3px",
                    "& small": {
                      color: "#777",
                      fontWeight: "400",
                      lineHeight: "1"
                    }
                  }} >
                    49 / 50 < small > Bots</small>
                  </h3>
                </CardHeader>
                <CardBody style={{ minHeight: "38px" }}>
                </CardBody>
              </Card>
            </Col>
          </Row>
          <Row>
            <Col xs="12" sm="12" md="12">
              <Card>
                <CardHeader color="primary">
                  <h4 style={{
                    color: "#FFFFFF",
                    marginTop: "0px",
                    minHeight: "auto",
                    marginBottom: "3px",
                    textDecoration: "none",
                    "& small": {
                      color: "#777",
                      fontSize: "65%",
                      fontWeight: "400",
                      lineHeight: "1"
                    }
                  }} > Registered Accounts</h4>
                  <Button block outline color="light" style={{width:"10%"}}>Add new</Button>
                </CardHeader>
              <CardBody>
                <Table
                  tableHeaderColor="primary"
                  tableHead={["Username", "Name", "other", "shit"]}
                  tableData={[
                    ["Dakota Rice", "Niger", "Oud-Turnhout", "$36,738"],
                    ["Minerva Hooper", "Curaçao", "Sinaai-Waas", "$23,789"],
                    ["Sage Rodriguez", "Netherlands", "Baileux", "$56,142"],
                    ["Philip Chaney", "Korea, South", "Overland Park", "$38,735"],
                    ["Doris Greene", "Malawi", "Feldkirchen in Kärnten", "$63,542"],
                    ["Mason Porter", "Chile", "Gloucester", "$78,615"]
                  ]}
                />
              </CardBody>
              </Card>
            </Col>
          </Row>
        </Container>

      </div >
    );
  }
}

export default Bots;

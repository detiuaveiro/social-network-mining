import React, { Component } from 'react';
import baseURL from '../../variables/baseURL'
import {
  FormGroup, Label, Input,
  Container, Row, Col, Button, Badge, Form,
} from 'reactstrap';

import Table from "../../components/Table/Table.js";

import Card from "../../components/Card/Card";
import CardHeader from "../../components/Card/CardHeader";
import CardBody from "../../components/Card/CardBody";
import CardIcon from "../../components/Card/CardIcon";

import { ToastContainer, toast, Flip } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import ReactLoading from "react-loading";
import Pagination from '@material-ui/lab/Pagination';

//import { PieChart } from 'react-minimal-pie-chart';

import { PieChart, Pie, Sector, Cell } from 'recharts';


import FadeIn from "react-fade-in";
import Lottie from "react-lottie";

import Dialog from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogTitle from "@material-ui/core/DialogTitle";

import * as loadingAnim from "../../assets/animations/squares_1.json";


class Statistics extends Component {
  constructor() {
    super();
  }

  state = {
    error: false,
    doneLoading: false,

    animationOptions: {
      loop: true, autoplay: true, animationData: loadingAnim.default, rendererSettings: {
        preserveAspectRatio: "xMidYMid slice"
      }
    },
  };


  async componentDidMount() {
    this.setState({
      doneLoading: true
    })
  }


  // Methods //////////////////////////////////////////////////////////

  /////////////////////////////////////////////////////////////////////

  loading = () => <div className="fadeIn pt-1 text-center"><ReactLoading type={"cubes"} color="#1da1f2" /></div>

  render() {

    if (!this.state.doneLoading) {
      return (
        <div className="animated fadeOut animated" style={{ width: "100%", marginTop: "10%" }}>
          <FadeIn>
            <Lottie options={this.state.animationOptions} height={"30%"} width={"30%"} />
          </FadeIn>
        </div>
      )
    } else if (this.state.error) {
      return (
        <Container fluid>
          <Row>
            <Col xs="12" sm="12" md="12">
              <div style={{ width: "100%", alignContent: "center" }}>
                <img style={{ width: "50%", display: "block", marginLeft: "auto", marginRight: "auto" }} src={require("../../assets/img/error.png")}></img>
              </div>
            </Col>
          </Row>
        </Container>
      )
    } else {
      /*
      <PieChart
        style={{
          fontFamily:
            '"Cabin", -apple-system, Helvetica, Arial, sans-serif',
          fontSize: '6px',
        }}

        label={({ dataEntry }) => dataEntry.value}
        labelPosition={50}
        labelStyle={{
          fill: '#fff',
          opacity: 0.75,
          pointerEvents: 'none',
        }}

        animate
        animationDuration={500}
        animationEasing="ease-out"

        center={[
          50,
          50
        ]}

        data={[
          {
            color: '#f77737',
            title: 'Users',
            value: 10
          },
          {
            color: '#63c2de',
            title: 'Tweets',
            value: 15
          },
          {
            color: '#833ab4',
            title: 'Bots',
            value: 20
          }
        ]}

        lengthAngle={360}
        lineWidth={100}
        paddingAngle={0}
        radius={40}

        startAngle={0}
        viewBoxSize={[
          100,
          100
        ]}
      />
      */

      const data = [
        { name: 'Users', value: 400 },
        { name: 'Tweets', value: 300 },
        { name: 'Bots', value: 300 },
      ];

      const COLORS = ['#f77737', '#63c2de', '#833ab4'];

      const RADIAN = Math.PI / 180;
      const renderCustomizedLabel = ({
        cx, cy, midAngle, innerRadius, outerRadius, percent, index,
      }) => {
        const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
        const x = cx + radius * Math.cos(-midAngle * RADIAN);
        const y = cy + radius * Math.sin(-midAngle * RADIAN);

        return (
          <text x={x} y={y} fill="white" textAnchor={x > cx ? 'start' : 'end'} dominantBaseline="central">
            {`${(percent * 100).toFixed(0)}%`}
          </text>
        );
      };

      return (
        <div className="animated fadeIn">

          <Container fluid>
            <ToastContainer
              position="top-center"
              autoClose={2500}
              hideProgressBar={false}
              transition={Flip}
              newestOnTop={false}
              closeOnClick
              rtl={false}
              pauseOnVisibilityChange
              draggable
              pauseOnHover
            />
            <Row>
              <Col xs="12" sm="12" md="12">
                <Card>
                  <CardHeader color="primary">
                    <h3 style={{ color: "white" }}>
                      <strong>Statistics</strong>
                    </h3>
                    <h5 style={{ color: "white" }}>
                      Various graphs showcasing the functioning and current state of our service
                    </h5>
                  </CardHeader>
                  <CardBody>
                  </CardBody>
                </Card>
              </Col>
            </Row>
            <Row>
              <Col xs="12" sm="12" md="8">
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
                    }} > Latest Activities</h4>
                  </CardHeader>
                </Card>
              </Col>

              <Col xs="12" sm="12" md="4">
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
                    }} > Recorded Entities</h4>
                  </CardHeader>
                  <CardBody>
                    <PieChart width={400} height={400}>
                      <Pie
                        data={data}
                        cx={200}
                        cy={200}
                        labelLine={false}
                        label={renderCustomizedLabel}
                        outerRadius={80}
                        
                        fill="#8884d8"
                        dataKey="value"
                      >
                        {
                          data.map((entry, index) => <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />)
                        }
                      </Pie>
                    </PieChart>
                  </CardBody>
                </Card>
              </Col>
            </Row>
          </Container>
        </div >
      );
    }
  }
}

export default Statistics;

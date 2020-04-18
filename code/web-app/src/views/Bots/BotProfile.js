import React, { Component, lazy, Suspense } from 'react';
import { Bar, Line } from 'react-chartjs-2';

import baseURL from '../../variables/baseURL'
import { Container, Row, Col, Button, Pagination, PaginationItem, PaginationLink, } from 'reactstrap';
import Table from "../../components/Table/Table.js";

import Card from "../../components/Card/Card";
import CardHeader from "../../components/Card/CardHeader";
import CardBody from "../../components/Card/CardBody";
import CardFooter from "../../components/Card/CardFooter";
import CardIcon from "../../components/Card/CardIcon";
import CardAvatar from "../../components/Card/CardAvatar.js";

import Bots from './Bots';

import { CustomTooltips } from '@coreui/coreui-plugin-chartjs-custom-tooltips';

import ReactLoading from "react-loading";

const Widget03 = lazy(() => import('../../views/Widgets/Widget03'));


const makeSocialBoxData = (dataset) => {
    const data = {
        labels: dataset.labels,
        datasets: [
            {
                backgroundColor: 'rgba(255,255,255,.1)',
                borderColor: 'rgba(255,255,255,.55)',
                pointHoverBackgroundColor: '#fff',
                borderWidth: 2,
                data: dataset.data,
                label: dataset.label,
            },
        ],
    };
    return () => data;
};

const socialChartOpts = {
    tooltips: {
        enabled: false,
        custom: CustomTooltips
    },
    responsive: true,
    maintainAspectRatio: false,
    legend: {
        display: false,
    },
    scales: {
        xAxes: [
            {
                display: false,
            }],
        yAxes: [
            {
                display: false,
            }],
    },
    elements: {
        point: {
            radius: 0,
            hitRadius: 10,
            hoverRadius: 4,
            hoverBorderWidth: 3,
        },
    },
};

class BotProfile extends Component {
    constructor() {
        super();
    }

    state = {
        error: false,
        goBack: false,
        policies: [],
        activities: [],
        loading: false
    };

    handleOpenPolicy(policy) {
        console.log(policy)
    }


    getBotPolicies() {
        fetch(baseURL + "policies/bots/" + this.props.bot.user_id, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            }
        }).then(response => {
            if (response.ok) return response.json();
            else {
                throw new Error(response.status);
            }
        }).then(data => {
            if (data != null && data != {}) {
                data = data.data

                var tempPolicies = []

                data.forEach(policy => {
                    var tempInfo = []
                    tempInfo.push("" + policy.name);
                    tempInfo.push("" + policy.filter);
                    tempInfo.push("" + policy.tags);

                    tempInfo.push("Active"); // Add wether its active or not


                    tempInfo.push(
                        <Button block outline color="primary"
                            onClick={() => this.handleOpenPolicy(policy)}
                        >
                            <i class="fas fa-ellipsis-h"></i>
                            <strong style={{ marginLeft: "3px" }}>More</strong>
                        </Button>
                    )

                    tempPolicies.push(tempInfo);
                })

                tempPolicies.sort((policy1, policy2) =>
                    policy1.name > policy2.name ? 1 : -1
                );

                this.setState({
                    error: this.state.error,
                    goBack: this.state.goBack,
                    policies: tempPolicies,
                    activities: this.state.activities,
                    loading: true
                })
            }
        }).catch(error => {
            console.log("error: " + error);
            this.setState({
                error: true,
                goBack: true,
                policies: this.state.policies,
                activities: this.state.activities,
                loading: this.state.loading
            })
        });
    }


    componentDidMount() {
        this.setState({
            error: this.state.error,
            goBack: this.state.goBack,
            policies: this.state.policies,
            activities: this.state.activities,
            loading: true
        })

        // Get Activities

        // Get Policies
        //this.getBotPolicies()

        this.setState({
            error: this.state.error,
            goBack: this.state.goBack,
            policies: this.state.policies,
            activities: this.state.activities,
            loading: false
        })

    }

    handleGoBack() {
        console.log("back")
        this.setState({
            error: this.state.error,
            goBack: true,
            policies: this.state.policies,
            activities: this.state.activities,
            loading: this.state.loading
        })
    }


    loading = () => <div className="fadeIn pt-1 text-center"><ReactLoading type={"cubes"} color="#1da1f2" /></div>

    render() {
        if (this.state.goBack) {
            return (<Bots />)
        }
        else if (this.state.error) {
            return (
                <div className="animated fadeIn">
                    <Container fluid>
                        <Row>
                            <Col xs="12" sm="12" md="12">
                                <Card>
                                    <CardHeader color="primary">
                                        <h3 style={{ color: "white" }}>
                                            <strong>Bot Profile</strong>
                                        </h3>
                                    </CardHeader>
                                    <CardBody>
                                        <Button block outline color="danger" onClick={() => this.handleGoBack()} style={{
                                            width: "150px", marginTop: "15px"
                                        }}><i class="fas fa-chevron-left"></i> Go Back</Button>
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
                                    </CardHeader>
                                    <CardBody>
                                        <p>Sorry, an error has occured! Please try again shortly</p>
                                    </CardBody>
                                </Card>
                            </Col>
                        </Row>
                    </Container>
                </div>
            )
        } else {
            return (
                <div className="animated fadeIn">
                    <Container fluid>
                        <Row>
                            <Col xs="12" sm="12" md="12" style={{ marginBottom: "30px" }}>
                                <Button block outline color="danger" onClick={() => this.handleGoBack()} style={{
                                    width: "150px", marginTop: "15px"
                                }}><i class="fas fa-chevron-left"></i> Go Back</Button>
                            </Col>
                        </Row>
                        <Row>
                            <Col xs="12" sm="12" md="4">
                                <Card profile>
                                    <CardAvatar profile>
                                        <a onClick={e => e.preventDefault()}>
                                            <img src={this.props.bot.profile_image_url_https} alt="Profile Image" style={{ minWidth: "100px" }} />
                                        </a>
                                    </CardAvatar>
                                    <CardBody profile>
                                        <h6 style={{
                                            color: "#999",
                                            margin: "0",
                                            fontSize: "14px",
                                            marginTop: "0",
                                            paddingTop: "10px",
                                            marginBottom: "0"
                                        }}>@{this.props.bot.screen_name}</h6>
                                        <h4 style={{
                                            color: "#3C4858",
                                            marginTop: "0px",
                                            minHeight: "auto",
                                            fontWeight: "300",
                                            marginBottom: "3px",
                                            textDecoration: "none",
                                            "& small": {
                                                color: "#999",
                                                fontWeight: "400",
                                                lineHeight: "1"
                                            }
                                        }}>{this.props.bot.name}</h4>
                                        <h5 style={{ marginTop: "15px" }}>
                                            <i>{this.props.bot.description}</i>
                                        </h5>

                                        <div class="row" style={{ marginTop: "20px" }}>
                                            <div class="col-sm-12 offset-md-3 col-md-3">
                                                <h6><b>{this.props.bot.followers_count}</b> following</h6>
                                            </div>

                                            <div class="col-sm-12 col-md-3">
                                                <h6><b>{this.props.bot.friends_count}</b> followers</h6>
                                            </div>
                                        </div>
                                    </CardBody>
                                    <CardFooter>
                                        <h5><b style={{ color: "#4dbd74" }}>Active</b></h5>
                                    </CardFooter>
                                </Card>

                                <Suspense fallback={this.loading()}>
                                    <Widget03 dataBox={() => ({ variant: 'twitter', tweets: '1.792' })} >
                                        <div className="chart-wrapper">
                                            <Line data={makeSocialBoxData({ data: [1, 13, 9, 17, 34, 41, 38], label: 'twitter', labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'] })} options={socialChartOpts} height={90} />
                                        </div>
                                    </Widget03>
                                </Suspense>
                            </Col>
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
                                        }} > Activity</h4>
                                    </CardHeader>
                                    <CardBody style={{ paddingTop: "0px" }}>
                                        <Table style={{ paddingTop: "0px" }}
                                            tableHeaderColor="primary"
                                            tableHead={["Log", "Description", "Date"]}
                                            tableData={[["Posted Tweet", "Published a new tweet - #id", "24/24/24"], ["Posted Tweet", "Published a new tweet - #id", "24/24/24"], ["Posted Tweet", "Published a new tweet - #id", "24/24/24"], ["Posted Tweet", "Published a new tweet - #id", "24/24/24"], ["Posted Tweet", "Published a new tweet - #id", "24/24/24"], ["Posted Tweet", "Published a new tweet - #id", "24/24/24"]]}
                                        />
                                    </CardBody>
                                    <CardFooter>
                                        <div class="col-12">
                                            <Pagination>
                                                <PaginationItem>
                                                    <PaginationLink previous tag="button"></PaginationLink>
                                                </PaginationItem>
                                                <PaginationItem active>
                                                    <PaginationLink tag="button">1</PaginationLink>
                                                </PaginationItem>
                                                <PaginationItem>
                                                    <PaginationLink tag="button">2</PaginationLink>
                                                </PaginationItem>
                                                <PaginationItem>
                                                    <PaginationLink tag="button">3</PaginationLink>
                                                </PaginationItem>
                                                <PaginationItem>
                                                    <PaginationLink tag="button">4</PaginationLink>
                                                </PaginationItem>
                                                <PaginationItem>
                                                    <PaginationLink next tag="button"></PaginationLink>
                                                </PaginationItem>
                                            </Pagination>
                                        </div>
                                    </CardFooter>
                                </Card>
                            </Col>
                        </Row>

                        <Row>
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
                                        }} > Last tweet</h4>
                                        <Button block outline color="light" style={{
                                            width: "150px", marginTop: "15px"
                                        }}>Post new tweet</Button>
                                    </CardHeader>
                                    <CardBody>
                                        <h5 style={{ marginTop: "15px" }}>
                                            <i>"oi"</i>
                                        </h5>
                                    </CardBody>
                                </Card>

                            </Col>
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
                                        }} > Policies</h4>
                                        <Button block outline color="light" style={{
                                            width: "150px", marginTop: "15px"
                                        }}>Add policy</Button>
                                    </CardHeader>
                                    <CardBody>
                                        <Table
                                            tableHeaderColor="primary"
                                            tableHead={["Name", "Type", "Tags", "Status", ""]}
                                            tableData={[["Posted Tweet", "Published a new tweet - #id", "24/24/24", ""]]}
                                        />
                                    </CardBody>
                                </Card>
                            </Col>
                        </Row>
                    </Container>
                </div>
            )
        }

    }
}

export default BotProfile;

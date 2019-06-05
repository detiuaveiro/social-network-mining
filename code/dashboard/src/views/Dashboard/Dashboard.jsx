import React from "react";
import {
  Card,
  CardHeader,
  CardBody,
  CardTitle,
  Row,
  Col,
} from "reactstrap";
// react plugin used to create charts
import { Line } from "react-chartjs-2";
// function that returns a color based on an interval of numbers

import { PanelHeader} from "components";

import {
  dashboardShippedProductsChart,
  dashboardAllProductsChart,
  dashboard24HoursPerformanceChart,
  dashboardFollowersPerformanceChart
} from "variables/charts.jsx";
import axios from "axios";

class Dashboard extends React.Component {
  state = {
    twitter_stats: [],
  };

  componentDidMount() {
    axios.get('http://192.168.85.182:5000/twitter/stats')
      .then(res => {
        const twitter_stats = res.data;
        this.setState({ twitter_stats });
        console.log(this.state.twitter_stats)
      })
/*     axios.get('/instagram/bots')
      .then(res => {
        const instagram_bots = res.data;
        this.setState({ instagram_bots });
      }) */
  }

  render() {
    return (
      <div>
        <PanelHeader
          size="md"
          content={
            <div className="header text-center">
              <h2 className="title">Dashboard</h2>
            </div>
          }
        />
        <div>
          <iframe src="http://mongodb-redesfis.5g.cn.atnog.av.it.pt:5601/app/kibana#/dashboard/2dd795b0-871f-11e9-9e1a-1d51404a76cd?embed=true&_g=(refreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3Anow%2FM%2Cto%3Anow))" height="100%" width="100%"></iframe>
        </div>
      </div>
    );
  }
}

export default Dashboard;

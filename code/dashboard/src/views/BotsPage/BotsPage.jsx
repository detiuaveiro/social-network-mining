import React from "react";

import { PanelHeader, CardBot } from "components";
import {
  Nav,
  NavItem,
  NavLink,
  Row,
  Col,
  TabPane,
  TabContent,
} from "reactstrap";
import axios from 'axios';

class BotsPage extends React.Component {
  state = {
    twitter_bots: [],
    instagram_bots: [],
    activeTab: '1',
  };

  componentDidMount() {
    axios.get('http://192.168.85.182:5000/twitter/bots')
      .then(res => {
        const twitter_bots = res.data;
        this.setState({ twitter_bots });
        console.log(this.state.twitter_bots)
      })
/*     axios.get('/instagram/bots')
      .then(res => {
        const instagram_bots = res.data;
        this.setState({ instagram_bots });
      }) */
  }

  constructor(props) {
    super(props);
    this.toggle = this.toggle.bind(this);
  }
  toggle(tab) {
      if (this.state.activeTab !== tab) {
          this.setState({
              activeTab: tab
          });
      }
  }
  render() {
    return (
      <div>
        <PanelHeader
          size="md"
          content={
            <div>
              <div className="header text-center">
                <h2 className="title">Bots</h2>
              </div>
              <Nav className="nav-tabs-default justify-content-right" tabs>
                <NavItem>
                    <NavLink
                        className={this.state.activeTab === '1' ? 'active':''}
                        onClick={() => { this.toggle('1'); }}
                    >
                    All
                    </NavLink>
                </NavItem>
                <NavItem>
                    <NavLink
                        className={this.state.activeTab === '2' ? 'active':''}
                        onClick={() => { this.toggle('2'); }}
                    >
                    Twitter
                    </NavLink>
                </NavItem>
                <NavItem>
                    <NavLink
                        className={this.state.activeTab === '3' ? 'active':''}
                        onClick={() => { this.toggle('3'); }}
                    >
                    Instagram
                    </NavLink>
                </NavItem>
              </Nav>
            </div>
          }
        />
        <div className="content mt-5 pt-4">
            <TabContent activeTab={this.state.activeTab} className="text-center">
              <TabPane tabId="1">
                <Row>
                  {this.state.twitter_bots.map(bots => 
                    <Col xs={12} md={4}>
                      <CardBot info={bots} />
                    </Col>
                  )}
                </Row>
{/*                 {this.state.instagram_bots.map(bots => 
                  <Col xs={12} md={3}>
                    <CardBot/>
                  </Col>
                )} */}
              </TabPane>
              <TabPane tabId="2">
                <Row>
                  {this.state.twitter_bots.map(bots => 
                    <Col xs={12} md={4}>
                      <CardBot info={bots}/>
                    </Col>
                  )}
                </Row>
              </TabPane>
              <TabPane tabId="3">
{/*                 {this.state.instagram_bots.map(bots => 
                  <Col xs={12} md={3}>
                    <CardBot/>
                  </Col>
                )} */}
              </TabPane>
            </TabContent>
        </div>
      </div>
    );
  }
}

export default BotsPage;

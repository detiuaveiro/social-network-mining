import React from "react";
// react plugin used to create charts
// function that returns a color based on an interval of numbers
import { PanelHeader} from "components";
import {
  Nav,
  NavItem,
  NavLink,
  Row,
  TabPane,
  TabContent,
} from "reactstrap";

class Network extends React.Component {
  state = {
    activeTab: '1',
    config1: {
      container_id: "viz",
      server_url: "bolt://192.168.85.187:7687",
      server_user: "neo4j",
      server_password: "neo4jPI",
      labels: {
        "Bot": {
          "caption": "name",
          "size": "pagerank",
          "community": "bots",
        },
        "User": {
          "caption": "name",
          "size": "pagerank",
        }
      },
      relationships: {
        "FOLLOWS": {
          caption: true,
          thickness: "count"
        }
      },
      arrows: true,
      initial_cypher: "MATCH (bot:Bot)-[follows:FOLLOWS]->(user:User) RETURN bot, follows, user Limit 300",
    },
    config2: {
      container_id: "viz2",
      server_url: "bolt://192.168.85.187:7687",
      server_user: "neo4j",
      server_password: "neo4jPI",
      labels: {
        "Bot": {
          "caption": "name",
          "size": "pagerank",
          "community": "bots",
        },
        "User": {
          "caption": "name",
          "size": "pagerank",
        }
      },
      relationships: {
        "FOLLOWS": {
          caption: true,
          thickness: "count"
        }
      },
      arrows: true,
      initial_cypher: "MATCH (user1:User)-[follows:FOLLOWS]->(user2:User) RETURN user1, follows, user2 Limit 300",
    },
  };
  constructor(props) {
    super(props);
    this.toggle = this.toggle.bind(this);
    this.loadGraphFirstTime = this.loadGraphFirstTime.bind(this);
  }

  componentDidMount() {
    this.loadGraphFirstTime()
  }

  loadGraphFirstTime(){
    this.vis = new window.NeoVis.default(this.state.config1);
    this.vis2 = new window.NeoVis.default(this.state.config2);
    this.vis.render();
    this.vis2.render();
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
                <h2 className="title">Network</h2>
              </div>
              <Nav className="nav-tabs-default justify-content-right" tabs>
                <NavItem>
                    <NavLink
                        className={this.state.activeTab === '1' ? 'active':''}
                        onClick={() => { this.toggle('1'); }}
                    >
                    Bots
                    </NavLink>
                </NavItem>
                <NavItem>
                    <NavLink
                        className={this.state.activeTab === '2' ? 'active':''}
                        onClick={() => { this.toggle('2'); }}
                    >
                    Users
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
                  <div
                    id="viz"
                    style={{width: "100%",
                      height: "700px"}}
                  >
                  </div>
                </Row>
              </TabPane>
              <TabPane tabId="2">
                <Row>
                  <div
                    id="viz2"
                    style={{width: "100%",
                      height: "700px"}}
                  >
                  </div>
                </Row>
              </TabPane>
            </TabContent>
        </div>
      </div>
    );
  }
}

export default Network;

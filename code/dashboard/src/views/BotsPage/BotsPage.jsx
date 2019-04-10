import React from "react";

import { PanelHeader, Stats, CardAuthor, CardCategory, CardInteractions, Button } from "components";
import {
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  CardTitle,
  Row,
  Col,
  UncontrolledDropdown,
  DropdownToggle,
  DropdownMenu,
  DropdownItem,
} from "reactstrap";
import axios from 'axios';
import userAvatar from "assets/img/mike.jpg";

class BotsPage extends React.Component {
  state = {
    twitter_bots: [],
    instagram_bots:[],
  };
  constructor(props) {
    super(props);
    this.state = {
        activeTab: '1',
    };
    this.toggle = this.toggle.bind(this);
  }
  componentDidMount() {
    axios.get('/twitter/bots')
      .then(res => {
        console.log(res.data)
        const twitter_bots = res.data;
        this.setState({ twitter_bots });
      })
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
            <div className="header text-center">
              <h2 className="title">Bots</h2>
            </div>
          }
        />
        <div className="content">
          <Row>
              <Col xs={12} md={4}>
                <Card className="card-chart">
                  <CardHeader>
                    <CardCategory>Twitter</CardCategory>
                    <CardAuthor
                      avatar={userAvatar}
                      avatarAlt="..."
                      title="Afonso Silva"
                      description="@afonsosilva01"
                    />
                  </CardHeader>
                  <CardBody>

                  </CardBody>
                  <CardFooter>
                    <Stats>
                      {[
                        {
                          i: "now-ui-icons arrows-1_refresh-69",
                          t: "Just Updated"
                        }
                      ]}
                    </Stats>
                  </CardFooter>
                </Card>
              </Col>
         </Row>
        </div>
      </div>
    );
  }
}

export default BotsPage;

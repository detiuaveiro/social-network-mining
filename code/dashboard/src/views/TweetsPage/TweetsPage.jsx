import React from "react";
import axios from 'axios';

import { Tweet, PanelHeader} from "components";
import {Collapse, Row, Col, InputGroup, InputGroupText, InputGroupAddon, Input } from 'reactstrap';

class User extends React.Component {
  state = {
    tweets: [],
  };

  componentDidMount() {
    axios.get('http://192.168.85.182:5000/twitter/tweets')
      .then(res => {
        const tweets = res.data;
        this.setState({ tweets });
      })
  }

  constructor(props) {
    super(props);
    this.anyTweets = this.anyTweets.bind(this);
  }

  anyTweets() {
    if (this.state.tweets.length==0){
      return false
    }
    else{
      return true
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
                <h2 className="title">Tweets</h2>
              </div>
              <div>
                <p className="title text-center text-white">- Filters -</p>
                <Col xs={6} xs={5}
                    navbar
                    className="justify-content-end"
                  >
                  <form>
                    <InputGroup className="no-border">
                      <Input placeholder="Search Tweet by User" />
                      <InputGroupAddon addonType="append">
                        <InputGroupText>
                          <i className="now-ui-icons ui-1_zoom-bold" />
                        </InputGroupText>
                      </InputGroupAddon>
                    </InputGroup>
                  </form>
                </Col>
              </div>
            </div>
          }
        />
        <div className="content mt-5 pt-4">
          <Row>
            {this.anyTweets()
              ? this.state.tweets.map(tweet => 
                <Col xs={12} md={6}>
                  <Tweet info={tweet}/>
                </Col>
                )
              : <Col xs={12} md={12}>
                  <h5 className="text-muted text-center">
                    No Tweets Available
                  </h5>
                </Col>
            }
          </Row>
        </div>
      </div>
    );
  }
}

export default User;

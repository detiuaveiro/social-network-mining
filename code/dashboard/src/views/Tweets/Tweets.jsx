import React from "react";
import axios from 'axios';

import { Tweet, PanelHeader} from "components";
import {Row, Col} from 'reactstrap';

class Tweets extends React.Component {
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
    if (this.state.tweets.length===0){
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
          size="sm"
          content={
            <div>
              <div className="header text-center">
                <h2 className="title">Tweets</h2>
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

export default Tweets;

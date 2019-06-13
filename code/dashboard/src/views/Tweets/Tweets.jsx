import React from "react";
import axios from 'axios';
import { PacmanLoader } from 'react-spinners';
import { css } from '@emotion/core';
import { Tweet, PanelHeader} from "components";
import {Row, Col} from 'reactstrap';

const override = css`
    text-align: center;
    margin: 0 auto;
`;

class Tweets extends React.Component {
  state = {
    tweets: [],
    loading: true,
  };

  componentDidMount() {
    axios.get(process.env.API_URL+'twitter/tweets')
      .then(res => {
        const tweets = res.data;
        this.setState({
          tweets: tweets,
          loading: false
         });
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
              : (this.state.loading)
                ? <Col xs={12} md={12} className='text-center'>
                    <PacmanLoader	
                      sizeUnit={"px"}
                      size={50}
                      color={'#6c757d'}
                      loading={this.state.loading}
                      css={override}
                    />
                  </Col>
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

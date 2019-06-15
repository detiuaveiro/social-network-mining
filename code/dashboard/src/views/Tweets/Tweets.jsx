import React from "react";
import axios from 'axios';
import { PacmanLoader } from 'react-spinners';
import { css } from '@emotion/core';
import { Tweet, PanelHeader, Button} from "components";
import {Row, Col} from 'reactstrap';

const override = css`
    text-align: center;
    margin: 0 auto;
`;

class Tweets extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      tweets: [],
      loading: true,
      limit: 100,
    };
    this.anyTweets = this.anyTweets.bind(this);
    this.loadTweets = this.loadTweets.bind(this);
    this.handleMoreTweets = this.handleMoreTweets.bind(this);
  }

  componentDidMount() {
    axios.get('http://192.168.85.182:5000/twitter/tweets?limit='+this.state.limit)
      .then(res => {
        const tweets = res.data;
        this.setState({
          tweets: tweets,
          loading: false
         });
      })  }

  loadTweets(){
    axios.get('http://192.168.85.182:5000/twitter/tweets?limit='+(this.state.limit+100))
      .then(res => {
        const tweets = res.data;
        this.setState({
          tweets: tweets,
          loading: false
         });
      })
  }

  anyTweets() {
    if (this.state.tweets.length===0){
      return false
    }
    else{
      return true
    }
  }

  handleMoreTweets() {
    this.setState({
      limit: this.state.limit+100
    })
    this.loadTweets()
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
              ? 
                <>
                {
                this.state.tweets.map(tweet => 
                  <Col xs={12} md={6}>
                    <Tweet info={tweet}/>
                  </Col>
                )
                }
                </>
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
          <Row>
            {(this.anyTweets())
                ? 
                <Col xs={12} md={12} className="text-center">
                  <Button color="primary" onClick={this.handleMoreTweets} size="lg">Load More Tweets</Button>
                </Col>
                : ""
              }
          </Row>
        </div>
      </div>
    );
  }
}

export default Tweets;

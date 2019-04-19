import React from "react";
// react plugin used to create charts
// function that returns a color based on an interval of numbers

import axios from 'axios';

class Test extends React.Component {
  state = {
    divisions: []
  };
  componentDidMount() {
    axios.get('/twitter/tweets')
      .then(res => {
        const divisions = res.data;
        this.setState({ divisions });
        console.log(this.state.divisions)
      })
  }
  render() {
    return (
      <div>
          {this.state.divisions.map(tweet => <div>test</div>
          )}
      </div>
    );
  }
}

export default Test;

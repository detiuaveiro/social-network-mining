import React from "react";
import NotificationAlert from "react-notification-alert";
import axios from 'axios';

import {PanelHeader, CreateTweet} from "components";

class TweetPage extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      bots:[]
    }
    this.sendTweet = this.sendTweet.bind(this);
    this.notify = this.notify.bind(this);
    this.refresh = this.refresh.bind(this);
  }

  componentDidMount(){
   axios.get(process.env.API_URL+'twitter/bots')
   .then(res => {
     const data = res.data;
     const options = []
     data.forEach(function(bot){
       options.push({value: bot['id'], label: bot['name']})
     })
     this.setState({bots: options});
   })
  }


  notify = (msg) => {
    var type = "primary";
    var options = {};
    options = {
      place: "tc",
      message: (
        <div>
          <div>
            {msg}
          </div>
        </div>
      ),
      type: type,
      icon: "now-ui-icons ui-1_bell-53",
      autoDismiss: 7
    };
    this.refs.notificationAlert.notificationAlert(options);
  }

  refresh(tipo,msg){
    switch(tipo){
      case "OKAY":
        this.notify("Tweet Creation Message sent with "+msg)
        break
      case "ERROR":
        this.notify("ERROR: "+msg)
        this.componentDidMount()
        break
      default:
        this.notify("ERROR")
        break
    }
  }

  sendTweet(data) {
    axios.post(process.env.API_URL+'twitter/create', data)
    .then((response) => {
      this.refresh(response.status===200 ? "OKAY" : "ERROR",response.data['Message'])
    })
  }

  render() {
    return (
      <div>
        <NotificationAlert ref="notificationAlert" />
        <PanelHeader
          size="sm"
          content={
            <div>
              <div className="header text-center">
                <h2 className="title">Create Tweet</h2>
              </div>
            </div>
          }
        />
        <div className="content mt-5 pt-4">
          <CreateTweet send={this.sendTweet} bots={this.state.bots}/>
        </div>
      </div>
    );
  }
}

export default TweetPage;

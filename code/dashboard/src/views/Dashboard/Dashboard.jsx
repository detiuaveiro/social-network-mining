import React from "react";

import { PanelHeader} from "components";

class Dashboard extends React.Component {
  state = {
    twitter_stats: [],
  };

  render() {
    return (
      <div>
        <PanelHeader
          size="sm"
          content={
            <div className="header text-center">
              <h2 className="title">Dashboard</h2>
            </div>
          }
        />
        <div>
          <iframe src={"http://192.168.85.142:5601/app/kibana#/dashboard/c375c770-8e29-11e9-8700-cf895ecb2cb4?embed=true&_g=(refreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3Anow%2FM%2Cto%3Anow))"} title="Dash Stats" height="800" width="100%"></iframe>
        </div>
      </div>
    );
  }
}

export default Dashboard;

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
          size="md"
          content={
            <div className="header text-center">
              <h2 className="title">Dashboard</h2>
            </div>
          }
        />
        <div>
          <iframe src="http://192.168.85.46:5601/app/kibana#/dashboard/caea1060-87ad-11e9-9a93-576733f53835?embed=true&_g=(refreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3Anow-10d%2Cto%3Anow))" height="800" width="100%"></iframe>
        </div>
      </div>
    );
  }
}

export default Dashboard;

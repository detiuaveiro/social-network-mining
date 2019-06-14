import React from "react";

import {PanelHeader} from "components";

class Instagram extends React.Component {

  render() {
    return (
      <div>
        <PanelHeader
          size="sm"
          content={
            <div>
              <div className="header text-center">
                <h2 className="title">Instagram</h2>
              </div>
            </div>
          }
        />
        <div className="content mt-5 pt-4">
          <a target="_blank" rel="noopener noreferrer" href={"http://192.168.85.142:8080"}>
            <h5 className="title text-center">Link</h5>
          </a>
        </div>
      </div>
    );
  }
}

export default Instagram;

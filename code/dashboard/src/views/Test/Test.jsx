import React from "react";
// react plugin used to create charts
// function that returns a color based on an interval of numbers
import * as popoto from "popoto";
import { PanelHeader} from "components";
class Test extends React.Component {

  render() {
    return (
      <div>
        <PanelHeader
          size="sm"
          content={
            <div>
              <div className="header text-center">
                <h2 className="title">Network</h2>
              </div>
            </div>
          }
        />
        <div id="popoto-graph" className="ppt-div-graph w-100" style={{height:600}}>
        </div>
      </div>
    );
  }
}

export default Test;

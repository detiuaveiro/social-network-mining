import React from "react";
// react plugin used to create charts
// function that returns a color based on an interval of numbers
import NeoVis from "neovis.js";
import { PanelHeader} from "components";

class Test extends React.Component {
  componentDidMount() {
    const config = {
      container_id: "viz",
      server_url: "bolt://100.25.118.163:33822",
      server_user: "neo4j",
      server_password: "requisitions-adjective-motions",
      labels: {
      },
      relationships: {
      },
      initial_cypher: "MATCH \
                      (follower:User)-[follows:FOLLOWS]->(user:User:Me) \
                      RETURN follower, follows, user \
                      ORDER BY follower DESC",
    }
    this.viz = new NeoVis(config);
    this.viz.render()
  }

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
        <div
          id="viz"
          style={{width: "900px",
            height: "700px"}}
        >
        </div>
      </div>
    );
  }
}

export default Test;

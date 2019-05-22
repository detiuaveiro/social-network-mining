import React from "react";
// react plugin used to create charts
// function that returns a color based on an interval of numbers
import NeoVis from "neovis.js";
import { PanelHeader} from "components";

class Network extends React.Component {
  componentDidMount() {
    const config = {
      container_id: "viz",
      server_url: "bolt://192.168.85.187:7687",
      server_user: "neo4j",
      server_password: "neo4jPI",
      labels: {
        "Bot": {
          "caption": "name",
          "size": "pagerank",
        },
        "User": {
          "caption": "name",
          "size": "pagerank",
        }
      },
      relationships: {
      },
      initial_cypher: "MATCH \
                      (bot:Bot)-[follows:FOLLOWS]->(user:User) \
                      RETURN bot, follows, user",
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
          style={{width: "95%",
            height: "700px"}}
        >
        </div>
      </div>
    );
  }
}

export default Network;
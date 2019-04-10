import React from "react";
// used for making the prop types of this component
import PropTypes from "prop-types";

import { Button } from "components";

class CardInteractions extends React.Component {
  render() {
    return (
      <div className="button-container">
        {this.props.socials.map((prop, key) => {
          return (
            <Button
              color="neutral"
              size={this.props.size}
              key={key}
            >
              <i className={prop.icon}/>
              <h5 className="text-muted">
                {prop.number}
              </h5>              
            </Button>
          );
        })}
      </div>
    );
  }
}

CardInteractions.propTypes = {
  // size of all social buttons
  size: PropTypes.oneOf(["sm", "lg"]),
  // example: [{icon: "name of icon", href="href of icon"},...]
  socials: PropTypes.arrayOf(PropTypes.object)
};

export default CardInteractions;
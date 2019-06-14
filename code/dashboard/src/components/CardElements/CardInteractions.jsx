import React from "react";
// used for making the prop types of this component
import PropTypes from "prop-types";

import { Button } from "components";

class CardInteractions extends React.Component {
  render() {
    return (
      <div className="button-container">
        {this.props.socials.map((prop, key) => {
          return(
            <>
            {
              (prop.tipo==="icon") 
            ?
              <Button
                color="neutral"
                size={this.props.size}
                key={key}
              >
                <i className={prop.icon}/>
                <h6 className="text-muted">
                  {prop.number}
                </h6>              
              </Button>

            :
              <Button
                color="neutral"
                size={this.props.size}
                key={key}
              >
                {prop.text}
                <h6 className="text-muted">
                  {prop.number}
                </h6>
              </Button>
            }
            </>
          );
        })}
      </div>
    );
  }
}

CardInteractions.propTypes = {
  // size of all social buttons
  size: PropTypes.oneOf(["xs", "sm", "lg"]),
  // example: [{icon: "name of icon", href="href of icon"},...]
  socials: PropTypes.arrayOf(PropTypes.object)
};

export default CardInteractions;

/*eslint-disable*/
import React from "react";
import PropTypes from "prop-types";
// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";
import ListItem from "@material-ui/core/ListItem";
import List from "@material-ui/core/List";
// core components
import styles from "assets/jss/material-dashboard-react/components/footerStyle.js";

const useStyles = makeStyles(styles);

export default function Footer(props) {
  const classes = useStyles();
  return (
    <footer className={classes.footer} style={{backgroundColor:"transparent"}}>
      <div className={classes.container}>
        <div className={classes.left}>

        </div>
        <p className={classes.right}>
          <span>
            Made with the help of a free template taken from
            <a
              href="https://www.creative-tim.com?ref=mdr-footer"
              target="_blank"
              className={classes.a}
              style={{marginLeft:"4px"}}
            >
              Creative Tim
            </a>
          </span>
        </p>
      </div>
    </footer>
  );
}

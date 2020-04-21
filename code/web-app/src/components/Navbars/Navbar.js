import React from "react";
import classNames from "classnames";
import PropTypes from "prop-types";
// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import IconButton from "@material-ui/core/IconButton";
import Hidden from "@material-ui/core/Hidden";
// @material-ui/icons
import Menu from "@material-ui/icons/Menu";
// core components
import AdminNavbarLinks from "./AdminNavbarLinks.js";
import RTLNavbarLinks from "./RTLNavbarLinks.js";
import Button from "components/CustomButtons/Button.js";

import Breadcrumbs from '@material-ui/core/Breadcrumbs';
import Typography from '@material-ui/core/Typography';
import Link from '@material-ui/core/Link';
import NavigateNextIcon from '@material-ui/icons/NavigateNext';

import styles from "assets/jss/material-dashboard-react/components/headerStyle.js";

const useStyles = makeStyles(styles);

export default function Header(props) {
  const classes = useStyles();

  var paths = { paths: []} 
  var current = null
  function makeBrand() {
    var name;
    props.routes.map(prop => {
      if (window.location.href.indexOf(prop.layout + prop.path) !== -1) {
        name = props.rtlActive ? prop.rtlName : prop.layout + prop.path;
      }
      return null;
    });

    var tmp = name.split("/"), allPaths = [""];
    for(var i = 1; i < tmp.length - 1; i++)
      allPaths.push(tmp[i].charAt(0).toUpperCase() + tmp[i].slice(1));

    paths = { paths: allPaths };
    current = tmp[tmp.length - 1].charAt(0).toUpperCase() + tmp[tmp.length - 1].slice(1);
  }
  const { color } = props;
  const appBarClasses = classNames({
    [" " + classes[color]]: color
  });

  const handleClick = (event) => {
    event.preventDefault();
    console.info('You clicked a breadcrumb.');
  }
  return (
    <AppBar className={classes.appBar + appBarClasses}>
      <Toolbar className={classes.container}>
        <div className={classes.flex}>
          {makeBrand()}
          <Button color="transparent" href="#" className={classes.title}>
          <Breadcrumbs separator={<NavigateNextIcon fontSize="small" />} aria-label="breadcrumb">
            {paths.paths.map((path) => {
              return <Link color="inherit" onClick={handleClick}>
              {path}
              </Link>
            })}
            <Typography color="textPrimary">{current}</Typography>
          </Breadcrumbs>
          </Button>
        </div>
        <Hidden smDown implementation="css">
          {props.rtlActive ? <RTLNavbarLinks /> : <AdminNavbarLinks />}
        </Hidden>
        <Hidden mdUp implementation="css">
          <IconButton
            color="inherit"
            aria-label="open drawer"
            onClick={props.handleDrawerToggle}
          >
            <Menu />
          </IconButton>
        </Hidden>
      </Toolbar>
    </AppBar>
  );
}

Header.propTypes = {
  color: PropTypes.oneOf(["primary", "info", "success", "warning", "danger"]),
  rtlActive: PropTypes.bool,
  handleDrawerToggle: PropTypes.func,
  routes: PropTypes.arrayOf(PropTypes.object)
};

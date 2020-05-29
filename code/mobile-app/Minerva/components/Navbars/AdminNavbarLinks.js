import React from "react";
import classNames from "classnames";

// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";
import MenuItem from "@material-ui/core/MenuItem";
import MenuList from "@material-ui/core/MenuList";
import Grow from "@material-ui/core/Grow";
import Paper from "@material-ui/core/Paper";
import ClickAwayListener from "@material-ui/core/ClickAwayListener";
import Hidden from "@material-ui/core/Hidden";
import Poppers from "@material-ui/core/Popper";
import Divider from "@material-ui/core/Divider";
// @material-ui/icons
import Person from "@material-ui/icons/Person";
import Notifications from "@material-ui/icons/Notifications";
import Dashboard from "@material-ui/icons/Dashboard";
import Search from "@material-ui/icons/Search";
// core components
import CustomInput from "components/CustomInput/CustomInput.js";
import Button from "components/CustomButtons/Button.js";

import styles from "assets/jss/material-dashboard-react/components/headerLinksStyle.js";
import global from "../../variables/global";
import { Redirect } from "react-router-dom";

const useStyles = makeStyles(styles);
export default function AdminNavbarLinks() {
  const [state,setState] = React.useState(false)

  const logout = e => {
    e.preventDefault();
    console.log("HI")
    console.log(global["token"]);  //Store our login token

  
    //Logout
    fetch(global["baseURL"] + "api/v1/logout", {
      method: "GET",
    })
      .then(response => {
        if (!response.ok) throw new Error(response.status);
        else return response;
      })
      .then(data => {        
        global["token"] = null;  //Reset our login info
        global["userInfo"] = null;  //Reset our logout info
      
        setState(true)
      })
      .catch(error => {
        console.log("error: " + error);
      });
  }


  const classes = useStyles();
  const [openNotification, setOpenNotification] = React.useState(null);
  const [openProfile, setOpenProfile] = React.useState(null);
  const handleClickNotification = event => {
    if (openNotification && openNotification.contains(event.target)) {
      setOpenNotification(null);
    } else {
      setOpenNotification(event.currentTarget);
    }
  };
  const handleCloseNotification = () => {
    setOpenNotification(null);
  };
  const handleClickProfile = event => {
    if (openProfile && openProfile.contains(event.target)) {
      setOpenProfile(null);
    } else {
      setOpenProfile(event.currentTarget);
    }
  };
  const handleCloseProfile = () => {
    setOpenProfile(null);
  };
  return (
    <div>

    </div>
  );
}

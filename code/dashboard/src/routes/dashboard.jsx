import Dashboard from "views/Dashboard/Dashboard.jsx";
import Notifications from "views/Notifications/Notifications.jsx";
import Icons from "views/Icons/Icons.jsx";
import Typography from "views/Typography/Typography.jsx";
import TableList from "views/TableList/TableList.jsx";
import UserPage from "views/UserPage/UserPage.jsx";


var dashRoutes = [
  {
    path: "/dashboard/",
    name: "Dashboard",
    icon: "fas fa-cube",
    component: Dashboard
  },
  {
    path: "/network",
    name: "Network",
    icon: "fas fa-network-wired",
    component: Notifications
  },
  {
    path: "/bots",
    name: "Bots",
    icon: "fas fa-robot",
    component: UserPage
  },
  {
    path: "/policies",
    name: "Policies",
    icon: "fas fa-list-alt",
    component: TableList
  },
  {
    path: "/instagram",
    name: "Instagram",
    icon: "fab fa-instagram",
    component: Typography
  },
  { redirect: true, path: "/", pathTo: "/dashboard", name: "Dashboard" }
];
export default dashRoutes;

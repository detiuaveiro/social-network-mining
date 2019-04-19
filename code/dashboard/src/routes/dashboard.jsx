import Dashboard from "views/Dashboard/Dashboard.jsx";
import Notifications from "views/Notifications/Notifications.jsx";
import Typography from "views/Typography/Typography.jsx";
import Policies from "views/Policies/Policies.jsx";
import UserPage from "views/UserPage/UserPage.jsx";
import BotsPage from "views/BotsPage/BotsPage.jsx";
import Test from "views/Test/Test.jsx"

var dashRoutes = [
  {
    path: "/dashboard/",
    name: "Dashboard",
    icon: "fas fa-cube",
    component: Dashboard,
    hide: false,
  },
  {
    path: "/network",
    name: "Network",
    icon: "fas fa-network-wired",
    component: Notifications,
    hide: false,
  },
  {
    path: "/bots/:botId",
    name: "Bots",
    icon: "fas fa-robot",
    component: UserPage,
    hide: true,
  },
  {
    path: "/bots",
    name: "Bots",
    icon: "fas fa-robot",
    component: BotsPage,
    hide: false,
  },
  {
    path: "/policies",
    name: "Policies",
    icon: "fas fa-list-alt",
    component: Policies,
    hide: false,
  },
  {
    path: "/instagram",
    name: "Instagram",
    icon: "fab fa-instagram",
    component: Typography,
    hide: false,
  },
  {
    path: "/test",
    name: "Test",
    icon: "fab fa-instagram",
    component: Test,
    hide: false,
  },
  { redirect: true, path: "/", pathTo: "/dashboard", name: "Dashboard" }
];
export default dashRoutes;

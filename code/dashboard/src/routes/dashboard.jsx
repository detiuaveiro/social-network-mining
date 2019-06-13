import Dashboard from "views/Dashboard/Dashboard.jsx";
import Typography from "views/Typography/Typography.jsx";
import Policies from "views/Policies/Policies.jsx";
import UserPage from "views/UserPage/UserPage.jsx";
import BotsPage from "views/BotsPage/BotsPage.jsx";
import TweetPage from "views/TweetPage/TweetPage.jsx";
import Tweets from "views/Tweets/Tweets.jsx";
import ExportData from "views/ExportData/ExportData.jsx";
import Network from "views/Network/Network";

var dashRoutes = [
  {
    path: "/dashboard",
    name: "Dashboard",
    icon: "fas fa-cube",
    component: Dashboard,
    hide: false,
  },
  {
    path: "/network",
    name: "Network",
    icon: "fas fa-network-wired",
    component: Network,
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
    path: "/tweets",
    name: "Tweets",
    icon: "fab fa-twitter",
    component: Tweets,
    hide: false,
  },
  {
    path: "/create_tweet",
    name: "Create Tweet",
    icon: "fas fa-quote-right",
    component: TweetPage,
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
    path: "/download",
    name: "Export Data",
    icon: "fas fa-save",
    component: ExportData,
    hide: false,
  },
  {
    path: "/instagram",
    name: "Instagram",
    icon: "fab fa-instagram",
    component: Typography,
    hide: false,
  },
  { redirect: true, path: "/", pathTo: "/dashboard", name: "Dashboard" }
];
export default dashRoutes;

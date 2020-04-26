import React from 'react';

const Breadcrumbs = React.lazy(() => import('./views/Base/Breadcrumbs'));
const Cards = React.lazy(() => import('./views/Base/Cards'));
const Carousels = React.lazy(() => import('./views/Base/Carousels'));
const Collapses = React.lazy(() => import('./views/Base/Collapses'));
const Dropdowns = React.lazy(() => import('./views/Base/Dropdowns'));
const Forms = React.lazy(() => import('./views/Base/Forms'));
const Jumbotrons = React.lazy(() => import('./views/Base/Jumbotrons'));
const ListGroups = React.lazy(() => import('./views/Base/ListGroups'));
const Navbars = React.lazy(() => import('./views/Base/Navbars'));
const Navs = React.lazy(() => import('./views/Base/Navs'));
const Paginations = React.lazy(() => import('./views/Base/Paginations'));
const Popovers = React.lazy(() => import('./views/Base/Popovers'));
const ProgressBar = React.lazy(() => import('./views/Base/ProgressBar'));
const Switches = React.lazy(() => import('./views/Base/Switches'));
const Tables = React.lazy(() => import('./views/Base/Tables'));
const Tabs = React.lazy(() => import('./views/Base/Tabs'));
const Tooltips = React.lazy(() => import('./views/Base/Tooltips'));
const BrandButtons = React.lazy(() => import('./views/Buttons/BrandButtons'));
const ButtonDropdowns = React.lazy(() => import('./views/Buttons/ButtonDropdowns'));
const ButtonGroups = React.lazy(() => import('./views/Buttons/ButtonGroups'));
const Buttons = React.lazy(() => import('./views/Buttons/Buttons'));
const Charts = React.lazy(() => import('./views/Charts'));
const Dashboard = React.lazy(() => import('./views/Dashboard'));
const CoreUIIcons = React.lazy(() => import('./views/Icons/CoreUIIcons'));
const Flags = React.lazy(() => import('./views/Icons/Flags'));
const FontAwesome = React.lazy(() => import('./views/Icons/FontAwesome'));
const SimpleLineIcons = React.lazy(() => import('./views/Icons/SimpleLineIcons'));
const Alerts = React.lazy(() => import('./views/Notifications/Alerts'));
const Badges = React.lazy(() => import('./views/Notifications/Badges'));
const Modals = React.lazy(() => import('./views/Notifications/Modals'));
const Colors = React.lazy(() => import('./views/Theme/Colors'));
const Typography = React.lazy(() => import('./views/Theme/Typography'));
const Widgets = React.lazy(() => import('./views/Widgets/Widgets'));

// Our Pages (delete everything before this before delivery)
const Bots = React.lazy(() => import('./views/Bots/Bots'));
const Policies = React.lazy(() => import('./views/Policies/Policies'));
const Network = React.lazy(() => import('./views/Network/Network'));
const Statistics = React.lazy(() => import('./views/Statistics/Statistics'));
const Reports = React.lazy(() => import('./views/Reports/Reports'));
const Users = React.lazy(() => import('./views/Users/Users'));


// https://github.com/ReactTraining/react-router/tree/master/packages/react-router-config
const routes = [
  { path: '/dash/home', name: 'Home', component: Dashboard},
  { path: '/dash/theme', exact: true, name: 'Theme', component: Colors },
  { path: '/dash/theme/colors', name: 'Colors', component: Colors },
  { path: '/dash/theme/typography', name: 'Typography', component: Typography },
  { path: '/dash/base', exact: true, name: 'Base', component: Cards },
  { path: '/dash/base/cards', name: 'Cards', component: Cards },
  { path: '/dash/base/forms', name: 'Forms', component: Forms },
  { path: '/dash/base/switches', name: 'Switches', component: Switches },
  { path: '/dash/base/tables', name: 'Tables', component: Tables },
  { path: '/dash/base/tabs', name: 'Tabs', component: Tabs },
  { path: '/dash/base/breadcrumbs', name: 'Breadcrumbs', component: Breadcrumbs },
  { path: '/dash/base/carousels', name: 'Carousel', component: Carousels },
  { path: '/dash/base/collapses', name: 'Collapse', component: Collapses },
  { path: '/dash/base/dropdowns', name: 'Dropdowns', component: Dropdowns },
  { path: '/dash/base/jumbotrons', name: 'Jumbotrons', component: Jumbotrons },
  { path: '/dash/base/list-groups', name: 'List Groups', component: ListGroups },
  { path: '/dash/base/navbars', name: 'Navbars', component: Navbars },
  { path: '/dash/base/navs', name: 'Navs', component: Navs },
  { path: '/dash/base/paginations', name: 'Paginations', component: Paginations },
  { path: '/dash/base/popovers', name: 'Popovers', component: Popovers },
  { path: '/dash/base/progress-bar', name: 'Progress Bar', component: ProgressBar },
  { path: '/dash/base/tooltips', name: 'Tooltips', component: Tooltips },
  { path: '/dash/buttons', exact: true, name: 'Buttons', component: Buttons },
  { path: '/dash/buttons/buttons', name: 'Buttons', component: Buttons },
  { path: '/dash/buttons/button-dropdowns', name: 'Button Dropdowns', component: ButtonDropdowns },
  { path: '/dash/buttons/button-groups', name: 'Button Groups', component: ButtonGroups },
  { path: '/dash/buttons/brand-buttons', name: 'Brand Buttons', component: BrandButtons },
  { path: '/dash/icons', exact: true, name: 'Icons', component: CoreUIIcons },
  { path: '/dash/icons/coreui-icons', name: 'CoreUI Icons', component: CoreUIIcons },
  { path: '/dash/icons/flags', name: 'Flags', component: Flags },
  { path: '/dash/icons/font-awesome', name: 'Font Awesome', component: FontAwesome },
  { path: '/dash/icons/simple-line-icons', name: 'Simple Line Icons', component: SimpleLineIcons },
  { path: '/dash/notifications', exact: true, name: 'Notifications', component: Alerts },
  { path: '/dash/notifications/alerts', name: 'Alerts', component: Alerts },
  { path: '/dash/notifications/badges', name: 'Badges', component: Badges },
  { path: '/dash/notifications/modals', name: 'Modals', component: Modals },
  { path: '/dash/widgets', name: 'Widgets', component: Widgets },
  { path: '/dash/charts', name: 'Charts', component: Charts },
  
  // Our Pages (delete everything before this before delivery)
  { path: '/dash/bots', name: 'Bots', component: Bots },
  { path: '/dash/users', name: 'Users', component: Users },
  { path: '/dash/policies', name: 'Policies', component: Policies },
  { path: '/dash/network', name: 'Network', component: Network },
  { path: '/dash/statistics', name: 'Statistics', component: Statistics },
  { path: '/dash/reports', name: 'Reports', component: Reports },

];

export default routes;

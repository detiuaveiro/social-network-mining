import React, { Component } from 'react';
import { createBrowserHistory } from "history";
import { Router, Route, Switch, Redirect } from "react-router-dom";
// import { renderRoutes } from 'react-router-config';
import './App.scss';

const loading = () => <div className="animated fadeIn pt-3 text-center">Loading...</div>;

// Containers
const DefaultLayout = React.lazy(() => import('./containers/DefaultLayout'));
const LandingLayout = React.lazy(() => import('./containers/LandingPageLayout'));

// Pages
const Page404 = React.lazy(() => import('./views/Pages/Page404'));
const Page500 = React.lazy(() => import('./views/Pages/Page500'));

const hist = createBrowserHistory();

class App extends Component {

  render() {
    return (
      <Router history={hist}>
          <React.Suspense fallback={loading()}>
            <Switch>
              <Route exact path="/" name="Home" render={props => <LandingLayout {...props}/>} />

              <Route path="/404" name="Page 404" render={props => <Page404 {...props}/>} />
              <Route path="/500" name="Page 500" render={props => <Page500 {...props}/>} />
              <Route path="/dash" name="Dashboard" render={props => <DefaultLayout {...props}/>} />
            </Switch>
          </React.Suspense>
      </Router>
    );
  }
}

export default App;

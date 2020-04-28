import React, { Component, Suspense } from "react";
import { Redirect, Route, Switch } from "react-router-dom";
import * as router from "react-router-dom";
import { Container } from "reactstrap";

import logo from "../../assets/img/brand/logo_white.png";

import {
  AppAside,
  AppFooter,
  AppHeader,
  AppNavbarBrand,
  AppSidebar,
  AppSidebarFooter,
  AppSidebarForm,
  AppSidebarHeader,
  AppSidebarMinimizer,
  AppBreadcrumb2 as AppBreadcrumb,
  AppSidebarNav2 as AppSidebarNav
} from "@coreui/react";

import { MobileView, BrowserView } from "react-device-detect";

// sidebar nav config
import navigation from "../../_nav";
// routes config
import routes from "../../routes";


import FadeIn from "react-fade-in";
import Lottie from "react-lottie";

import * as loadingAnim from "../../assets/animations/squares_1.json";

const DefaultFooter = React.lazy(() => import("./DefaultFooter"));
const DefaultHeader = React.lazy(() => import("./DefaultHeader"));

class DefaultLayout extends Component {
  options = {
    loop: true, autoplay: true, animationData: loadingAnim.default, rendererSettings: {
      preserveAspectRatio: "xMidYMid slice"
    }
  }

  loading = () => (
    <div className="animated fadeIn pt-1 text-center">
      <div style={{ width: "100%", marginTop: "10%" }}>
        <FadeIn>
          <Lottie options={this.options} height={"30%"} width={"30%"} />
        </FadeIn>
      </div>
    </div>
  );

  render() {
    return (
      <div className="app">
        <MobileView>
          <AppHeader fixed>
            <Suspense fallback={this.loading()}>
              <DefaultHeader />
            </Suspense>
          </AppHeader>
        </MobileView>
        <div className="app-body">
          <AppSidebar fixed display="lg">
            <AppSidebarHeader>
              <BrowserView>
                <AppNavbarBrand
                  full={{
                    src: logo,
                    width: 120,
                    height: 103,
                    alt: "Logo"
                  }}
                />
              </BrowserView>
            </AppSidebarHeader>
            <AppSidebarForm />
            <Suspense>
              <AppSidebarNav
                navConfig={navigation}
                {...this.props}
                router={router}
              />
            </Suspense>
            <AppSidebarFooter />
            <AppSidebarMinimizer />
          </AppSidebar>
          <main className="main">
            <AppBreadcrumb appRoutes={routes} router={router} />
            <Container fluid>
              <Suspense fallback={this.loading()}>
                <Switch>
                  {routes.map((route, idx) => {
                    return route.component ? (
                      <Route
                        key={idx}
                        path={route.path}
                        exact={route.exact}
                        name={route.name}
                        render={props => <route.component {...props} />}
                      />
                    ) : null;
                  })}
                  <Redirect from="/" to="/dash/home" />
                </Switch>
              </Suspense>
            </Container>
          </main>
        </div>
        <AppFooter>
          <Suspense fallback={this.loading()}>
            <DefaultFooter />
          </Suspense>
        </AppFooter>
      </div>
    );
  }
}

export default DefaultLayout;

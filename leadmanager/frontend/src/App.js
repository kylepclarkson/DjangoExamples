import React, { Component, Fragment, useEffect } from "react";

import { Provider as AlertProvider } from "react-alert";
import AlertTemplate from "react-alert-template-basic";
import { Provider } from "react-redux";
import {
  HashRouter as Router,
  Route,
  Switch,
  Redirect,
} from "react-router-dom";

import { loadUser } from './actions/auth'

import store from "./store";
import Header from "./components/layout/Header";
import Dashboard from "./components/leads/Dashboard";
import Alerts from "./components/layout/Alerts";
import Login from './components/accounts/Login'
import Register from './components/accounts/Register'
import PrivateRoute from './components/common/PrivateRoute'

// Alert options
const alertOptions = {
  timeout: 3000,
  position: "top center",
};


function App() {
  
  useEffect(() => {
    store.dispatch(loadUser());
  })


  return (
    // Redux store.
    <Provider store={store}>
      <AlertProvider template={AlertTemplate} {...alertOptions}>
        <Router>
          <Fragment>
            <Header />
            <Alerts />
            <div className="container">
              <Switch>
                <PrivateRoute exact path="/" component={Dashboard} />
                <Route exact path="/register" component={Register} />
                <Route exact path="/login" component={Login} />
              </Switch>
            </div>
          </Fragment>
        </Router>
      </AlertProvider>
    </Provider>
  );
}

export default App;

import React, { Component, Fragment } from "react";

import { Provider as AlertProvider } from "react-alert";
import AlertTemplate from "react-alert-template-basic";
import { Provider } from "react-redux";
import store from "./store";

import Header from "./components/layout/Header";
import Dashboard from "./components/leads/Dashboard";
import Alerts from "./components/layout/Alerts";

// Alert options
const alertOptions = {
  timeout: 3000,
  position: "top center",
};

function App() {
  return (
    // Redux store.
    <Provider store={store}>
      <AlertProvider template={AlertTemplate} {...alertOptions}>
        <Fragment>
          <Header />
          <Alerts />
          <div className="container">
            <Dashboard />
          </div>
        </Fragment>
      </AlertProvider>
    </Provider>
  );
}

export default App;

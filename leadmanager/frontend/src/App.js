import React, { Component, Fragment } from "react";

import { Provider } from "react-redux";
import store from "./store";

import Header from "./components/layout/Header";
import Dashboard from "./components/leads/Dashboard";

function App() {
  return (
    // Redux store. 
    <Provider store={store}> 
      <Fragment>
        <Header />
        <div className="container">
          <Dashboard />
        </div>
      </Fragment>
    </Provider>
  );
}

export default App;

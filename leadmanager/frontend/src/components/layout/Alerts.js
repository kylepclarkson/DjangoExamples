import React, { Component, Fragment } from "react";
import { withAlert } from "react-alert";
import { connect } from "react-redux";
import PropTypes from "prop-types";

// Displays messages to user. 

export class Alerts extends Component {
  static propTypes = {
    error: PropTypes.object.isRequired,
    message: PropTypes.object.isRequired,
  };

  componentDidUpdate(prevProps) {
    const { error, alert, message } = this.props;
    // check that a new error has occurred.
    if (error !== prevProps.error) {
      if (error.msg.name) {
        alert.error(`Name: ${error.msg.name.join()}`);
      }
      if (error.msg.email) {
        alert.error(`Name: ${error.msg.email.join()}`);
      }
      if (error.msg.message) {
        alert.error(`Name: ${error.msg.message.join()}`);
      }
      if (error.msg.non_field_errors) {
        alert.error(error.msg.non_field_errors.join());
      }
      if (error.msg.username) {
        alert.error(error.msg.username.join())
      }
    }

    if (message !== prevProps.message) {
      if (message.deleteLead) {
        alert.success(message.deleteLead);
      }
      if (message.addLead) {
          alert.success(message.addLead);
      }
      if (message.passwordsNotMatch) {
        alert.error(message.passwordsNotMatch)
      }
    }
  }

  render() {
    return <Fragment />;
  }
}

const mapStateToProps = (state) => ({
  error: state.errors,
  message: state.messages,
});

export default connect(mapStateToProps)(withAlert()(Alerts));

import React, { Component } from "react";
import {connect} from 'react-redux'
import PropTypes from 'prop-types'
import { addLead } from '../../actions/leads'

export class Form extends Component {
  state = {
    name: "",
    email: "",
    message: "",
  };

  static propTypes = {
      addLead: PropTypes.func.isRequired
  } 

  onChange = (e) =>
    this.setState({
      [e.target.name]: e.target.value,
    });

  onSubmit = (e) => {
    e.preventDefault();
    // create lead and call server
    const { name, email, message } = this.state;
    const lead = { name, email, message }
    console.log('constructing lead', lead)
    this.props.addLead(lead);
    this.setState({
      name: "",
      email: "",
      message: ""
    })
  };

  render() {
    const { name, email, message } = this.state;
    return (
      <div className="card card-body my-4">
        <h2>Add Lead</h2>
        <form onSubmit={this.onSubmit}>
          <div className="form-group">
            <label>Name</label>
            <input
              type="text"
              name="name"
              onChange={this.onChange}
              value={this.state.name}
              className="form-control"
            />
            <label>Email</label>
            <input
              type="email"
              name="email"
              onChange={this.onChange}
              value={this.state.email}
              className="form-control"
            />
            <label>Message</label>
            <input
              type="text"
              name="message"
              onChange={this.onChange}
              value={this.state.message}
              className="form-control"
            />
          </div>
          <div className="form-group">
            <button
              className="btn btn-primary mt-2"
              type="submit"
              onSubmit={this.onSubmit}
            >
              Submit
            </button>
          </div>
        </form>
      </div>
    );
  }
}

export default connect(null, { addLead })(Form);

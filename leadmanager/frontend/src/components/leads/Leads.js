import React, { Component, Fragment } from "react";
import { connect } from "react-redux";
import PropTypes from "prop-types";

import { getLeads, deleteLead } from "../../actions/leads";

export class Leads extends Component {
  static propTypes = {
    leads: PropTypes.array.isRequired,
    getLeads: PropTypes.func.isRequired,
    deleteLead: PropTypes.func.isRequired,
  };

  componentDidMount() {
    this.props.getLeads();
  }

  render() {
    return (
      <Fragment>
        <h2>Leads</h2>
        <table className="table table-striped">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Message</th>
              <th />
            </tr>
          </thead>
          <tbody>
            {this.props.leads.map((lead) => (
              <tr key={lead.id}>
                <td>{lead.id}</td>
                <td>{lead.name}</td>
                <td>{lead.email}</td>
                <td>{lead.message}</td>
                <td>
                  <button 
                    className="btn btn-danger btn-sm mt-2"
                    onClick={this.props.deleteLead.bind(this, lead.id)}
                  >Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </Fragment>
    );
  }
}

// brings leads back in. 
const mapStateToProps = (state) => ({
  // state.leads -> reducer.
  // state.leads.leads -> value of leads in reducer.
  leads: state.leads.leads,
});

// need to wrap leads with connect. Call add functions for calling functions. .
export default connect(mapStateToProps, { getLeads, deleteLead })(Leads);

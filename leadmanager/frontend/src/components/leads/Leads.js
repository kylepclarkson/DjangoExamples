import React, { Component } from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { getLeads } from '../../actions/leads'

export class Leads extends Component {

    static propTypes = {
        leads: PropTypes.array.isRequired
    }

    componentDidMount() {
        this.props.getLeads();
    }

    render() {
        return (
            <div>
                <h1>Leads List</h1>
            </div>
        )
    }
}

// map 'redux state' to the props of component.
// state.leads -> reducer. Get leads from this reducer.
const mapStateToProps = state => ({
    leads: state.leads.leads
})

// export connect, passing Leads
export default connect(mapStateToProps, { getLeads })(Leads);
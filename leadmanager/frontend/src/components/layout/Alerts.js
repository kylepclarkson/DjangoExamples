import React, { Component, Fragment } from 'react'
import { withAlert } from 'react-alert'
import { connect } from 'react-redux'
import PropTypes from 'prop-types'

export class Alerts extends Component {
    
    static propTypes = {
        error: PropTypes.object.isRequired,
    }

    componentDidUpdate(prevProps) {
        // check if new message needs to be displayed
        const { error, alert, message } = this.props;
        if (error !== prevProps.error) {
            if (error.msg.name)
                alert.error('Name is required')
            
        }
    }

    render() {
        return <Fragment />
    }
}

// convert redux state to props.
const mapStateToProps = state => ({
    error: state.errors,
    message: state.messages
}) 

export default connect(mapStateToProps)(withAlert()(Alerts))
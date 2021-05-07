import React, { Component } from 'react'

/**
 *  The room in which users can vote on controls.
 */

export default class Room extends Component {
    constructor(props) {
        super(props)

        this.state = {
            votesToSkip: 2,
            guestCanPause: false,
            isHost: false,
        }
        // Get roomCode from Router
        this.roomCode = this.props.match.params.roomCode;
        this.getRoomDetails();
    }

    // get Room details from api and set to state
    getRoomDetails() {
        fetch(`/api/get-room?code=${this.roomCode}`)
        .then((response) => response.json())
        .then((data) => {
            this.setState({
                votesToSkip: data.votes_to_skip,
                guestCanPause: data.guest_can_pause,
                isHost: data.is_host
            })
        })
        
    }

    render() {
        return (
            <div>
                <h3>{this.roomCode}</h3>
                <p>Votes: {this.state.votesToSkip.toString()}</p>
                <p>Guest Can Pause: {this.state.guestCanPause.toString()}</p>
                <p>Is host: {this.state.isHost.toString()}</p>
            </div>
        )
    }
}
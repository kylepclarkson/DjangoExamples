import React, { Component } from 'react'

import { Button, Grid, Typography, TextField, FormHelperText, FormControl, Radio, RadioGroup, FormControlLabel } from "@material-ui/core"
import { Link } from "react-router-dom"

export class CreateRoomPage extends Component {
    
    defaultVotes = 2;

    constructor(props) {
        super(props)
        this.state = {
            guestCanPause: true,
            votesToSkip: this.defaultVotes,
        }

        this.handleVotesChange = this.handleVotesChange.bind(this)
        this.handleGuestCanPauseChange = this.handleGuestCanPauseChange.bind(this)
        this.handleRoomButtonPressed = this.handleRoomButtonPressed.bind(this)
    }

    // Update state
    handleVotesChange(e) {
        this.setState({
            votesToSkip: e.target.value,
        })
    } 
    handleGuestCanPauseChange(e) {
        this.setState({
            guestCanPause: e.target.value === 'true' ? true : false
        })
    }

    // submit room data to backend.
    handleRoomButtonPressed() {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                votes_to_skip: this.state.votesToSkip,
                guest_can_pause: this.state.guestCanPause,
            }),
        };

        // send to server, get response, convert to json, and log.
        fetch('/api/create-room', requestOptions)
        .then((response) => response.json())
        // redirect to room once created.
        .then((data) => this.props.history.push('/room/' + data.code))
    }
    
    render() {
        return (
            <Grid container spacing={1}>
                <Grid item xs={12} align="center">
                    <Typography component="h4" variant="h4">
                        Create A Room
                    </Typography>
                </Grid>
                <Grid item xs={12} align="center">
                    <FormControl component="fieldset">
                        <FormHelperText>
                            <div align='center'>
                                Guest Control of Playback
                            </div>    
                        </FormHelperText>
                        <RadioGroup row defaultValue="true" onChange={this.handleGuestCanPauseChange}>
                            <FormControlLabel 
                                value="true" 
                                control={<Radio color="primary" />} 
                                label="Play/Pause"
                                labelPlacement="bottom"/>
                            <FormControlLabel 
                                value="false" 
                                control={<Radio color="secondary" />} 
                                label="No Control"
                                labelPlacement="bottom"/>
                        </RadioGroup>
                    </FormControl>    
                </Grid>
                <Grid item xs={12} align="center">
                    <FormControl>
                        <TextField 
                            required={true} 
                            type="number" 
                            onChange={this.handleVotesChange}
                            defaultValue={this.defaultVotes} 
                            inputProps={{
                                min: 1,
                                style: { textAlign: "center"}
                            }} />
                        <FormHelperText>
                            <div algin="center">
                                Votes Required to Skip Song
                            </div>
                        </FormHelperText>
                    </FormControl>
                </Grid>
                <Grid item xs={12} align="center">
                    <Button color="primary" variant="contained" onClick={this.handleRoomButtonPressed}>Create A Room</Button>
                </Grid>
                <Grid item xs={12} align="center">
                    <Button color="secondary" variant="contained" to="/" component={Link}>Back</Button>
                </Grid>
            </Grid>
        )
    }
}

export default CreateRoomPage


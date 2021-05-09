import React, { Component } from "react";

import {
  Button,
  Grid,
  Typography,
  TextField,
  FormHelperText,
  FormControl,
  Radio,
  RadioGroup,
  FormControlLabel,
} from "@material-ui/core";
import { Link } from "react-router-dom";
import { Collapse } from "@material-ui/core"
import Alert from "@material-ui/lab/Alert";

export class CreateRoomPage extends Component {
  // default props
  static defaultProps = {
    votesToSkip: 2,
    guestCanPause: true,
    update: false,
    roomCode: null,
    updateCallback: () => {},
  };

  constructor(props) {
    super(props);
    this.state = {
      guestCanPause: this.props.guestCanPause,
      votesToSkip: this.props.votesToSkip,
      successMsg: "",
      errorMsg: "",
    };

    this.handleVotesChange = this.handleVotesChange.bind(this);
    this.handleGuestCanPauseChange = this.handleGuestCanPauseChange.bind(this);
    this.handleRoomButtonPressed = this.handleRoomButtonPressed.bind(this);
    this.handleUpdateButtonPressed = this.handleUpdateButtonPressed.bind(this);
  }

  // Update state
  handleVotesChange(e) {
    this.setState({
      votesToSkip: e.target.value,
    });
  }
  handleGuestCanPauseChange(e) {
    this.setState({
      guestCanPause: e.target.value === "true" ? true : false,
    });
  }

  // submit room data to backend.
  handleRoomButtonPressed() {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        votes_to_skip: this.state.votesToSkip,
        guest_can_pause: this.state.guestCanPause,
      }),
    };

    // send to server, get response, convert to json, and log.
    fetch("/api/create-room", requestOptions)
      .then((response) => response.json())
      // redirect to room once created.
      .then((data) => this.props.history.push("/room/" + data.code));
  }

  // submit room updated data to backend. 
  handleUpdateButtonPressed() {
    const requestOptions = {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        votes_to_skip: this.state.votesToSkip,
        guest_can_pause: this.state.guestCanPause,
        code: this.props.roomCode
      }),
    };

    // send to server, get response, convert to json, and log.
    fetch("/api/update-room", requestOptions)
      .then((response) => {
          if (response.ok) {
            this.setState({
                successMsg: "Room updated successfully!"
            })
          } else {
              this.setState({
                  errorMsg: "Error updating room."
              })
          }
          // Update display.
          this.props.updateCallback();
      })
  }

  renderCreateButtons() {
    return (
      <Grid container spacing={1}>
        <Grid item xs={12} align="center">
          <Button
            color="primary"
            variant="contained"
            onClick={this.handleRoomButtonPressed}
          >
            Create A Room
          </Button>
        </Grid>
        <Grid item xs={12} align="center">
          <Button color="secondary" variant="contained" to="/" component={Link}>
            Back
          </Button>
        </Grid>
      </Grid>
    );
  }

  renderUpdateButtons() {
    return (
      <Grid item xs={12} align="center">
        <Button
          color="primary"
          variant="contained"
          onClick={this.handleUpdateButtonPressed}
        >
          Update Room
        </Button>
      </Grid>
    );
  }


  render() {
    const title = this.props.update ? "Update Room" : "Create a Room";

    return (
      <Grid container spacing={1}>
          <Grid item xs={12} align="center">
              {/* Display message if it is present */}
              <Alert severity="error">This is an error alert — check it out!</Alert>
              <Collapse 
                in={this.state.errorMsg != "" || this.state.successMsg != ""}>
                {this.state.successMsg != "" ? (
                    <Alert 
                    severity="success" 
                        onClose={() => {this.setState({ successMsg: "" })}}>
                        {this.state.successMsg}
                    </Alert>
                    ) : (
                    <Alert 
                    severity="error" 
                        onClose={() => {this.setState({ errorMsg: "" })}}>
                        {this.state.errorMessage}
                    </Alert>
                )}
              </Collapse>
          </Grid>
        <Grid item xs={12} align="center">
          <Typography component="h4" variant="h4">
            {title}
          </Typography>
        </Grid>
        <Grid item xs={12} align="center">
          <FormControl component="fieldset">
            <FormHelperText>
              <div align="center">Guest Control of Playback</div>
            </FormHelperText>
            <RadioGroup
              row
              defaultValue="true"
              onChange={this.handleGuestCanPauseChange}
            >
              <FormControlLabel
                value="true"
                control={<Radio color="primary" />}
                label="Play/Pause"
                labelPlacement="bottom"
              />
              <FormControlLabel
                value="false"
                control={<Radio color="secondary" />}
                label="No Control"
                labelPlacement="bottom"
              />
            </RadioGroup>
          </FormControl>
        </Grid>
        <Grid item xs={12} align="center">
          <FormControl>
            <TextField
              required={this.props.guestCanPause.toString()}
              type="number"
              onChange={this.handleVotesChange}
              defaultValue={this.state.votesToSkip}
              inputProps={{
                min: 1,
                style: { textAlign: "center" },
              }}
            />
            <FormHelperText>
              <div algin="center">Votes Required to Skip Song</div>
            </FormHelperText>
          </FormControl>
        </Grid>
        {this.props.update ? this.renderUpdateButtons() : this.renderCreateButtons()}
      </Grid>
    );
  }
}

export default CreateRoomPage;

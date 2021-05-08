import React, { Component } from 'react'

import { Grid, Button, ButtonGroup, Typography } from "@material-ui/core"
import { BrowserRouter as Router, Switch, Route, Link, Redirect } from 'react-router-dom';

import RoomJoinPage from "./RoomJoinPage"
import CreateRoomPage from "./CreateRoomPage"
import Room from "./Room"

export class HomePage extends Component {
    
    constructor(props) {
        super(props)
        this.state = {
            roomCode: null,
        }

        // this.renderHomePage = this.renderHomePage.bind(this)
    }

    async componentDidMount() {
        // call api to check if user is currently in a room.
        fetch('/api/user-in-room')
        .then((response) => response.json())
        .then((data) => {
            this.setState({
                roomCode: data.code // will be null if not in room.
            })
        })
    }

    renderHomePage() {
        console.log("render")
        return (
            <Grid container spacing={3}>
                <Grid item xs={12} align="center"> 
                    <Typography
                        variant="h3"
                        component="h3"
                    >
                        House Party!
                    </Typography>
                </Grid>
                <Grid item xs={12} align="center"> 
                    <ButtonGroup disableElevation variant="contained" color="primary">
                        <Button color="primary" to="/join" component={ Link }>Join a Room</Button>
                        <Button color="secondary" to="/create" component={ Link }>Create a Room</Button>
                    </ButtonGroup>
                </Grid>
            </Grid>
        );
    }
    
    render() {
        return (
            <Router>
                <Switch>
                    {/* Render home page if not in room, else redirect to room. */}
                    <Route exact path='/' render={() => {
                        return this.state.roomCode ? ( <Redirect to={`/room/${this.state.roomCode}`}/> ) : (this.renderHomePage());
                    }}>
                    </Route>
                    {/* Need to add to both React and Django */}
                    <Route path='/join' component={RoomJoinPage} />
                    <Route path='/create' component={CreateRoomPage} />
                    <Route path='/room/:roomCode' component={Room} />
                    
                </Switch>
            </Router>
        )
    }
}

export default HomePage


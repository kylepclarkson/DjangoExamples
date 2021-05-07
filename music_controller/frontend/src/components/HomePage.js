import React, { Component } from 'react'

import { BrowserRouter as Router, Switch, Route, Link, Redirect } from 'react-router-dom';

import RoomJoinPage from "./RoomJoinPage"
import CreateRoomPage from "./CreateRoomPage"

export class HomePage extends Component {
    
    constructor(props) {
        super(props)
    }
    
    render() {
        return (
            <Router>
                <Switch>
                    {/* Need to add to both React and Django */}
                    <Route path='/join' component={RoomJoinPage} />
                    <Route path='/create' component={CreateRoomPage} />
                    <Route exact path='/'> <p>This is the home page</p></Route>
                </Switch>
            </Router>
        )
    }
}

export default HomePage


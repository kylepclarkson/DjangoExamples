// actions that we fire off (make http requests.)

import axios from 'axios';

import { createMessage, returnErrors } from './messages'
import { GET_LEADS, DELETE_LEAD, ADD_LEAD } from './types'

import { tokenConfig } from './auth'

// GET LEADS
// The function to get all leads.
export const getLeads = () => (dispatch, getState) => {
    axios.get('http://localhost:8000/api/leads/', tokenConfig(getState))
    .then(res => {
        // dispatch to reducer
        console.log(res.data)
        dispatch({
            type: GET_LEADS,
            payload: res.data
        })
    })
    .catch(err =>  dispatch(returnErrors(err.response.data, err.response.status)))
}

// DELETE LEAD
// The function to delete a lead. 
export const deleteLead = (id) => (dispatch, getState) => {
    axios.delete(`http://localhost:8000/api/leads/${id}`, tokenConfig(getState))
    .then(res => {
        // dispatch to reducer
        console.log(res.data)
        // call createMessage
        dispatch(createMessage({
            deleteLead: 'Lead Deleted'
        }))
        dispatch({
            type: DELETE_LEAD,
            payload: id
        })
    })
    .catch(err => console.log(err))
}

// ADD LEAD
// Create a new lead from the form. 
export const addLead = (lead) => (dispatch, getState) => {
    axios.post('http://localhost:8000/api/leads/', lead,  tokenConfig(getState))
    .then(res => {
        // dispatch to reducer
        console.log(res.data)
        // call createMessage
        dispatch(createMessage({
            addLead: 'Lead Added'
        }))
        dispatch({
            type: ADD_LEAD,
            payload: res.data
        })
    })
    .catch(err => dispatch(returnErrors(err.response.data, err.response.status)))
}

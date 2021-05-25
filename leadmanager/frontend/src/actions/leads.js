// actions that we fire off (make http requests.)

import axios from 'axios';

import { GET_LEADS, DELETE_LEAD, ADD_LEAD } from './types'

// GET LEADS
// The function to get all leads.
export const getLeads = () => dispatch => {
    axios.get('http://localhost:8000/api/leads/')
    .then(res => {
        // dispatch to reducer
        console.log(res.data)
        dispatch({
            type: GET_LEADS,
            payload: res.data
        })
    })
    .catch(err => console.log(err))
}

// DELETE LEAD
// The function to delete a lead. 
export const deleteLead = (id) => dispatch => {
    axios.delete(`http://localhost:8000/api/leads/${id}`)
    .then(res => {
        // dispatch to reducer
        console.log(res.data)
        dispatch({
            type: DELETE_LEAD,
            payload: id
        })
    })
    .catch(err => console.log(err))
}

// ADD LEAD
// Create a new lead from the form. 
export const addLead = (lead) => dispatch => {
    console.log('add lead')
    axios.post('http://localhost:8000/api/leads/', lead)
    .then(res => {
        // dispatch to reducer
        console.log(res.data)
        dispatch({
            type: ADD_LEAD,
            payload: res.data
        })
    })
    .catch(err => console.log(err))
}

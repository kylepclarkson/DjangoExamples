// leads actions

import axios from 'axios';
import { GET_LEADS, DELETE_LEAD, ADD_LEAD, GET_ERRORS } from './types'

// GET LEADS
export const getLeads = () => dispatch => {
    axios.get('/api/leads/')
    .then(res => {
        // pass to reducer
        dispatch({
            type: GET_LEADS,
            payload: res.data
        });
    })
    .catch(err => console.log(err))
}

// ADD LEADS
export const addLead = (lead) => dispatch => {
    axios.post('/api/leads/', lead)
    .then(res => {
        // pass to reducer
        dispatch({
            type: ADD_LEAD,
            payload: res.data
        });
    })
    .catch(err => {
        console.log('error: ', err)
        const errors = {
            msg: err.response.data,
            status: err.response.status
        }
        dispatch({
            type: GET_ERRORS,
            payload: errors
        })
    })
}

// DELETE LEAD
export const deleteLead = (id) => dispatch => {
    axios.delete(`/api/leads/${id}/`)
    .then(res => {
        // pass to reducer
        dispatch({
            type: DELETE_LEAD,
            payload: id
        });
    })
    .catch(err => console.log(err))
}


// leads actions

import axios from 'axios';
import { GET_LEADS } from './types'

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

// combine all reducers

import { combineReducers } from 'redux'
import leads from './leads'

export default combineReducers({
    leads: leads,
});


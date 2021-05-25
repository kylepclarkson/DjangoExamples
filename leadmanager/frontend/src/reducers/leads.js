import { DELETE_LEAD, GET_LEADS, ADD_LEAD } from "../actions/types.js";

// Leads state

const initialState = {
  leads: [],
};

export default function (state = initialState, action) {
  // return appropriate state
  switch (action.type) {
    case GET_LEADS:
      return {
        ...state,
        leads: action.payload,
      };

    case DELETE_LEAD:
      return {
          ...state,
          leads: state.leads.filter(lead => lead.id !== action.payload) // return all leads, excluding that which is deleted. 
      };

    case ADD_LEAD:
      return {
          ...state,
          leads: [...state.leads, action.payload] // Add new lead to existing leads in list. 
      };

    default:
      return state;
  }
}

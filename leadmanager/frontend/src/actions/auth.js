import axios from "axios";

import {
  USER_LOADED,
  USER_LOADING,
  AUTH_ERROR,
  LOGIN_SUCCESS,
  LOGIN_FAIL,
  LOGOUT_SUCCESS,
  REGISTER_SUCCESS,
  REGISTER_FAIL
} from "./types";

import { returnErrors } from "./messages";

// CHECK TOKEN AND LOAD USER
export const loadUser = () => (dispatch, getState) => {
  // user loading
  dispatch({
    type: USER_LOADING,
  });

  axios
    .get("http://127.0.0.1:8000/api/auth/user", tokenConfig(getState))
    .then((res) => {
      dispatch({
        type: USER_LOADED,
        payload: res.data,
      });
    })
    .catch((err) => {
      // Not auth
      dispatch(returnErrors(err.response.data, err.response.status));
      dispatch({
        type: AUTH_ERROR,
      });
    });
};

// LOGIN USER
export const login = (username, password) => (dispatch) => {
  // Header
  const config = {
    headers: {
      "Content-Type": "application/json",
    },
  };

  // Body
  const body = JSON.stringify({
    username,
    password,
  });

  axios
    .post("http://127.0.0.1:8000/api/auth/login", body, config)
    .then((res) => {
      dispatch({
        type: LOGIN_SUCCESS,
        payload: res.data,
      });
    })
    .catch((err) => {
      // Not auth
      dispatch(returnErrors(err.response.data, err.response.status));
      dispatch({
        type: LOGIN_FAIL,
      });
    });
};


// LOGOUT USER
export const logout = () => (dispatch, getState) => {
  
  // null body
  axios
    .post("http://127.0.0.1:8000/api/auth/logout", null, tokenConfig(getState))
    .then((res) => {
      dispatch({
        type: LOGOUT_SUCCESS,
      });
    })
    .catch((err) => {
      // Not auth
      dispatch(returnErrors(err.response.data, err.response.status));
    });
};

// REGISTER USER
export const register = ({ username, password, email }) => (dispatch) => {
    // Header
    const config = {
      headers: {
        "Content-Type": "application/json",
      },
    };
    // Body
    const body = JSON.stringify({ username, password, email,});
  
    axios
      .post("http://127.0.0.1:8000/api/auth/register", body, config)
      .then((res) => {
        dispatch({
          type: REGISTER_SUCCESS,
          payload: res.data,
        });
      })
      .catch((err) => {
        // Not auth
        dispatch(returnErrors(err.response.data, err.response.status));
        dispatch({
          type: REGISTER_FAIL,
        });
      });
  };


// Helper function
// Setup config with token
export const tokenConfig = getState => {
    // get token from state.
  const token = getState().auth.token;

  // Header
  const config = {
    headers: {
      "Content-Type": "application/json",
    },
  };

  // Add token to headers
  if (token) {
    config.headers["Authorization"] = `Token ${token}`;
  }
  return config
}

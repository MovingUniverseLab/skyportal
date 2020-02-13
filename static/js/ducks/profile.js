import messageHandler from 'baselayer/MessageHandler';

import * as API from '../API';


export const FETCH_USER_PROFILE = 'skyportal/FETCH_USER_PROFILE';
export const FETCH_USER_PROFILE_OK = 'skyportal/FETCH_USER_PROFILE_OK';

export const GENERATE_TOKEN = 'skyportal/GENERATE_TOKEN';
export const GENERATE_TOKEN_OK = 'skyportal/GENERATE_TOKEN_OK';

export const DELETE_TOKEN = 'skyportal/DELETE_TOKEN';
export const DELETE_TOKEN_OK = 'skyportal/DELETE_TOKEN_OK';


export function fetchUserProfile() {
  return API.GET('/api/internal/profile', FETCH_USER_PROFILE);
}

export function createToken(form_data) {
  return API.POST('/api/internal/tokens', GENERATE_TOKEN, form_data);
}

export function deleteToken(tokenID) {
  return API.DELETE(
    `/api/internal/tokens/${tokenID}`,
    DELETE_TOKEN
  );
}


// Websocket message handler
messageHandler.add((action, payload, dispatch) => {
  if (action === FETCH_USER_PROFILE) {
    dispatch(fetchUserProfile());
  }
});


export default function reducer(state={ username: '', roles: [], acls: [], tokens: [] }, action) {
  switch (action.type) {
    case FETCH_USER_PROFILE_OK:
      return action.data;
    default:
      return state;
  }
}

import ClientOAuth2, { Token } from 'client-oauth2';

import { getOAuth2, getWithCredentials } from "./helpers";


export interface User {
  username: string;
  email: string;
  firstName: string;
  surname: string;
  displayName: string;
}





export default class Session {
  user?: User;
  token?: Token;

  constructor(user?: User, token?: Token) {
    this.user = user;
    this.token = token;
  }

  logIn = () => {
    console.log('Session.logIn');

    if (this.user) {
      console.warn('Session.logIn called while already logged in');
      return;
    }

    window.location.href = getOAuth2().token.getUri();
  }

  logOut = () => {
    console.warn('Session.logOut called while not logged in');
    // TODO
  }

  get(path: string) {
    return getWithCredentials(path, this.token ? this.token.accessToken : '');
  }
}


export const emptySession = new Session();

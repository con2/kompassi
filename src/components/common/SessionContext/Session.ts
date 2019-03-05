import Config from '../../../Config';
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
  accessToken?: string;

  constructor(user?: User, accessToken?: string) {
    this.user = user;
    this.accessToken = accessToken;
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
    if (!this.user) {
      console.warn('Session.logOut called while not logged in');
      return;
    }

    // TODO revoke token

    sessionStorage.clear();
    window.location.href = `${Config.api.baseUrl}/logout`;
  }

  get(path: string) {
    return getWithCredentials(path, this.accessToken || '');
  }
}


export const emptySession = new Session();

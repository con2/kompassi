import Config from '../../../Config';
import { fetchWithCredentials, getOAuth2 } from './helpers';

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
  };

  logOut = () => {
    if (!this.user) {
      console.warn('Session.logOut called while not logged in');
      return;
    }

    // TODO revoke token

    sessionStorage.clear();
    window.location.href = `${Config.api.baseUrl}/logout`;
  };

  get(path: string) {
    return fetchWithCredentials('GET', path, this.accessToken || '');
  }

  post(path: string, data: any) {
    return fetchWithCredentials('POST', path, this.accessToken || '', data);
  }

  put(path: string, data: any) {
    return fetchWithCredentials('PUT', path, this.accessToken || '', data);
  }

  delete(path: string) {
    return fetchWithCredentials('DELETE', path, this.accessToken || '');
  }
}

export const emptySession = new Session();

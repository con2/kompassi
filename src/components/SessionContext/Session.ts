import { getWithCredentials } from "./helpers";

export interface User {
  username: string;
  email: string;
  firstName: string;
  surname: string;
  displayName: string;
}


export default class Session {
  user?: User;
  token = '';

  constructor(user?: User) {
    this.user = user;
  }

  logIn = () => {
    console.log('Session.logIn');

    // TODO
    if (this.user) {
      console.warn('Session.logIn called while already logged in');
    }
  }

  logOut = () => {
    console.warn('Session.logOut called while not logged in');
    // TODO
  }

  get(path: string) {
    return getWithCredentials(path, this.token);
  }
}


export const emptySession = new Session();

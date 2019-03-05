import React from 'react';

import Loading from '../Loading';

import { getOAuth2, getWithCredentials } from './helpers';
import Session, { emptySession } from './Session';


const SessionContext = React.createContext<Session>(emptySession);
export const SessionConsumer = SessionContext.Consumer;


interface SessionProviderState {
  session?: Session;
}


export class SessionProvider extends React.Component<{}, SessionProviderState> {
  // why do I have to type this explicitly? :thinking:
  state: SessionProviderState = {
    session: undefined,
  };

  async componentDidMount() {
    let accessToken = sessionStorage.getItem('accessToken');

    if (window.location.hash) {
      const token = await getOAuth2().token.getToken(window.location.href);
      accessToken = token.accessToken;
    }

    if (accessToken) {
      try {
        const user = await getWithCredentials('user', accessToken);
        sessionStorage.setItem('accessToken', accessToken);
        this.setState({ session: new Session(user, accessToken) });
      } catch (e) {
        console.warn('Not logged in:', e);
        sessionStorage.clear();
        this.setState({ session: emptySession });
      }
    } else {
      this.setState({ session: emptySession });
    }

  }

  render() {
    const { session } = this.state;

    if (session) {
      return (
        <SessionContext.Provider value={session}>
          {this.props.children}
        </SessionContext.Provider>
      );
    } else {
      return <Loading />;
    }
  }
}


export default SessionContext;
